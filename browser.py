from playwright.sync_api import sync_playwright
import config
from core.session import Session
from config import BASE_URL


class Browser:

    def __init__(self):

        self.playwright = None
        self.browser = None
        self.context = None
        self.page = None

    def start(self):

        self.playwright = sync_playwright().start()

        if config.BROWSER == "chromium":
            self.browser = self.playwright.chromium.launch(
                headless=config.HEADLESS,
                slow_mo=config.SLOW_MO
            )

        elif config.BROWSER == "firefox":
            self.browser = self.playwright.firefox.launch(
                headless=config.HEADLESS,
                slow_mo=config.SLOW_MO
            )

        elif config.BROWSER == "webkit":
            self.browser = self.playwright.webkit.launch(
                headless=config.HEADLESS,
                slow_mo=config.SLOW_MO
            )

        else:
            raise Exception(f"Unsupported browser: {config.BROWSER}")

        if Session.exists():

            print("Loading existing session...")

            self.context = self.browser.new_context(
                storage_state=Session.file()
            )

        else:

            print("No session found. Starting fresh...")

            self.context = self.browser.new_context()

        self.page = self.context.new_page()

        # If a session exists, open the application
        if Session.exists():

            print("Opening application...")

            self.page.goto(BASE_URL)

            if "login" in self.page.url.lower():

                print("Session expired.")

                Session.delete()

            self.page.wait_for_load_state("networkidle")

        self.page.set_default_timeout(config.TIMEOUT)

    def stop(self):

        if self.context:
            self.context.close()

        if self.browser:
            self.browser.close()

        if self.playwright:
            self.playwright.stop()