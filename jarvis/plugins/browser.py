TOOL = {
    "name": "browser",
    "description": "Busca información en internet usando un navegador",
    "parameters": {
        "query": "string (términos de búsqueda)",
    },
}


async def execute(query: str = ""):
    if not query:
        return {"error": "Se necesita un término de búsqueda"}

    import webbrowser
    import urllib.parse

    encoded = urllib.parse.quote(query)
    url = f"https://www.google.com/search?q={encoded}"
    webbrowser.open(url)

    return {"ok": True, "mensaje": f"Buscando '{query}' en Google", "url": url}
