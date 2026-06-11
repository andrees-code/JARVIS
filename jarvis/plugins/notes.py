from pathlib import Path
from datetime import datetime


TOOL = {
    "name": "notes",
    "description": "Crea, lee y busca notas rápidas de texto. Guárdalas en una carpeta de notas local",
    "parameters": {
        "accion": "string (crear | leer | buscar | listar)",
        "titulo": "string (título o nombre de la nota)",
        "contenido": "string (texto de la nota, solo para 'crear')",
    },
}

NOTES_DIR = Path.home() / "JARVIS" / "notas"


async def execute(accion: str = "", titulo: str = "", contenido: str = ""):
    NOTES_DIR.mkdir(parents=True, exist_ok=True)

    if accion == "crear":
        return _create_note(titulo, contenido)

    elif accion == "leer":
        return _read_note(titulo)

    elif accion == "listar":
        return _list_notes()

    elif accion == "buscar":
        return _search_notes(titulo)

    return {"error": f"Acción '{accion}' no soportada. Usa: crear, leer, listar, buscar"}


def _create_note(titulo, contenido):
    if not titulo:
        titulo = f"nota_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    if not contenido:
        return {"error": "Necesito contenido para crear la nota"}

    safe_name = "".join(c for c in titulo if c.isalnum() or c in " _-").rstrip()
    filepath = NOTES_DIR / f"{safe_name}.txt"

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    full_content = f"# {titulo}\n{timestamp}\n\n{contenido}"

    filepath.write_text(full_content)
    return {"ok": True, "mensaje": f"Nota '{titulo}' creada", "ruta": str(filepath)}


def _read_note(titulo):
    path = _find_note(titulo)
    if not path:
        return {"error": f"No encontré la nota '{titulo}'"}

    text = path.read_text()
    return {"ok": True, "titulo": path.stem, "contenido": text}


def _list_notes():
    files = sorted(NOTES_DIR.glob("*.txt"), key=lambda p: p.stat().st_mtime, reverse=True)
    if not files:
        return {"ok": True, "mensaje": "No hay notas todavía", "items": []}

    items = []
    for f in files[:20]:
        first_line = f.read_text().split("\n")[0].replace("# ", "")[:60]
        items.append(f"📝 {first_line} ({f.stem})")

    return {"ok": True, "items": items, "total": len(files)}


def _search_notes(query):
    results = []
    for f in NOTES_DIR.glob("*.txt"):
        text = f.read_text().lower()
        if query.lower() in text:
            first_line = text.split("\n")[0].replace("# ", "")[:80]
            results.append({"archivo": f.stem, "titulo": first_line})

    if not results:
        return {"ok": True, "mensaje": f"No encontré notas con '{query}'", "items": []}

    return {"ok": True, "items": [f"📝 {r['titulo']}" for r in results], "total": len(results)}


def _find_note(titulo):
    for f in NOTES_DIR.glob("*.txt"):
        if titulo.lower() in f.stem.lower():
            return f
    return None
