import requests
from telegram import Update
from telegram.ext import ContextTypes

NOMBRES_CASAS = {
    "oficial": "Dólar Oficial",
    "blue": "Dólar Blue",
}

def obtener_cotizaciones():
    """
    Consulta todas las cotizaciones del dólar en un solo pedido.
    Devuelve la lista completa, o None si algo falla.
    """
    try:
        response = requests.get(
            "https://api.argentinadatos.com/v1/cotizaciones/dolares",
            timeout=10,
        )
        response.raise_for_status()
        return response.json()
    except requests.RequestException:
        return None


def obtener_ultima_cotizacion(cotizaciones, casa):
    """
    De la lista completa (todas las casas, todas las fechas),
    devuelve el registro más reciente de una casa puntual.
    """
    de_esa_casa = [c for c in cotizaciones if c["casa"] == casa]
    if not de_esa_casa:
        return None
    return max(de_esa_casa, key=lambda c: c["fecha"])


def texto_cotizacion_dolar() -> str:
    cotizaciones = obtener_cotizaciones()

    if cotizaciones is None:
        return "😕 No pude consultar la cotización ahora. Probá de nuevo en un rato."

    lineas = ["💵 *Cotización del dólar*\n"]

    for casa, nombre in NOMBRES_CASAS.items():
        item = obtener_ultima_cotizacion(cotizaciones, casa)
        if item is None:
            lineas.append(f"*{nombre}*: no disponible")
            continue
        lineas.append(
            f"*{nombre}*: compra ${item['compra']} / venta ${item['venta']}"
            f"_(al {item['fecha']})_"
        )

    return "\n".join(lineas)