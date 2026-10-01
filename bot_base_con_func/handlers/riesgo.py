import requests


def obtener_riesgo_pais():
    """
    Consulta el último valor publicado del riesgo país.
    Devuelve un dict {"valor": int, "fecha": "YYYY-MM-DD"}, o None si falla.
    """
    try:
        response = requests.get(
            "https://api.argentinadatos.com/v1/finanzas/indices/riesgo-pais/ultimo",
            timeout=10,
        )
        response.raise_for_status()
        return response.json()
    except requests.RequestException:
        return None


def texto_riesgo_pais() -> str:
    dato = obtener_riesgo_pais()

    if dato is None:
        return "😕 No pude consultar el riesgo país ahora. Probá de nuevo en un rato."

    return (
        "📊 *Riesgo país*\n\n"
        f"*{dato['valor']}* puntos básicos\n"
        f"_(al {dato['fecha']})_"
    )