from playwright.sync_api import sync_playwright

import config
from core.session import Session


_LAUNCHERS = {
    "chromium": lambda pw: pw.chromium,
    "firefox": lambda pw: pw.firefox,
    "webkit": lambda pw: pw.webkit,
}


class Browser:
    """Playwright browser lifecycle.

    `authenticated` is True when a saved session still lands on the app
    (not the login page). Callers should inject a login flow when it is False.
    """

    def __init__(self):
        self.playwright = None
        self.browser = None
        self.context = None
        self.page = None
        self.authenticated = False

    def start(self):
        self.playwright = sync_playwright().start()

        launcher = _LAUNCHERS.get(config.BROWSER)
        if launcher is None:
            raise ValueError(
                f"Unsupported browser: {config.BROWSER!r}. "
                f"Choose one of: {', '.join(_LAUNCHERS)}"
            )

        self.browser = launcher(self.playwright).launch(
            headless=config.HEADLESS,
            slow_mo=config.SLOW_MO,
        )

        self.authenticated = False

        if Session.exists():
            print("Loading existing session...")
            self.context = self.browser.new_context(
                storage_state=Session.file()
            )
            self.page = self.context.new_page()
            self.page.set_default_timeout(config.TIMEOUT)

            print("Opening application...")
            self.page.goto(config.BASE_URL)
            self.page.wait_for_load_state("networkidle")

            if self._is_login_page():
                print("Session expired. Clearing session and starting fresh.")
                Session.delete()
                self.context.close()
                self.context = self.browser.new_context()
                self.page = self.context.new_page()
                self.page.set_default_timeout(config.TIMEOUT)
                self.authenticated = False
            else:
                print("Session is valid.")
                self.authenticated = True
        else:
            print("No session found. Starting fresh...")
            self.context = self.browser.new_context()
            self.page = self.context.new_page()
            self.page.set_default_timeout(config.TIMEOUT)
            self.authenticated = False

    def _is_login_page(self) -> bool:
        """True when the current page is the login screen (session unusable)."""
        url = (self.page.url or "").lower()
        if "login" in url or "signin" in url or "sign-in" in url:
            return True

        # Fallback: login form controls visible on the page
        try:
            if self.page.get_by_role("button", name="Login").count() > 0:
                return True
        except Exception:
            pass

        return False

    def stop(self):
        if self.context:
            self.context.close()
        if self.browser:
            self.browser.close()
        if self.playwright:
            self.playwright.stop()
