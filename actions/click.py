from playwright.sync_api import Page, TimeoutError
from .base import BaseAction


class ClickAction(BaseAction):

    def execute(self, page: Page, target=None, **kwargs):

        strategies = [

            lambda: page.get_by_role("button", name=target),

            lambda: page.get_by_role("link", name=target),

            lambda: page.get_by_label(target),

            lambda: page.get_by_text(target, exact=True),

            lambda: page.get_by_text(target),

        ]

        for strategy in strategies:

            try:

                locator = strategy()

                if locator.count() > 0:

                    locator.first.scroll_into_view_if_needed()
                    locator.first.click(timeout=3000)

                    print(f"✓ Clicked '{target}'")
                    return

            except TimeoutError:
                continue

            except Exception:
                continue

        raise Exception(f"Could not find clickable element: {target}")