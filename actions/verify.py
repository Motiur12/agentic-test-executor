from .base import BaseAction
from core.locator import Locator


class VerifyAction(BaseAction):

    def execute(
        self,
        page,
        verify_type=None,
        target=None,
        value=None,
        **kwargs
    ):

        if verify_type == "url_contains":

            if value not in page.url:

                raise Exception(
                    f"Expected URL to contain '{value}'\n"
                    f"Actual URL: {page.url}"
                )

            print(f"✓ URL Verified '{value}'")

            return

        # Default = verify visible element/text
        locator = Locator(page).find(target)

        if locator is None:

            raise Exception(
                f"Verification failed: {target}"
            )

        locator.wait_for()

        print(f"✓ Verified '{target}'")
