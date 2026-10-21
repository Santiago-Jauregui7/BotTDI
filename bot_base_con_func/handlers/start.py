from telegram import Update
from telegram.ext import ContextTypes
from telegram.error import TelegramError
from telegram.helpers import escape_markdown

from config import CHAT_ID_ADMIN


async def _avisar_al_admin(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Segundo chat de la respuesta: le avisa al admin que alguien inició el bot."""
    if not CHAT_ID_ADMIN:
        return

    usuario = update.effective_user
    username = f"@{usuario.username}" if usuario.username else "sin username"
    texto = (
        "🔔 *Nuevo /start*\n\n"
        f"Nombre: {escape_markdown(usuario.full_name)}\n"
        f"Usuario: {escape_markdown(username)}\n"
        f"Chat ID: `{update.effective_chat.id}`"
    )
    try:
        await context.bot.send_message(
            chat_id=int(CHAT_ID_ADMIN), text=texto, parse_mode="Markdown"
        )
    except (TelegramError, ValueError):
        pass  # si falla el aviso, que no afecte la respuesta al usuario

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Comando /start.
    Saluda al usuario por su nombre y da el pantallazo inicial del flujo de diálogo.
    """
    nombre = update.effective_user.first_name or "che"

    mensaje = (
        f"¡Hola {nombre}! 👋\n\n"
        "Soy tu bot de *finanzas, política y cultura general* de Argentina.\n"
        "Puedo contarte sobre la cotización del dólar, presidentes históricos, "
        "riesgo país, inflacion mensual y más.\n\n"
        "Escribí /ayuda para ver todo lo que puedo hacer."
    )

    await update.message.reply_text(mensaje, parse_mode="Markdown")
    await _avisar_al_admin(update, context)
