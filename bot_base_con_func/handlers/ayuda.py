from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

from handlers.dolar import texto_cotizacion_dolar
from handlers.riesgo import texto_riesgo_pais
from handlers.historial import texto_historial
from handlers.presidentes import texto_presidentes_recientes

# callback_data -> texto de respuesta cuando todavía no está implementado
FUNCIONES_PENDIENTES = {
    "dolar": "💵 *Cotización del dólar*\n\nEsta función todavía está en construcción 🚧. ¡Ya la sumamos!",
    "riesgo_pais": "📊 *Riesgo país*\n\nEsta función todavía está en construcción 🚧. ¡Ya la sumamos!",
    "inflación mensual": "🏛️ *Grafica de inflación*\n\nEsta función todavía está en construcción 🚧. ¡Ya la sumamos!",
    "presidentes": "🕰️ *Presidentes históricos*\n\nEsta función todavía está en construcción 🚧. ¡Ya la sumamos!",
    "historial": "📜 *Historial de consultas*\n\nEsta función todavía está en construcción 🚧. ¡Ya la sumamos!",
}


def _teclado_ayuda() -> InlineKeyboardMarkup:
    botones = [
        [InlineKeyboardButton("💵 Cotización del dólar", callback_data="dolar")],
        [InlineKeyboardButton("📊 Riesgo país", callback_data="riesgo_pais")],
        [InlineKeyboardButton("🏛️ Inflación mensual", callback_data="inflacion_mensual")],
        [InlineKeyboardButton("🕰️ Presidentes históricos", callback_data="presidentes")],
        [InlineKeyboardButton("📜 Historial de consultas", callback_data="historial")],
    ]
    return InlineKeyboardMarkup(botones)


async def ayuda(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Comando /ayuda.
    Lista los comandos principales y ofrece atajos como botones inline.
    """
    texto = (
        "📋 *Comandos disponibles:*\n\n"
        "/start — iniciar la conversación\n"
        "/ayuda — ver esta ayuda\n\n"
        "/historial — ver tus últimas 5 consultas\n\n"
        "/presidente <nombre> — buscar un presidente histórico\n\n"
        "También podés tocar uno de estos atajos 👇"
    )
    await update.message.reply_text(
        texto, parse_mode="Markdown", reply_markup=_teclado_ayuda()
    )


async def boton_ayuda(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Se ejecuta cuando el usuario toca alguno de los botones inline del /ayuda.
    Por ahora responde con un mensaje "en construcción"; cada opción se va
    a ir reemplazando por la consulta real a la API correspondiente.
    """
    query = update.callback_query
    await query.answer()  # le saca el "reloj de carga" al botón en Telegram

    if query.data == "dolar":
        await context.bot.send_chat_action(chat_id=query.message.chat_id, action="typing")
        respuesta = texto_cotizacion_dolar()
    elif query.data == "riesgo_pais":
        await context.bot.send_chat_action(chat_id=query.message.chat_id, action="typing")
        respuesta = texto_riesgo_pais()
    elif query.data == "historial":
        respuesta = texto_historial(query.message.chat_id)
    elif query.data == "presidentes":
        await context.bot.send_chat_action(chat_id=query.message.chat_id, action="typing")
        respuesta = texto_presidentes_recientes()
    else:
        respuesta = FUNCIONES_PENDIENTES.get(
            query.data, "No reconozco esa opción todavía 🤔"
        )

    await query.message.reply_text(respuesta, parse_mode="Markdown")
