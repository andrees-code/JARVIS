import asyncio
import argparse
from core.engine import Jarvis


def main():
    parser = argparse.ArgumentParser(description="J.A.R.V.I.S — Asistente personal")
    parser.add_argument(
        "--no-overlay", action="store_true",
        help="Desactiva el overlay HUD flotante"
    )
    parser.add_argument(
        "--hotkey", action="store_true",
        help="Activa Ctrl+J como atajo para hablar sin wake word"
    )
    args = parser.parse_args()

    jarvis = Jarvis(
        show_overlay=not args.no_overlay,
        hotkey=args.hotkey,
    )
    asyncio.run(jarvis.run())


if __name__ == "__main__":
    main()
