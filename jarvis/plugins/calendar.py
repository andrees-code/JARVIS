import os
from datetime import datetime, timedelta

TOOL = {
    "name": "calendar",
    "description": "Consulta y crea eventos en tu calendario CalDAV (Google Calendar, iCloud, Nextcloud)",
    "parameters": {
        "accion": "string (hoy | crear | buscar)",
        "titulo": "string (título del evento, solo para 'crear')",
        "fecha": "string (fecha y hora, ej: 'mañana 15:00', solo para 'crear')",
    },
}

CALDAV_URL = os.environ.get("CALDAV_URL", "")
CALDAV_USER = os.environ.get("CALDAV_USER", "")
CALDAV_PASS = os.environ.get("CALDAV_PASS", "")


async def execute(accion: str = "", titulo: str = "", fecha: str = ""):
    if not CALDAV_URL or not CALDAV_USER:
        return {
            "error": "Calendario no configurado.\n"
            "Configura las variables de entorno:\n"
            "  CALDAV_URL=https://tu-servidor/caldav/calendars/usuario/calendario\n"
            "  CALDAV_USER=tu_usuario\n"
            "  CALDAV_PASS=tu_contraseña_o_app_password\n\n"
            "Google Calendar: CALDAV_URL=https://apidata.googleusercontent.com/caldav/v2/tu_calendar_id/events\n"
            "iCloud: CALDAV_URL=https://caldav.icloud.com/... (usa app-specific password)"
        }

    client = _get_client()
    if not client:
        return {"error": "No se pudo conectar al servidor CalDAV"}

    if accion == "hoy":
        return _get_today_events(client)
    elif accion == "crear":
        return _create_event(client, titulo, fecha)
    elif accion == "buscar":
        return _search_events(client, titulo)

    return {"error": f"Acción '{accion}' no soportada"}


def _get_client():
    try:
        import caldav
        client = caldav.DAVClient(url=CALDAV_URL, username=CALDAV_USER, password=CALDAV_PASS)
        return client
    except Exception:
        return None


def _get_today_events(client):
    try:
        principal = client.principal()
        calendars = principal.calendars()

        if not calendars:
            return {"ok": True, "mensaje": "No se encontraron calendarios", "eventos": []}

        cal = calendars[0]
        today = datetime.now()
        start = today.replace(hour=0, minute=0, second=0)
        end = start + timedelta(days=1)

        events = cal.search(start=start, end=end, expand=True, sort_keys=("dtstart",))

        items = []
        for ev in events[:15]:
            name = str(ev.vobject_instance.vevent.summary.value)
            dtstart = str(ev.vobject_instance.vevent.dtstart.value)[:16]
            items.append(f"📅 {dtstart} — {name}")

        return {"ok": True, "eventos": items, "total": len(items), "fecha": today.strftime("%Y-%m-%d")}

    except Exception as e:
        return {"error": f"Error al consultar calendario: {e}"}


def _create_event(client, titulo, fecha):
    if not titulo:
        return {"error": "Necesito un título para el evento"}

    try:
        from caldav.elements import dav, cdav
        from datetime import datetime, timedelta
        import dateutil.parser
        import pytz

        start = _parse_fecha(fecha)
        if not start:
            start = datetime.now() + timedelta(hours=1)
        end = start + timedelta(hours=1)

        principal = client.principal()
        calendars = principal.calendars()

        if not calendars:
            return {"error": "No se encontró un calendario donde crear el evento"}

        cal = calendars[0]
        cal.save_event(
            dtstart=start,
            dtend=end,
            summary=titulo,
        )

        return {"ok": True, "mensaje": f"Evento '{titulo}' creado el {start.strftime('%d/%m %H:%M')}"}

    except Exception as e:
        return {"error": f"Error al crear evento: {e}"}


def _search_events(client, query):
    try:
        principal = client.principal()
        calendars = principal.calendars()

        if not calendars:
            return {"ok": True, "mensaje": "No se encontraron calendarios", "eventos": []}

        cal = calendars[0]
        today = datetime.now()
        end = today + timedelta(days=30)

        events = cal.search(start=today, end=end, expand=True, sort_keys=("dtstart",))

        items = []
        for ev in events:
            name = str(ev.vobject_instance.vevent.summary.value).lower()
            if query.lower() in name:
                dtstart = str(ev.vobject_instance.vevent.dtstart.value)[:16]
                items.append(f"📅 {dtstart} — {ev.vobject_instance.vevent.summary.value}")

        if not items:
            return {"ok": True, "mensaje": f"No hay eventos con '{query}' en los próximos 30 días", "eventos": []}

        return {"ok": True, "eventos": items[:10], "total": len(items)}

    except Exception as e:
        return {"error": f"Error al buscar: {e}"}


def _parse_fecha(texto):
    try:
        import dateutil.parser
        now = datetime.now()
        texto = texto.lower().replace("mañana", f"{now.day + 1}").replace("pasado mañana", f"{now.day + 2}")
        return dateutil.parser.parse(texto, fuzzy=True)
    except Exception:
        return None
