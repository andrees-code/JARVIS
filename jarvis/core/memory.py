import sqlite3
import time
from pathlib import Path
from config import PROJECT_ROOT


class Memory:
    def __init__(self, db_path=None):
        db_path = db_path or PROJECT_ROOT / "jarvis.db"
        self._db_path = Path(db_path)
        self._conn = sqlite3.connect(str(self._db_path), check_same_thread=False)
        self._init_db()

    def _init_db(self):
        self._conn.execute("""
            CREATE TABLE IF NOT EXISTS history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                role TEXT NOT NULL,
                content TEXT NOT NULL,
                ts REAL NOT NULL
            )
        """)
        self._conn.commit()

    def save(self, role, content):
        self._conn.execute(
            "INSERT INTO history (role, content, ts) VALUES (?, ?, ?)",
            (role, content, time.time()),
        )
        self._conn.commit()
        self._trim()

    def _trim(self, keep=40):
        self._conn.execute("""
            DELETE FROM history WHERE id NOT IN (
                SELECT id FROM history ORDER BY ts DESC LIMIT ?
            )
        """, (keep,))

    def get_recent(self, n=20):
        rows = self._conn.execute(
            "SELECT role, content FROM history ORDER BY ts DESC LIMIT ?",
            (n,),
        ).fetchall()
        return list(reversed(rows))

    def get_context(self, n=10):
        rows = self.get_recent(n)
        if not rows:
            return ""
        lines = []
        for role, content in rows:
            name = "Usuario" if role == "user" else "JARVIS"
            lines.append(f"{name}: {content}")
        return "\n".join(lines)

    def clear(self):
        self._conn.execute("DELETE FROM history")
        self._conn.commit()

    def count(self):
        return self._conn.execute(
            "SELECT COUNT(*) FROM history"
        ).fetchone()[0]
