"""
Carga la configuración del bot desde el archivo .env.
No hardcodear tokens ni claves acá: todo sale de las variables de entorno.
"""
import os
from dotenv import load_dotenv

load_dotenv()  # busca el archivo .env en la carpeta del proyecto

BOT_TOKEN = os.getenv("BOT_TOKEN")
API_KEY_DATOS_ARG = os.getenv("API_KEY_DATOS_ARG")  # ArgentinaDatos no exige key hoy, se deja por si cambia
CHAT_ID_ADMIN = os.getenv("CHAT_ID_ADMIN")

if not BOT_TOKEN:
    raise RuntimeError(
        "Falta BOT_TOKEN en el archivo .env. "
        "Copiá .env.example como .env y completá el token de BotFather."
    )
