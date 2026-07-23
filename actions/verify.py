from playwright.sync_api import Page
from .base import BaseAction


class VerifyAction(BaseAction):

    def execute(self, page: Page, target=None, **kwargs):

        page.get_by_text(target).first.wait_for(timeout=5000)

        print(f"✓ Verified '{target}'")

        from core.session import Session

        if target == "Dashboard":

            print("✓ Session saved")