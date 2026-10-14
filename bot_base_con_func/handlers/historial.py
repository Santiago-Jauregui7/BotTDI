import csv
from datetime import datetime
from pathlib import Path

from telegram import Update
from telegram.ext import ContextTypes
from telegram.helpers import escape_markdown

RUTA_CSV = Path(__file__).resolve().parent.parent / "historial" / "historial.csv"
CAMPOS = ["timestamp", "chat_id", "nombre", "mensaje"]

# Consultas que no tiene sentido mostrar dentro del propio historial
IGNORAR_EN_HISTORIAL = {"/historial", "[botón] historial"}


def registrar_interaccion(chat_id, nombre, mensaje) -> None:
    """Agrega una fila al CSV (crea el archivo con encabezado si no existe)."""
    RUTA_CSV.parent.mkdir(exist_ok=True)
    existe = RUTA_CSV.exists()
    with open(RUTA_CSV, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if not existe:
            writer.writerow(CAMPOS)
        writer.writerow(
            [datetime.now().isoformat(timespec="seconds"), chat_id, nombre, mensaje]
        )


def ultimas_consultas(chat_id, cantidad: int = 5) -> list[dict]:
    """Devuelve las últimas `cantidad` consultas de ese chat (de la más vieja a la más nueva)."""
    if not RUTA_CSV.exists():
        return []
    with open(RUTA_CSV, newline="", encoding="utf-8") as f:
        filas = [
            fila
            for fila in csv.DictReader(f)
            if fila["chat_id"] == str(chat_id)
            and fila["mensaje"] not in IGNORAR_EN_HISTORIAL
        ]
    return filas[-cantidad:]


def texto_historial(chat_id) -> str:
    filas = ultimas_consultas(chat_id)
    if not filas:
        return "📜 *Historial de consultas*\n\nTodavía no hiciste ninguna consulta."

    lineas = ["📜 *Tus últimas consultas*\n"]
    for fila in filas:
        mensaje = escape_markdown(fila["mensaje"])
        lineas.append(f"• `{fila['timestamp']}` — {mensaje}")
    return "\n".join(lineas)


async def registrar_update(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Se ejecuta ANTES que cualquier otro handler y anota todo en el CSV."""
    usuario = update.effective_user
    chat = update.effective_chat
    if usuario is None or chat is None:
        return

    if update.message and update.message.text:
        mensaje = update.message.text
    elif update.callback_query:
        mensaje = f"[botón] {update.callback_query.data}"
    elif update.message:
        mensaje = "[mensaje sin texto]"  # audio, documento, foto, etc.
    else:
        return

    registrar_interaccion(chat.id, usuario.first_name, mensaje)


async def historial(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Comando /historial: muestra las últimas 5 consultas del usuario."""
    await update.message.reply_text(
        texto_historial(update.effective_chat.id), parse_mode="Markdown"
    )