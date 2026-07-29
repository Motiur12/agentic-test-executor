from playwright.sync_api import Page

from .base import BaseAction


class GotoAction(BaseAction):

    def execute(self, page: Page, url=None, **kwargs):
        if not url:
            raise Exception("URL is required for goto.")

        print(f"Opening: {url}")
        page.goto(url)
        page.wait_for_load_state("networkidle")
        print(f"✓ Opened '{url}'")
