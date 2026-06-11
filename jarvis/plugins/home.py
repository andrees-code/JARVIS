import os
import json
import urllib.request
import urllib.error

TOOL = {
    "name": "home",
    "description": "Controla dispositivos de Home Assistant: luces, persianas, enchufes, clima del hogar",
    "parameters": {
        "accion": "string (encender | apagar | atenuar | estado | listar)",
        "entidad": "string (nombre o ID de la entidad, ej: luz_salon, persiana_dormitorio)",
        "valor": "string (para atenuar: brillo 0-100, o posición persiana 0-100)",
    },
}

HA_URL = os.environ.get("HA_URL", "")
HA_TOKEN = os.environ.get("HA_TOKEN", "")


async def execute(accion: str = "", entidad: str = "", valor: str = ""):
    if not HA_URL or not HA_TOKEN:
        return {
            "error": "Home Assistant no configurado.\n"
            "Configura las variables de entorno:\n"
            "  HA_URL=http://tu-ha:8123\n"
            "  HA_TOKEN=tu_long_lived_access_token\n\n"
            "El token se crea en: Perfil > Seguridad > Tokens de larga duración"
        }

    if accion in ("encender", "apagar"):
        return _toggle(entidad, accion)
    elif accion == "atenuar":
        return _dim(entidad, valor)
    elif accion == "estado":
        return _get_state(entidad)
    elif accion == "listar":
        return _list_devices()

    return {"error": f"Acción '{accion}' no soportada"}


def _toggle(entity, action):
    domain = _get_domain(entity)
    service = f"{domain}/turn_{'on' if action == 'encender' else 'off'}"
    return _call_service(service, {"entity_id": entity})


def _dim(entity, brightness):
    domain = _get_domain(entity)
    service = f"{domain}/turn_on"
    data = {"entity_id": entity}

    if "light" in domain:
        data["brightness_pct"] = int(brightness)
    elif "cover" in domain:
        data["position"] = int(brightness)

    return _call_service(service, data)


def _get_state(entity):
    data = _api_get(f"/api/states/{entity}")
    if data:
        return {
            "ok": True,
            "entidad": entity,
            "estado": data.get("state", "?"),
            "atributos": {
                k: v for k, v in data.get("attributes", {}).items()
                if k in ("friendly_name", "brightness", "current_position", "device_class", "unit_of_measurement")
            },
        }
    return {"error": f"Entidad '{entity}' no encontrada en Home Assistant"}


def _list_devices():
    data = _api_get("/api/states")
    if not data:
        return {"error": "No se pudieron obtener dispositivos"}

    items = []
    for s in data[:30]:
        name = s.get("attributes", {}).get("friendly_name", s["entity_id"])
        state = s.get("state", "?")
        items.append(f"  {name}: {state}")

    return {"ok": True, "items": items, "total": len(data)}


def _call_service(service, data):
    url = f"{HA_URL}/api/services/{service}"
    return _api_post(url, data)


def _api_get(path):
    try:
        req = urllib.request.Request(
            f"{HA_URL}{path}",
            headers={"Authorization": f"Bearer {HA_TOKEN}"},
        )
        with urllib.request.urlopen(req, timeout=5) as resp:
            return json.loads(resp.read())
    except Exception:
        return None


def _api_post(path, data):
    try:
        body = json.dumps(data).encode()
        req = urllib.request.Request(
            f"{HA_URL}{path}",
            data=body,
            headers={
                "Authorization": f"Bearer {HA_TOKEN}",
                "Content-Type": "application/json",
            },
        )
        with urllib.request.urlopen(req, timeout=5) as resp:
            result = json.loads(resp.read())
            return {"ok": True, "mensaje": "Comando enviado a Home Assistant", "resultado": result}
    except urllib.error.HTTPError as e:
        return {"error": f"Error HA: {e.code}"}
    except Exception as e:
        return {"error": f"No se pudo conectar a Home Assistant: {e}"}


def _get_domain(entity):
    return entity.split(".")[0] if "." in entity else "switch"
