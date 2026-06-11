import asyncio
import pyttsx3


class Speaker:
    def __init__(self):
        self._engine = None
        self._ready = False

    def _init_engine(self):
        if self._ready:
            return
        self._engine = pyttsx3.init()
        self._engine.setProperty("rate", 180)
        self._engine.setProperty("volume", 0.9)
        voices = self._engine.getProperty("voices")
        for v in voices:
            if "es" in v.id.lower() or "spanish" in v.name.lower():
                self._engine.setProperty("voice", v.id)
                break
        self._ready = True

    async def say(self, text):
        if not text.strip():
            return
        self._init_engine()
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, self._speak, text)

    def _speak(self, text):
        self._engine.say(text)
        self._engine.runAndWait()
