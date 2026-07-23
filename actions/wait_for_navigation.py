from playwright.sync_api import TimeoutError

from .base import BaseAction


class WaitForNavigationAction(BaseAction):

    def execute(
        self,
        page,
        timeout=5000,
        url_contains=None,
        **kwargs
    ):

        try:

            if url_contains:

                page.wait_for_url(
                    f"**{url_contains}**",
                    timeout=int(timeout)
                )

            else:

                page.wait_for_load_state(
                    "networkidle",
                    timeout=int(timeout)
                )

            print("✓ Navigation completed")

        except TimeoutError:

            raise Exception(
                "Navigation timeout"
            )