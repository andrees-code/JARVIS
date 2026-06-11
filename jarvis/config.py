import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent

PICOVOICE_ACCESS_KEY = os.environ.get("PICOVOICE_ACCESS_KEY", "")
WAKE_WORD = "jarvis"
OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", "llama3.2:3b")
WHISPER_MODEL = os.environ.get("WHISPER_MODEL", "tiny")
SAMPLE_RATE = 16000
LISTEN_TIMEOUT = 5
