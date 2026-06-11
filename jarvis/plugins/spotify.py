import os
import json
import urllib.request
import base64

TOOL = {
    "name": "spotify",
    "description": "Controla la reproducción de Spotify: play, pause, siguiente, anterior, buscar y reproducir música",
    "parameters": {
        "accion": "string (play | pause | siguiente | anterior | buscar)",
        "query": "string (canción, artista o álbum a buscar y reproducir)",
    },
}

SPOTIFY_CLIENT_ID = os.environ.get("SPOTIFY_CLIENT_ID", "")
SPOTIFY_CLIENT_SECRET = os.environ.get("SPOTIFY_CLIENT_SECRET", "")
SPOTIFY_REFRESH_TOKEN = os.environ.get("SPOTIFY_REFRESH_TOKEN", "")


async def execute(accion: str = "", query: str = ""):
    if not SPOTIFY_CLIENT_ID or not SPOTIFY_REFRESH_TOKEN:
        return {
            "error": "Spotify no configurado.\n"
            "Configura las variables de entorno:\n"
            "  SPOTIFY_CLIENT_ID=tu_client_id\n"
            "  SPOTIFY_CLIENT_SECRET=tu_client_secret\n"
            "  SPOTIFY_REFRESH_TOKEN=tu_refresh_token\n\n"
            "Obtén las credenciales en: https://developer.spotify.com/dashboard"
        }

    token = _get_token()
    if not token:
        return {"error": "No se pudo autenticar con Spotify. Revisa tus credenciales."}

    if accion == "play":
        return _control(token, "PUT", "/v1/me/player/play")
    elif accion == "pause":
        return _control(token, "PUT", "/v1/me/player/pause")
    elif accion == "siguiente":
        return _control(token, "POST", "/v1/me/player/next")
    elif accion == "anterior":
        return _control(token, "POST", "/v1/me/player/previous")
    elif accion == "buscar":
        return _search_and_play(token, query)

    return {"error": f"Acción '{accion}' no soportada. Usa: play, pause, siguiente, anterior, buscar"}


def _get_token():
    try:
        auth = base64.b64encode(
            f"{SPOTIFY_CLIENT_ID}:{SPOTIFY_CLIENT_SECRET}".encode()
        ).decode()

        data = urllib.parse.urlencode({"grant_type": "refresh_token", "refresh_token": SPOTIFY_REFRESH_TOKEN}).encode()

        req = urllib.request.Request(
            "https://accounts.spotify.com/api/token",
            data=data,
            headers={"Authorization": f"Basic {auth}", "Content-Type": "application/x-www-form-urlencoded"},
        )

        with urllib.request.urlopen(req, timeout=5) as resp:
            return json.loads(resp.read()).get("access_token")
    except Exception:
        return None


def _control(token, method, path):
    try:
        req = urllib.request.Request(
            f"https://api.spotify.com{path}",
            headers={"Authorization": f"Bearer {token}"},
            method=method,
        )
        urllib.request.urlopen(req, timeout=5)
        accion = path.split("/")[-1]
        return {"ok": True, "mensaje": f"Spotify: {accion}"}
    except Exception as e:
        return {"error": f"No se pudo controlar Spotify. ¿Hay un dispositivo activo?"}


def _search_and_play(token, query):
    import urllib.parse

    if not query:
        return {"error": "¿Qué quieres escuchar?"}

    try:
        encoded = urllib.parse.quote(query)
        search_url = f"https://api.spotify.com/v1/search?q={encoded}&type=track&limit=1"

        req = urllib.request.Request(
            search_url,
            headers={"Authorization": f"Bearer {token}"},
        )
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read())

        tracks = data.get("tracks", {}).get("items", [])
        if not tracks:
            return {"error": f"No encontré '{query}' en Spotify"}

        track = tracks[0]
        uri = track["uri"]
        name = track["name"]
        artist = track["artists"][0]["name"]

        body = json.dumps({"uris": [uri]}).encode()
        req2 = urllib.request.Request(
            "https://api.spotify.com/v1/me/player/play",
            data=body,
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json",
            },
            method="PUT",
        )
        urllib.request.urlopen(req2, timeout=5)

        return {
            "ok": True,
            "mensaje": f"Reproduciendo '{name}' de {artist}",
            "cancion": name,
            "artista": artist,
        }

    except Exception as e:
        return {"error": f"Error al buscar en Spotify: {e}"}
