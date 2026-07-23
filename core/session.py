import json
import os

SESSION_FILE = "session/storage_state.json"


class Session:

    @staticmethod
    def exists():

        if not os.path.exists(SESSION_FILE):
            return False

        try:
            with open(SESSION_FILE, "r", encoding="utf-8") as f:
                json.load(f)

            return True

        except Exception:

            return False

    @staticmethod
    def file():

        return SESSION_FILE

    @staticmethod
    def save(page):

        page.context.storage_state(path=SESSION_FILE)

        print("✓ Session saved")

    @staticmethod
    def delete():

        if os.path.exists(SESSION_FILE):

            os.remove(SESSION_FILE)

            print("✓ Session deleted")
