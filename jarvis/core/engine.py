import asyncio
import threading
from core.voice_listener import VoiceListener
from core.brain import Brain
from core.speaker import Speaker
from core.plugin_registry import PluginRegistry
from core.memory import Memory
from core.overlay import Overlay


class Jarvis:
    def __init__(self, show_overlay=True, hotkey=False):
        self.listener = VoiceListener()
        self.memory = Memory()
        self.brain = Brain(memory=self.memory)
        self.speaker = Speaker()
        self.plugins = PluginRegistry()
        self.overlay = Overlay() if show_overlay else None
        self._hotkey_enabled = hotkey
        self._hotkey_queue = asyncio.Queue()

    async def run(self):
        print("=" * 50)
        print("  J.A.R.V.I.S — Just A Rather Very Intelligent System")
        print("=" * 50)

        all_tools = self.plugins.auto_discover()
        tool_count = len(all_tools)

        if self.overlay:
            self.overlay.start()

        if self._hotkey_enabled:
            self._start_hotkey()

        if self.listener.voice_enabled:
            print(f"\n[+] Escuchando wake word: '{self.listener.wake_word}'...")
            print(f"[+] Modelo: llama3.2:3b  |  Whisper: tiny  |  Plugins: {tool_count}")
            self.listener.start()
        else:
            print(f"\n[!] Modo texto (sin Picovoice key)")
            print(f"[+] Modelo: llama3.2:3b  |  Plugins: {tool_count}")
            print("[+] Escribe tu mensaje y presiona Enter")

        if self._hotkey_enabled:
            print("[+] Hotkey: Ctrl+J para activar sin wake word")

        if all_tools:
            print(f"[+] Herramientas: {', '.join(t['name'] for t in all_tools)}")
        print(f"[+] Memoria: {self.memory.count()} turnos guardados")
        if self.overlay:
            print("[+] Overlay HUD activo")

        print("-" * 50)

        self._set_status("escuchando")

        while True:
            try:
                text = await self._get_input()

                if text.lower() in ("salir", "exit", "adiós", "adios"):
                    self.memory.save("user", text)
                    await self.speaker.say("Hasta luego")
                    break

                print(f"\n[Tú] {text}")
                self.memory.save("user", text)

                memory_context = self.memory.get_context(n=10)

                self._set_status("pensando")
                relevant_plugins, relevant_tools = self.plugins.relevant_for(text)
                decision = await self.brain.decide(text, relevant_tools, memory_context)

                if decision.get("direct"):
                    response = decision["text"]
                else:
                    tool_call = decision["tool_call"]
                    print(f"[>] Ejecutando: {tool_call['name']}({tool_call['parameters']})")
                    self._set_tool(tool_call["name"], tool_call["parameters"])
                    result = await self.plugins.execute(tool_call)
                    print(f"[<] Resultado: {result}")
                    response = await self.brain.respond(result)

                print(f"[JARVIS] {response}")
                self.memory.save("assistant", response)
                self._show_response(response)

                self._set_status("hablando")
                await self.speaker.say(response)
                self._set_status("escuchando")

            except KeyboardInterrupt:
                print("\n[!] Apagando JARVIS...")
                break
            except Exception as e:
                print(f"\n[!] Error: {e}")
                self._set_status("error")
                continue

        self.listener.stop()
        if self.overlay:
            self.overlay.stop()
        print(f"[+] JARVIS apagado. {self.memory.count()} turnos en memoria.")

    async def _get_input(self):
        if self._hotkey_enabled:
            queue_task = asyncio.create_task(self._hotkey_queue.get())
            listener_task = asyncio.create_task(self.listener.listen())
            done, pending = await asyncio.wait(
                [queue_task, listener_task],
                return_when=asyncio.FIRST_COMPLETED,
            )
            for task in pending:
                task.cancel()
            return done.pop().result()
        return await self.listener.listen()

    def _start_hotkey(self):
        def on_activate():
            try:
                loop = asyncio.get_event_loop()
                loop.call_soon_threadsafe(
                    lambda: asyncio.ensure_future(
                        self._on_hotkey()
                    )
                )
            except Exception:
                pass

        async def listen_for_hotkey():
            from pynput import keyboard
            listener = keyboard.GlobalHotKeys({"<ctrl>+j": on_activate})
            listener.start()
            while self.listener._running or not self._hotkey_queue.empty:
                await asyncio.sleep(0.5)
            listener.stop()

        threading.Thread(target=lambda: asyncio.run(listen_for_hotkey()), daemon=True).start()

    async def _on_hotkey(self):
        if self.listener.voice_enabled:
            return
        await self._hotkey_queue.put("hotkey")

    def _set_status(self, status):
        if self.overlay:
            self.overlay.update_status(status)

    def _show_response(self, text):
        if self.overlay:
            self.overlay.show_response(text)

    def _set_tool(self, name, params):
        if self.overlay:
            self.overlay.show_tool(name, params)
