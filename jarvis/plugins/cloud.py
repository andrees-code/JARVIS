TOOL = {
    "name": "cloud",
    "description": "Operaciones con Google Drive: subir archivos, listar recientes, descargar por nombre",
    "parameters": {
        "action": "string (subir | listar | descargar)",
        "ruta": "string (ruta local del archivo para subir/descargar)",
        "nombre": "string (nombre del archivo en Drive para descargar)",
    },
}


async def execute(action: str = "", ruta: str = "", nombre: str = ""):
    service = _get_service()

    if not service:
        return {
            "error": "Google Drive no está configurado. Coloca credentials.json en config/ y ejecuta 'python plugins/cloud.py --auth'"
        }

    if action == "listar":
        return _list_files(service)

    elif action == "subir":
        return _upload_file(service, ruta)

    elif action == "descargar":
        return _download_file(service, nombre, ruta)

    return {"error": f"Acción '{action}' no soportada. Usa: listar, subir, descargar"}


def _get_service():
    try:
        from google.oauth2.service_account import Credentials
        from googleapiclient.discovery import build
        from config import PROJECT_ROOT
        from pathlib import Path

        creds_path = Path(PROJECT_ROOT) / "config" / "credentials.json"
        if not creds_path.exists():
            return None

        creds = Credentials.from_service_account_file(
            str(creds_path),
            scopes=["https://www.googleapis.com/auth/drive.file"],
        )
        return build("drive", "v3", credentials=creds)

    except Exception:
        return None


def _list_files(service):
    try:
        results = (
            service.files()
            .list(pageSize=10, fields="files(name, id, modifiedTime)")
            .execute()
        )
        files = results.get("files", [])

        if not files:
            return {"ok": True, "mensaje": "No hay archivos en Drive", "items": []}

        items = []
        for f in files:
            items.append(f"📄 {f['name']} (id: {f['id'][:12]}...)")

        return {"ok": True, "items": items, "total": len(items)}

    except Exception as e:
        return {"error": str(e)}


def _upload_file(service, ruta):
    from pathlib import Path
    from googleapiclient.http import MediaFileUpload

    path = Path(ruta).expanduser().resolve()
    if not path.exists():
        return {"error": f"Archivo no encontrado: {ruta}"}

    try:
        file_metadata = {"name": path.name}
        media = MediaFileUpload(str(path), resumable=True)
        uploaded = (
            service.files()
            .create(body=file_metadata, media_body=media, fields="id,name")
            .execute()
        )
        return {
            "ok": True,
            "mensaje": f"'{path.name}' subido a Drive",
            "id": uploaded.get("id"),
        }
    except Exception as e:
        return {"error": str(e)}


def _download_file(service, nombre, ruta):
    from pathlib import Path
    import io
    from googleapiclient.http import MediaIoBaseDownload

    try:
        results = (
            service.files()
            .list(q=f"name='{nombre}'", pageSize=1, fields="files(id, name)")
            .execute()
        )
        files = results.get("files", [])

        if not files:
            return {"error": f"No encontré '{nombre}' en Drive"}

        file_id = files[0]["id"]
        dest = Path(ruta).expanduser().resolve() if ruta else Path.home() / "Downloads" / nombre
        dest.parent.mkdir(parents=True, exist_ok=True)

        request = service.files().get_media(fileId=file_id)
        with io.FileIO(str(dest), "wb") as fh:
            downloader = MediaIoBaseDownload(fh, request)
            done = False
            while not done:
                _, done = downloader.next_chunk()

        return {
            "ok": True,
            "mensaje": f"'{nombre}' descargado a {dest.name}",
            "ruta": str(dest),
        }
    except Exception as e:
        return {"error": str(e)}


if __name__ == "__main__":
    print("Google Drive plugin para JARVIS")
    print()
    print("Configuración:")
    print("1. Ve a https://console.cloud.google.com")
    print("2. Crea un proyecto → APIs y servicios → Drive API → Habilitar")
    print("3. Credenciales → Crear credenciales → Cuenta de servicio")
    print("4. Descarga el JSON y guárdalo como config/credentials.json")
    print()
    print("La cuenta de servicio es la opción más simple (sin OAuth interactivo).")
