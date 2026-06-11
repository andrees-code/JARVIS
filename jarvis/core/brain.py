import json
import ollama
from config import OLLAMA_MODEL


SYSTEM_PROMPT = (
    "Eres JARVIS, un asistente de voz personal. "
    "Responde en español, de forma concisa y útil. "
    "Máximo 2-3 frases por respuesta. "
    "Sé natural y directo, como un asistente de confianza."
)

TOOL_SYSTEM = """Eres un asistente que decide si usar herramientas. Tienes acceso a estas herramientas:

{tools}

REGLAS:
1. Si el usuario pide algo que una herramienta puede hacer, responde SOLO con JSON.
2. Si el usuario solo habla/saluda/pregunta algo general, responde en texto normal.
3. El JSON debe ser EXACTAMENTE: {{"tool": "nombre", "parameters": {{"clave": "valor"}}}}

EJEMPLOS:
Usuario: "abre Safari"
Respuesta: {{"tool": "system", "parameters": {{"action": "abrir_app", "target": "Safari"}}}}

Usuario: "hola cómo estás"
Respuesta: ¡Hola! Estoy bien, gracias. ¿En qué puedo ayudarte?"""

TOOL_USER = 'Usuario: "{text}"\nRespuesta:'


class Brain:
    def __init__(self, model=None, memory=None):
        self.model = model or OLLAMA_MODEL
        self._memory = memory
        self._history = []

    def _build_system(self, memory_context=""):
        prompt = SYSTEM_PROMPT
        if memory_context:
            prompt += f"\n\nConversación anterior:\n{memory_context}"
        return prompt

    async def chat(self, text, memory_context=""):
        system = self._build_system(memory_context)
        messages = [{"role": "system", "content": system}]
        messages.extend(self._history)
        messages.append({"role": "user", "content": text})

        if len(messages) > 22:
            messages = [messages[0]] + messages[-21:]

        response = await self._call_ollama(messages)
        self._history.append({"role": "user", "content": text})
        self._history.append({"role": "assistant", "content": response})
        return response

    async def decide(self, text, tools, memory_context=""):
        if not tools:
            return {"direct": True, "text": await self.chat(text, memory_context)}

        tools_desc = self._format_tools(tools)
        system = TOOL_SYSTEM.format(tools=tools_desc)

        if memory_context:
            system += f"\n\nContexto de conversación anterior:\n{memory_context}"

        user = TOOL_USER.format(text=text)

        messages = [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ]

        raw = await self._call_ollama(messages)

        tool_call = self._parse_tool_call(raw)

        if tool_call:
            return {"direct": False, "tool_call": tool_call}
        else:
            return {"direct": True, "text": raw}

    async def respond(self, result):
        prompt = f"El resultado de la herramienta fue: {json.dumps(result, ensure_ascii=False)}. Resume esto para el usuario en español, en 1-2 frases."
        messages = [
            {"role": "system", "content": "Resume resultados de herramientas en español, natural y breve."},
            {"role": "user", "content": prompt},
        ]
        response = await self._call_ollama(messages)
        self._history.append({"role": "assistant", "content": response})
        return response

    def _format_tools(self, tools):
        lines = []
        for t in tools:
            params = json.dumps(t.get("parameters", {}), ensure_ascii=False)
            lines.append(f"- {t['name']}: {t['description']} (parámetros: {params})")
        return "\n".join(lines)

    def _parse_tool_call(self, text):
        text = text.strip()
        try:
            data = json.loads(text)
            if "tool" in data and "parameters" in data:
                return {"name": data["tool"], "parameters": data["parameters"]}
        except json.JSONDecodeError:
            if text.startswith("{") and '"tool"' in text:
                start = text.find("{")
                end = text.rfind("}") + 1
                try:
                    data = json.loads(text[start:end])
                    if "tool" in data and "parameters" in data:
                        return {"name": data["tool"], "parameters": data["parameters"]}
                except json.JSONDecodeError:
                    pass
        return None

    async def _call_ollama(self, messages):
        client = ollama.AsyncClient()
        full = ""
        async for chunk in await client.chat(
            model=self.model,
            messages=messages,
            stream=True,
        ):
            if "message" in chunk and "content" in chunk["message"]:
                full += chunk["message"]["content"]
        return full.strip()
