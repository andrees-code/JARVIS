TOOL = {
    "name": "youtube",
    "description": "Busca vídeos en YouTube y los reproduce en el navegador o Chromecast",
    "parameters": {
        "query": "string (términos de búsqueda en YouTube)",
    },
}


async def execute(query: str = ""):
    if not query:
        return {"error": "Necesito saber qué quieres buscar en YouTube"}

    url = await _search_youtube(query)

    if not url:
        return {"error": f"No encontré resultados para '{query}' en YouTube"}

    casted = _try_cast(url)

    if casted:
        return {"ok": True, "mensaje": f"Reproduciendo '{query}' en la TV", "url": url}

    import webbrowser
    webbrowser.open(url)
    return {"ok": True, "mensaje": f"Abriendo '{query}' en YouTube", "url": url}


async def _search_youtube(query):
    from playwright.async_api import async_playwright
    import urllib.parse

    encoded = urllib.parse.quote(query)
    search_url = f"https://www.youtube.com/results?search_query={encoded}"

    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            await page.goto(search_url, wait_until="domcontentloaded", timeout=15000)

            await page.wait_for_selector("ytd-video-renderer a#video-title", timeout=8000)

            href = await page.evaluate("""
                () => {
                    const link = document.querySelector('ytd-video-renderer a#video-title');
                    return link ? link.href : null;
                }
            """)

            await browser.close()

            if href and "watch" in href:
                return href

    except Exception:
        pass

    return f"https://www.youtube.com/results?search_query={encoded}"


def _try_cast(url):
    try:
        import pychromecast
        chromecasts, _ = pychromecast.get_chromecasts(timeout=3)

        if not chromecasts:
            return False

        cast = chromecasts[0]
        cast.wait()
        mc = cast.media_controller
        mc.play_media(url, "video/mp4")
        mc.block_until_active(timeout=5)
        return True

    except Exception:
        return False
