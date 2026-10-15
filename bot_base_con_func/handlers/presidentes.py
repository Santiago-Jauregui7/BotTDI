import unicodedata

import requests
from telegram import Update
from telegram.error import TelegramError
from telegram.ext import ContextTypes
from telegram.helpers import escape_markdown

URL_PRESIDENTES = "https://api.argentinadatos.com/v1/presidentes"


def obtener_presidentes():
    """Devuelve la lista de presidentes, o None si falla la consulta."""
    try:
        response = requests.get(URL_PRESIDENTES, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException:
        return None


def _normalizar(texto: str) -> str:
    """Minúsculas y sin tildes, para que 'peron' encuentre 'Perón'."""
    sin_tildes = unicodedata.normalize("NFD", texto)
    sin_tildes = "".join(c for c in sin_tildes if unicodedata.category(c) != "Mn")
    return sin_tildes.lower()


def _ficha(p: dict) -> str:
    lineas = [f"🏛️ *{escape_markdown(p.get('nombre', 's/d'))}*"]
    if p.get("periodoPresidencial"):
        lineas.append(f"📅 Período: {escape_markdown(p['periodoPresidencial'])}")
    if p.get("partido"):
        lineas.append(f"🎗️ Partido: {escape_markdown(p['partido'])}")
    if p.get("vicepresidente"):
        lineas.append(f"🤝 Vicepresidente: {escape_markdown(p['vicepresidente'])}")
    return "\n".join(lineas)


def texto_presidentes_recientes(cantidad: int = 5) -> str:
    """Para el botón del /ayuda: los últimos presidentes de la lista."""
    presidentes = obtener_presidentes()
    if presidentes is None:
        return "😕 No pude consultar los presidentes ahora. Probá de nuevo en un rato."

    lineas = ["🕰️ *Últimos presidentes*\n"]
    for p in reversed(presidentes[-cantidad:]):
        nombre = escape_markdown(p.get("nombre", "s/d"))
        periodo = escape_markdown(p.get("periodoPresidencial", "s/d"))
        lineas.append(f"• *{nombre}* — {periodo}")
    lineas.append("\nBuscá uno puntual con /presidente seguido del nombre.")
    lineas.append("Ejemplo: /presidente Sarmiento")
    return "\n".join(lineas)


async def presidente(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Comando /presidente <nombre>: busca por nombre y manda la ficha con foto."""
    consulta = " ".join(context.args).strip()
    if not consulta:
        await update.message.reply_text(
            "Decime a quién buscar 🔎\nEjemplo: /presidente Sarmiento"
        )
        return

    chat_id = update.effective_chat.id
    await context.bot.send_chat_action(chat_id=chat_id, action="typing")

    presidentes = obtener_presidentes()
    if presidentes is None:
        await update.message.reply_text(
            "😕 No pude consultar los presidentes ahora. Probá de nuevo en un rato."
        )
        return

    buscado = _normalizar(consulta)
    coincidencias = [
        p for p in presidentes if buscado in _normalizar(p.get("nombre", ""))
    ]

    if not coincidencias:
        await update.message.reply_text(
            f"No encontré presidentes que coincidan con «{consulta}» 🤔"
        )
        return

    for p in coincidencias[:3]:  # máximo 3 para no inundar el chat
        ficha = _ficha(p)
        if p.get("imagen"):
            try:
                await update.message.reply_photo(
                    photo=p["imagen"], caption=ficha, parse_mode="Markdown"
                )
                continue
            except TelegramError:
                pass  # si Telegram no puede bajar la imagen, mandamos solo el texto
        await update.message.reply_text(ficha, parse_mode="Markdown")