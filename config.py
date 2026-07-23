from pathlib import Path

# ======================================================
# PROJECT
# ======================================================

PROJECT_ROOT = Path(__file__).parent

SCREENSHOT_DIR = PROJECT_ROOT / "screenshots"
REPORT_DIR = PROJECT_ROOT / "reports"
TESTCASE_DIR = PROJECT_ROOT / "testcases"

# ======================================================
# PLAYWRIGHT
# ======================================================

BROWSER = "chromium"        # chromium | chrome | msedge | firefox
HEADLESS = False
SLOW_MO = 300
TIMEOUT = 30000

# ======================================================
# APPLICATION
# ======================================================

BASE_URL = ""

USERNAME = ""
PASSWORD = ""

# ======================================================
# AI (OLLAMA)
# ======================================================

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL = "qwen2.5:7b"

TEMPERATURE = 0

# ======================================================
# EXECUTION
# ======================================================

MAX_RETRY = 2
TAKE_SCREENSHOT_ON_FAILURE = True

# ======================================================
# REPORT
# ======================================================

SAVE_SCREENSHOTS = True
SAVE_LOGS = True

BASE_URL = "https://pre-prod-admin.cartup.com"