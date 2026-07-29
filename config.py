from pathlib import Path

# ======================================================
# PROJECT
# ======================================================

PROJECT_ROOT = Path(__file__).resolve().parent

SCREENSHOT_DIR = PROJECT_ROOT / "screenshots"
REPORT_DIR = PROJECT_ROOT / "reports"
TESTCASE_DIR = PROJECT_ROOT / "testcases"
SESSION_DIR = PROJECT_ROOT / "session"

# ======================================================
# PLAYWRIGHT
# ======================================================

BROWSER = "chromium"  # chromium | firefox | webkit
HEADLESS = False
SLOW_MO = 300
TIMEOUT = 30_000

# ======================================================
# APPLICATION
# ======================================================

BASE_URL = "https://pre-prod-admin.cartup.com"

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
