import threading
import customtkinter as ctk


class Overlay:
    def __init__(self):
        self._running = False
        self._thread = None
        self._app = None
        self._status_label = None
        self._text_label = None
        self._tool_label = None

    def start(self):
        if self._running:
            return
        self._running = True
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()

    def _run(self):
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self._app = ctk.CTk()
        self._app.title("JARVIS HUD")
        self._app.geometry("420x200+20+40")
        self._app.overrideredirect(True)
        self._app.attributes("-topmost", True)
        self._app.configure(fg_color="#0a0c10")

        self._app.attributes("-alpha", 0.88)

        top_bar = ctk.CTkFrame(self._app, fg_color="#0f1218", height=28)
        top_bar.pack(fill="x")
        title = ctk.CTkLabel(
            top_bar, text="J.A.R.V.I.S  HUD",
            font=ctk.CTkFont(family="Menlo", size=11),
            text_color="#00d4ff",
        )
        title.pack(side="left", padx=10, pady=4)

        close_btn = ctk.CTkButton(
            top_bar, text="×", width=24, height=24,
            fg_color="transparent", hover_color="#2a1015",
            text_color="#6a7a8a", font=ctk.CTkFont(size=14),
            command=self._app.quit,
        )
        close_btn.pack(side="right", padx=4, pady=2)

        self._status_label = ctk.CTkLabel(
            self._app,
            text="◉ INICIANDO",
            font=ctk.CTkFont(family="Menlo", size=12, weight="bold"),
            text_color="#00d4ff",
        )
        self._status_label.pack(pady=(12, 2))

        self._tool_label = ctk.CTkLabel(
            self._app,
            text="",
            font=ctk.CTkFont(family="Menlo", size=10),
            text_color="#4ade80",
        )
        self._tool_label.pack(pady=(0, 6))

        self._text_label = ctk.CTkLabel(
            self._app,
            text="",
            font=ctk.CTkFont(family="Menlo", size=12),
            text_color="#c8d4e0",
            wraplength=380,
            justify="left",
        )
        self._text_label.pack(padx=16, pady=(0, 10))

        self._app.protocol("WM_DELETE_WINDOW", self._app.quit)
        self._app.mainloop()
        self._running = False

    def update_status(self, status):
        if not self._app:
            return
        colors = {
            "escuchando": ("◉ ESCUCHANDO", "#00d4ff"),
            "pensando":   ("◉ PENSANDO",   "#fbbf24"),
            "hablando":   ("◉ HABLANDO",   "#4ade80"),
            "error":      ("◉ ERROR",      "#f87171"),
        }
        text, color = colors.get(status, ("◉ " + status.upper(), "#00d4ff"))
        self._app.after(0, lambda: self._status_label.configure(
            text=text, text_color=color
        ))

    def show_response(self, text):
        if not self._app:
            return
        display = text[:200] + ("..." if len(text) > 200 else "")
        self._app.after(0, lambda: self._text_label.configure(text=display))

    def show_tool(self, name, params):
        if not self._app:
            return
        display = f"⚡ {name}({params})"
        self._app.after(0, lambda: self._tool_label.configure(text=display))

    def stop(self):
        if self._app:
            self._app.after(0, self._app.quit)
        self._running = False
