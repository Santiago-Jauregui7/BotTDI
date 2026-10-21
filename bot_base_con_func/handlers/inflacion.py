import io

import matplotlib

matplotlib.use("Agg")  # sin ventana: el bot genera la imagen en memoria
import matplotlib.pyplot as plt
import requests
from telegram import Update
from telegram.ext import ContextTypes

URL_INFLACION = "https://api.argentinadatos.com/v1/finanzas/indices/inflacion"
MESES = ["ene", "feb", "mar", "abr", "may", "jun",
         "jul", "ago", "sep", "oct", "nov", "dic"]


def obtener_inflacion(cantidad: int = 6):
    """Devuelve los últimos `cantidad` meses ordenados por fecha, o None si falla."""
    try:
        response = requests.get(URL_INFLACION, timeout=10)
        response.raise_for_status()
        datos = response.json()
    except requests.RequestException:
        return None
    datos = sorted(datos, key=lambda d: d["fecha"])
    return datos[-cantidad:]


def _etiqueta(fecha: str) -> str:
    """'2026-08-31' -> 'ago 26'"""
    anio, mes = fecha.split("-")[:2]
    return f"{MESES[int(mes) - 1]} {anio[2:]}"


def generar_grafico(datos: list[dict]) -> io.BytesIO:
    etiquetas = [_etiqueta(d["fecha"]) for d in datos]
    valores = [d["valor"] for d in datos]

    fig, ax = plt.subplots(figsize=(8, 5))
    barras = ax.bar(etiquetas, valores, color="#4C78A8")
    ax.bar_label(barras, fmt="%.1f%%", padding=3)
    ax.set_title(f"Inflación mensual — últimos {len(datos)} meses")
    ax.set_ylabel("Variación mensual (%)")
    ax.margins(y=0.15)
    ax.grid(axis="y", alpha=0.3)
    fig.tight_layout()

    buffer = io.BytesIO()
    fig.savefig(buffer, format="png", dpi=150)
    plt.close(fig)  # libera memoria: sin esto, cada gráfico queda abierto
    buffer.seek(0)
    return buffer


def _texto(datos: list[dict]) -> str:
    acumulada = 1.0
    for d in datos:
        acumulada *= 1 + d["valor"] / 100
    acumulada = (acumulada - 1) * 100

    ultimo = datos[-1]
    return (
        "📈 *Inflación mensual*\n\n"
        f"Último dato ({_etiqueta(ultimo['fecha'])}): *{ultimo['valor']}%*\n"
        f"Acumulada en {len(datos)} meses: *{acumulada:.1f}%*\n\n"
        "_Fuente: BCRA vía ArgentinaDatos_"
    )


async def enviar_grafico_inflacion(chat_id: int, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sirve tanto para el comando /inflacion como para el botón del /ayuda."""
    await context.bot.send_chat_action(chat_id=chat_id, action="upload_photo")

    datos = obtener_inflacion()
    if not datos:
        await context.bot.send_message(
            chat_id=chat_id,
            text="😕 No pude consultar la inflación ahora. Probá de nuevo en un rato.",
        )
        return

    await context.bot.send_photo(
        chat_id=chat_id,
        photo=generar_grafico(datos),
        caption=_texto(datos),
        parse_mode="Markdown",
    )


async def inflacion(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Comando /inflacion."""
    await enviar_grafico_inflacion(update.effective_chat.id, context)