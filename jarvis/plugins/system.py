TOOL = {
    "name": "system",
    "description": "Controla el sistema: abre apps, ajusta volumen, brillo de pantalla",
    "parameters": {
        "action": "string (abrir_app | volumen | brillo)",
        "target": "string (nombre de app, o 'subir'/'bajar', o 0-100)",
    },
}


async def execute(action: str, target: str = ""):
    if action == "abrir_app":
        import subprocess
        subprocess.Popen(["open", "-a", target])
        return {"ok": True, "mensaje": f"Aplicación '{target}' abierta"}

    elif action == "volumen":
        import subprocess
        if target in ("subir", "up"):
            subprocess.run(["osascript", "-e", "set volume output volume (output volume of (get volume settings) + 10)"])
        elif target in ("bajar", "down"):
            subprocess.run(["osascript", "-e", "set volume output volume (output volume of (get volume settings) - 10)"])
        else:
            val = int(target)
            subprocess.run(["osascript", "-e", f"set volume output volume {val}"])
        return {"ok": True, "mensaje": f"Volumen ajustado: {target}"}

    elif action == "brillo":
        import subprocess
        val = float(target) / 100.0
        subprocess.run(["brightness", str(val)], capture_output=True)
        return {"ok": True, "mensaje": f"Brillo ajustado al {target}%"}

    return {"error": f"Acción '{action}' no soportada"}
