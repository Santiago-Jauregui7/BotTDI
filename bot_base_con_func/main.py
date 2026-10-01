import logging
 
from telegram.ext import ApplicationBuilder, CallbackQueryHandler, CommandHandler
 
from config import BOT_TOKEN
from handlers.start import start
from handlers.ayuda import ayuda, boton_ayuda
 
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
 
 
def main() -> None:
    app = ApplicationBuilder().token(BOT_TOKEN).build()
 
    # Comandos
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("ayuda", ayuda))
 
    # Botones inline (los del /ayuda por ahora)
    app.add_handler(CallbackQueryHandler(boton_ayuda))
 
    # A medida que sumemos funcionalidades (dólar, historial, etc.)
    # cada una va en handlers/ y se registra acá con una línea nueva.
 
    print("Bot corriendo... (Ctrl+C para detener)")
    app.run_polling()
 
 
if __name__ == "__main__":
    main()
 