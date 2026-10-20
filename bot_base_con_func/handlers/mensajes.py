from telegram import Update
from telegram.ext import ContextTypes

AYUDA = "Escribí /ayuda para ver lo que sí puedo hacer 😉"


async def texto_libre(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        f"🤔 No puedo interpretar texto libre, solo respondo a comandos.\n\n{AYUDA}"
    )


async def comando_desconocido(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        f"🤷 No conozco ese comando.\n\n{AYUDA}"
    )


async def audio(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        f"🎧 No puedo escuchar audios.\n\n{AYUDA}"
    )


async def imagen(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        f"🖼️ No puedo interpretar imágenes.\n\n{AYUDA}"
    )


async def documento(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        f"📄 No puedo leer documentos.\n\n{AYUDA}"
    )


async def otro_tipo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        f"🙈 No puedo procesar ese tipo de mensaje.\n\n{AYUDA}"
    )

async def video(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        f"🎬 No puedo interpretar videos.\n\n{AYUDA}"
    )