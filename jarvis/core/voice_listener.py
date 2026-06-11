import asyncio
import threading
import numpy as np
import sounddevice as sd
from config import PICOVOICE_ACCESS_KEY, WAKE_WORD, WHISPER_MODEL, SAMPLE_RATE, LISTEN_TIMEOUT


class VoiceListener:
    def __init__(self, access_key=None, wake_word=None, whisper_model=None):
        self.access_key = access_key or PICOVOICE_ACCESS_KEY
        self.wake_word = wake_word or WAKE_WORD
        self.whisper_model = whisper_model or WHISPER_MODEL

        self._text_queue = asyncio.Queue()
        self._running = False
        self._thread = None
        self._whisper = None
        self._porcupine = None

        self.voice_enabled = bool(self.access_key)

    def _load_models(self):
        import whisper
        import pvporcupine

        self._whisper = whisper.load_model(self.whisper_model)
        self._porcupine = pvporcupine.create(
            access_key=self.access_key,
            keywords=[self.wake_word]
        )

    def _run_loop(self):
        self._load_models()

        frame_length = self._porcupine.frame_length
        sample_rate = self._porcupine.sample_rate
        audio_buffer = []
        recording = False
        silence_frames = 0
        max_silence = int(1.5 * sample_rate / frame_length)

        def callback(indata, frames, time_info, status):
            nonlocal recording, silence_frames

            pcm = indata[:, 0].astype(np.int16)

            if recording:
                audio_buffer.append(pcm.copy())
                if np.abs(pcm).mean() < 80:
                    silence_frames += 1
                else:
                    silence_frames = 0
                return

            if self._porcupine.process(pcm.tobytes()) >= 0:
                recording = True
                audio_buffer.clear()
                audio_buffer.append(pcm.copy())
                silence_frames = 0

        with sd.InputStream(
            samplerate=sample_rate,
            channels=1,
            dtype=np.int16,
            callback=callback,
            blocksize=frame_length,
        ):
            while self._running:
                sd.sleep(100)
                if recording and silence_frames >= max_silence:
                    recording = False
                    silence_frames = 0
                    if audio_buffer:
                        audio = np.concatenate(audio_buffer)
                        text = self._transcribe(audio, sample_rate)
                        if text.strip():
                            asyncio.run_coroutine_threadsafe(
                                self._text_queue.put(text),
                                asyncio.get_event_loop(),
                            )

    def _transcribe(self, audio, sample_rate):
        audio_float = audio.astype(np.float32) / 32768.0
        result = self._whisper.transcribe(audio_float, language="es")
        return result["text"].strip()

    def start(self):
        if not self.voice_enabled:
            return
        self._running = True
        self._thread = threading.Thread(target=self._run_loop, daemon=True)
        self._thread.start()

    def stop(self):
        self._running = False

    async def listen(self):
        if self.voice_enabled and not self._thread:
            self.start()
        if self.voice_enabled:
            return await self._text_queue.get()
        return await asyncio.get_event_loop().run_in_executor(
            None, lambda: input("\n[Tú] >>> ")
        )
