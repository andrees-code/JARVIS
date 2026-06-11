TOOL = {
    "name": "weather",
    "description": "Consulta el tiempo meteorológico actual y previsión para una ciudad usando Open-Meteo (gratis, sin API key)",
    "parameters": {
        "ciudad": "string (nombre de la ciudad, ej: 'Madrid', 'Buenos Aires')",
    },
}


async def execute(ciudad: str = ""):
    if not ciudad:
        return {"error": "Dime la ciudad para consultar el tiempo"}

    coords = await _geocode(ciudad)

    if not coords:
        return {"error": f"No encontré coordenadas para '{ciudad}'"}

    lat, lon, name = coords
    weather = await _get_weather(lat, lon)

    return {
        "ok": True,
        "ciudad": name,
        "temperatura": f"{weather['temp']}°C",
        "sensacion": f"{weather['feels_like']}°C",
        "humedad": f"{weather['humidity']}%",
        "viento": f"{weather['wind']} km/h",
        "descripcion": weather["desc"],
    }


async def _geocode(city):
    try:
        import urllib.request
        import json
        import urllib.parse

        encoded = urllib.parse.quote(city)
        url = (
            f"https://geocoding-api.open-meteo.com/v1/search"
            f"?name={encoded}&count=1&language=es&format=json"
        )

        req = urllib.request.Request(url, headers={"User-Agent": "JARVIS/1.0"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read())

        if data.get("results"):
            r = data["results"][0]
            return (r["latitude"], r["longitude"], f"{r['name']}, {r.get('country', '')}")

    except Exception:
        pass

    return None


async def _get_weather(lat, lon):
    try:
        import urllib.request
        import json

        url = (
            f"https://api.open-meteo.com/v1/forecast"
            f"?latitude={lat}&longitude={lon}"
            f"&current=temperature_2m,relative_humidity_2m,apparent_temperature,wind_speed_10m,weather_code"
            f"&timezone=auto"
        )

        req = urllib.request.Request(url, headers={"User-Agent": "JARVIS/1.0"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read())

        current = data.get("current", {})
        code = current.get("weather_code", 0)

        weather_codes = {
            0: "Despejado", 1: "Mayormente despejado", 2: "Parcialmente nublado",
            3: "Nublado", 45: "Niebla", 48: "Niebla con escarcha",
            51: "Llovizna ligera", 53: "Llovizna", 55: "Llovizna intensa",
            61: "Lluvia ligera", 63: "Lluvia", 65: "Lluvia intensa",
            71: "Nieve ligera", 73: "Nieve", 75: "Nieve intensa",
            80: "Chubascos", 95: "Tormenta", 96: "Tormenta con granizo",
        }

        return {
            "temp": current.get("temperature_2m", "?"),
            "feels_like": current.get("apparent_temperature", "?"),
            "humidity": current.get("relative_humidity_2m", "?"),
            "wind": current.get("wind_speed_10m", "?"),
            "desc": weather_codes.get(code, f"Código {code}"),
        }

    except Exception:
        pass

    return {"temp": "?", "feels_like": "?", "humidity": "?", "wind": "?", "desc": "No disponible"}
