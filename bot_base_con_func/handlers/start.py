from telegram import Update
from telegram.ext import ContextTypes


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
        "riesgo país, confianza en el gobierno y más.\n\n"
        "Escribí /ayuda para ver todo lo que puedo hacer."
    )

    await update.message.reply_text(mensaje, parse_mode="Markdown")
