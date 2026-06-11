from pathlib import Path


TOOL = {
    "name": "files",
    "description": "Operaciones con archivos: leer, escribir, listar contenidos de carpetas",
    "parameters": {
        "action": "string (leer | escribir | listar)",
        "ruta": "string (ruta del archivo o carpeta)",
        "contenido": "string (solo para escribir, contenido opcional)",
    },
}


async def execute(action: str, ruta: str = "", contenido: str = ""):
    path = Path(ruta).expanduser().resolve()

    if action == "leer":
        if not path.exists():
            return {"error": f"Archivo no encontrado: {ruta}"}
        try:
            text = path.read_text()
            preview = text[:3000]
            return {"ok": True, "contenido": preview, "ruta": str(path)}
        except Exception as e:
            return {"error": str(e)}

    elif action == "escribir":
        try:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(contenido)
            return {"ok": True, "mensaje": f"Escrito en {path.name}", "ruta": str(path)}
        except Exception as e:
            return {"error": str(e)}

    elif action == "listar":
        if not path.exists():
            return {"error": f"Carpeta no encontrada: {ruta}"}
        if not path.is_dir():
            path = path.parent
        items = []
        for p in sorted(path.iterdir()):
            tipo = "📁" if p.is_dir() else "📄"
            items.append(f"{tipo} {p.name}")
        return {"ok": True, "items": items[:50], "total": len(items)}

    return {"error": f"Acción '{action}' no soportada"}
