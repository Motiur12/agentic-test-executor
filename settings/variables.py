import os
from pathlib import Path


ENV_FILE = Path(__file__).resolve().parents[1] / ".env"


def load_env_file(path=ENV_FILE):
    """Load local credentials without adding a third-party dependency."""
    if not path.is_file():
        return

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()

        if not line or line.startswith("#") or "=" not in line:
            continue

        key, value = (part.strip() for part in line.split("=", 1))

        if key not in {"CARTUP_USERNAME", "CARTUP_PASSWORD", "CARTUP_OTP"}:
            continue

        if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
            value = value[1:-1]

        os.environ.setdefault(key, value)


load_env_file()


# Shell environment variables take precedence over values from .env.
VARIABLES = {
    "USERNAME": os.getenv("CARTUP_USERNAME"),
    "PASSWORD": os.getenv("CARTUP_PASSWORD"),
    "OTP": os.getenv("CARTUP_OTP"),
}
