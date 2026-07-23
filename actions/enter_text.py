from playwright.sync_api import Page
from .base import BaseAction
from core.locator import Locator


class EnterTextAction(BaseAction):

    def execute(self, page: Page, target=None, value=None, **kwargs):

        if target == "OTP":

            for i, digit in enumerate(value, start=1):

                page.get_by_label(
                    f"Please enter OTP character {i}"
                ).fill(digit)

            print("✓ Filled OTP")

            return

        locator = Locator(page).find(target)

        if locator is None:

            raise Exception(
                f"Could not find input: {target}"
            )

        locator.fill(value)

        print(f"✓ Filled '{target}'")
