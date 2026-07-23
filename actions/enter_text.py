from playwright.sync_api import Page
from .base import BaseAction


class EnterTextAction(BaseAction):

    def execute(self, page: Page, target=None, value=None, **kwargs):

        if target == "OTP":

            for i, digit in enumerate(value, start=1):

                page.get_by_label(
                    f"Please enter OTP character {i}"
                ).fill(digit)

            print("✓ Filled OTP")

            return

        strategies = [

            lambda: page.get_by_label(target),

            lambda: page.get_by_placeholder(target),

            lambda: page.get_by_role("textbox", name=target),

            lambda: page.locator(f'input[name="{target}"]'),

            lambda: page.locator(f'input[id="{target}"]'),

        ]

        for strategy in strategies:

            try:

                locator = strategy()

                if locator.count() > 0:

                    locator.first.fill(value)

                    print(f"✓ Filled '{target}'")

                    return

            except Exception:
                continue

        raise Exception(f"Could not find input field: {target}")