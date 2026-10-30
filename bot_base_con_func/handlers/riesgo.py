from datetime import date, timedelta

import requests

URL_ULTIMO = "https://api.argentinadatos.com/v1/finanzas/indices/riesgo-pais/ultimo"
URL_SERIE = "https://api.argentinadatos.com/v1/finanzas/indices/riesgo-pais"


def obtener_riesgo_pais():
    """Último valor publicado: {"valor": int, "fecha": "YYYY-MM-DD"}, o None si falla."""
    try:
        response = requests.get(URL_ULTIMO, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException:
        return None


def _dato_hace_30_dias(fecha_ultima: str):
    """
    Busca en la serie histórica el último valor publicado hasta 30 días antes.
    Devuelve None ante cualquier problema: la comparación es un extra,
    si falla el mensaje sale igual sin ella.
    """
    try:
        response = requests.get(URL_SERIE, timeout=10)
        response.raise_for_status()
        serie = response.json()
        limite = (date.fromisoformat(fecha_ultima) - timedelta(days=30)).isoformat()
        anteriores = [d for d in serie if d["fecha"] <= limite]
        if not anteriores:
            return None
        return max(anteriores, key=lambda d: d["fecha"])
    except (requests.RequestException, ValueError, KeyError, TypeError):
        return None


def texto_riesgo_pais() -> str:
    dato = obtener_riesgo_pais()

    if dato is None:
        return "😕 No pude consultar el riesgo país ahora. Probá de nuevo en un rato."

    valor = dato["valor"]
    puntos_porcentuales = f"{valor / 100:.2f}".replace(".", ",")

    lineas = [
        "📊 *Riesgo país*\n",
        f"*{valor}* puntos básicos _(al {dato['fecha']})_\n",
        "💡 *¿Qué significa?*",
        "Es el extra de interés que los inversores piden para prestarle plata a "
        "Argentina, comparado con lo que paga EE.UU. (considerado el deudor más seguro).",
        f"En este caso, {puntos_porcentuales} puntos porcentuales más "
        "(100 puntos básicos equivalen a 1 punto porcentual).",
        "Si baja, los inversores perciben menos riesgo; si sube, perciben más.",
    ]

    anterior = _dato_hace_30_dias(dato["fecha"])
    if anterior:
        diferencia = valor - anterior["valor"]
        if diferencia > 0:
            tendencia = f"🔺 Subió {diferencia} puntos"
        elif diferencia < 0:
            tendencia = f"🔻 Bajó {abs(diferencia)} puntos"
        else:
            tendencia = "➡️ Se mantuvo igual"
        lineas.append(
            f"\n{tendencia} en los últimos 30 días "
            f"(era {anterior['valor']} el {anterior['fecha']})."
        )

    return "\n".join(lineas)