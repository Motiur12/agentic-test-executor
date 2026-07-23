from playwright.sync_api import Page
from .base import BaseAction
from core.locator import Locator


class EnterNumberAction(BaseAction):

    def execute(self, page: Page, target=None, value=None, **kwargs):

        Locator(page).enter_number(target, value)

        print(f"✓ Typed '{target}'")
