import logging
 
from telegram.ext import ApplicationBuilder, CallbackQueryHandler, CommandHandler, TypeHandlerMessageHandler, filters
from telegram import Update
from handlers import mensajes
from handlers.historial import historial, registrar_update
from handlers.presidentes import presidente
 
from config import BOT_TOKEN
from handlers.start import start
from handlers.ayuda import ayuda, boton_ayuda
 
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
 
 
def main() -> None:
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # group=-1 => corre antes que todo lo demás y registra cada interacción
    app.add_handler(TypeHandler(Update, registrar_update), group=-1)
    # Comandos
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("ayuda", ayuda))
    app.add_handler(CommandHandler("historial", historial))
    app.add_handler(CommandHandler("presidente", presidente))

 
    # Botones inline (los del /ayuda por ahora)
    app.add_handler(CallbackQueryHandler(boton_ayuda))
 
    # A medida que sumemos funcionalidades (dólar, historial, etc.)
    # cada una va en handlers/ y se registra acá con una línea nueva.

    # Mensajes que no son comandos (van al final: dentro de un mismo grupo
    #  gana el primer handler que coincide, así que los comandos reales tienen prioridad)
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, mensajes.texto_libre))
    app.add_handler(MessageHandler(filters.VOICE | filters.AUDIO, mensajes.audio))
    app.add_handler(MessageHandler(filters.PHOTO, mensajes.imagen))
    app.add_handler(MessageHandler(filters.Document.ALL, mensajes.documento))
    app.add_handler(MessageHandler(filters.COMMAND, mensajes.comando_desconocido))
    app.add_handler(MessageHandler(filters.ALL, mensajes.otro_tipo))  # stickers, videos, etc.
    app.add_handler(MessageHandler(filters.VIDEO | filters.VIDEO_NOTE, mensajes.video))

    
    print("Bot corriendo... (Ctrl+C para detener)")
    app.run_polling()
 
 
if __name__ == "__main__":
    main()
 