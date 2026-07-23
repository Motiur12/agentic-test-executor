from playwright.sync_api import Page
from .base import BaseAction


class GotoAction(BaseAction):

    def execute(self, page: Page, url=None, **kwargs):

        print(f"Opening: {url}")

        page.goto(url)

        page.wait_for_load_state("networkidle")