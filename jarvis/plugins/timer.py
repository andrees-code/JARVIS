import asyncio
import time

TOOL = {
    "name": "timer",
    "description": "Pon alarmas, temporizadores y recordatorios con cuenta atrás",
    "parameters": {
        "accion": "string (alarma | temporizador | recordatorio)",
        "cuando": "string (ej: '5 minutos', '10 segundos', 'mañana 8am')",
        "mensaje": "string (mensaje del recordatorio)",
    },
}


async def execute(accion: str = "", cuando: str = "", mensaje: str = ""):
    segundos = _parse_time(cuando)

    if segundos is None:
        return {"error": f"No entendí el tiempo '{cuando}'. Prueba con '30 segundos' o '5 minutos'"}

    if accion in ("temporizador", "timer"):
        return await _timer(segundos, mensaje or "Temporizador")

    elif accion == "alarma":
        return {"ok": True, "mensaje": f"Alarma puesta para {cuando}", "segundos": segundos}

    elif accion == "recordatorio":
        return {
            "ok": True,
            "mensaje": f"Recordatorio '{mensaje}' en {cuando}",
            "segundos": segundos,
        }

    return {"error": f"Acción '{accion}' no soportada"}


async def _timer(segundos, nombre):
    print(f"[TIMER] {nombre}: {segundos}s")
    await asyncio.sleep(segundos)
    print(f"[TIMER] ¡{nombre} terminado!")

    import subprocess
    subprocess.run(["osascript", "-e", f'display notification "¡Terminó!" with title "{nombre}"'])

    return {"ok": True, "mensaje": f"Temporizador '{nombre}' de {segundos}s terminado"}


def _parse_time(texto):
    texto = texto.lower().strip()
    try:
        import re
        match = re.search(r"(\d+)\s*(segundos|segundo|minutos|minuto|horas|hora)", texto)
        if match:
            num = int(match.group(1))
            unit = match.group(2)
            if "hora" in unit:
                return num * 3600
            elif "minuto" in unit:
                return num * 60
            else:
                return num
    except Exception:
        pass

    try:
        return int(texto)
    except Exception:
        return None
