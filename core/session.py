import json
from pathlib import Path

import config

SESSION_FILE = config.SESSION_DIR / "storage_state.json"


class Session:

    @staticmethod
    def exists():
        if not SESSION_FILE.is_file():
            return False

        try:
            with SESSION_FILE.open(encoding="utf-8") as f:
                json.load(f)
            return True
        except Exception:
            return False

    @staticmethod
    def file():
        return str(SESSION_FILE)

    @staticmethod
    def save(page):
        SESSION_FILE.parent.mkdir(parents=True, exist_ok=True)
        page.context.storage_state(path=str(SESSION_FILE))
        print("✓ Session saved")

    @staticmethod
    def delete():
        if SESSION_FILE.is_file():
            SESSION_FILE.unlink()
            print("✓ Session deleted")
