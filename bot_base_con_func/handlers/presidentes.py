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


def _agrupar_por_nombre(presidentes: list[dict]) -> list[list[dict]]:
    """
    Agrupa los mandatos de una misma persona.
    Devuelve una lista de grupos: cada grupo es la lista de mandatos de un presidente.
    """
    grupos: dict[str, list[dict]] = {}
    for p in presidentes:
        clave = _normalizar(p.get("nombre", "s/d"))
        grupos.setdefault(clave, []).append(p)
    return list(grupos.values())


def _ficha(mandatos: list[dict]) -> str:
    primero = mandatos[0]
    lineas = [f"🏛️ *{escape_markdown(primero.get('nombre', 's/d'))}*"]

    if len(mandatos) == 1:
        if primero.get("periodoPresidencial"):
            lineas.append(f"📅 Período: {escape_markdown(primero['periodoPresidencial'])}")
        if primero.get("partido"):
            lineas.append(f"🎗️ Partido: {escape_markdown(primero['partido'])}")
        if primero.get("vicepresidente"):
            lineas.append(f"🤝 Vicepresidente: {escape_markdown(primero['vicepresidente'])}")
        return "\n".join(lineas)

    lineas.append(f"\n📅 *{len(mandatos)} mandatos:*")
    for i, m in enumerate(mandatos, start=1):
        detalle = escape_markdown(m.get("periodoPresidencial", "s/d"))
        extras = []
        if m.get("partido"):
            extras.append(escape_markdown(m["partido"]))
        if m.get("vicepresidente"):
            extras.append(f"VP: {escape_markdown(m['vicepresidente'])}")
        if extras:
            detalle += f" ({', '.join(extras)})"
        lineas.append(f"{i}. {detalle}")
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

    for mandatos in _agrupar_por_nombre(coincidencias)[:3]:  # máximo 3 personas
        ficha = _ficha(mandatos)
        imagen = next((m["imagen"] for m in mandatos if m.get("imagen")), None)
        if imagen:
            try:
                await update.message.reply_photo(
                    photo=imagen, caption=ficha, parse_mode="Markdown"
                )
                continue
            except TelegramError:
                pass  # si Telegram no puede bajar la imagen, mandamos solo el texto
        await update.message.reply_text(ficha, parse_mode="Markdown")