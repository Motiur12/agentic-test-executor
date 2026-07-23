from playwright.sync_api import TimeoutError

from .base import BaseAction
from core.locator import Locator


class ClickAction(BaseAction):

    def execute(
        self,
        page,
        target=None,
        wait_for_navigation=False,
        **kwargs
    ):

        locator = Locator(page).find(target)

        if locator is None:
            raise Exception(
                f"Could not find clickable element: {target}"
            )

        old_url = page.url

        locator.click()

        if wait_for_navigation:

            try:

                page.wait_for_function(
                    "(old) => window.location.href !== old",
                    arg=old_url,
                    timeout=5000
                )

            except TimeoutError:

                raise Exception(
                    f"Navigation did not occur after clicking '{target}'"
                )

        print(f"✓ Clicked '{target}'")
