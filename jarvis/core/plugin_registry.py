import importlib.util
import json
import time
from pathlib import Path
from config import PROJECT_ROOT


class PluginRegistry:
    def __init__(self, plugins_dir=None):
        self.plugins_dir = Path(plugins_dir or PROJECT_ROOT / "plugins")
        self._plugins = {}
        self._tools = []
        self._loaded = False
        self._collection = None
        self._embedder = None
        self._router_enabled = False

    def auto_discover(self):
        if self._loaded:
            return self._tools

        for file in sorted(self.plugins_dir.glob("*.py")):
            if file.name.startswith("_"):
                continue

            name = file.stem
            spec = importlib.util.spec_from_file_location(
                f"plugins.{name}", file
            )
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)

            if hasattr(mod, "TOOL") and hasattr(mod, "execute"):
                self._plugins[name] = mod
                self._tools.append(mod.TOOL)

        self._loaded = True
        self._init_router()
        return self._tools

    def _init_router(self):
        try:
            import chromadb
            from sentence_transformers import SentenceTransformer

            self._embedder = SentenceTransformer(
                "paraphrase-multilingual-MiniLM-L12-v2", device="cpu"
            )

            self._client = chromadb.Client(
                chromadb.config.Settings(
                    anonymized_telemetry=False,
                    is_persistent=False,
                )
            )

            self._collection = self._client.create_collection(
                name="jarvis_tools",
                metadata={"hnsw:space": "cosine"},
            )

            descs = [t["description"] for t in self._tools]
            ids = [t["name"] for t in self._tools]
            embeddings = self._embedder.encode(descs).tolist()

            self._collection.add(
                embeddings=embeddings,
                documents=descs,
                ids=ids,
            )

            self._router_enabled = True
            print(f"[+] Router semántico activo ({len(self._tools)} herramientas indexadas)")

        except Exception as e:
            print(f"[!] Router semántico no disponible: {e}")
            self._router_enabled = False

    def relevant_for(self, text, k=3):
        if not self._router_enabled or not self._collection:
            return list(self._plugins.values()), self._tools

        start = time.time()
        query_embedding = self._embedder.encode([text]).tolist()

        results = self._collection.query(
            query_embeddings=query_embedding,
            n_results=min(k, len(self._tools)),
        )

        elapsed = (time.time() - start) * 1000
        matched_names = results["ids"][0]
        matched_distances = results.get("distances", [[0]] * len(matched_names))[0]

        plugins = [self._plugins[name] for name in matched_names]
        tools = [
            t for t in self._tools if t["name"] in matched_names
        ]

        if matched_names:
            top_name = matched_names[0]
            top_dist = matched_distances[0] if matched_distances else 0
            print(f"[>] Semántica: '{top_name}' ({top_dist:.3f}) en {elapsed:.0f}ms")

        return plugins, tools

    def get_tools_json(self):
        return self._tools

    def has_tools(self):
        return len(self._tools) > 0

    async def execute(self, tool_call):
        name = tool_call.get("name", "")
        params = tool_call.get("parameters", {})

        if name not in self._plugins:
            return {"error": f"Plugin '{name}' no encontrado"}

        try:
            result = await self._plugins[name].execute(**params)
            return result
        except Exception as e:
            return {"error": str(e)}
