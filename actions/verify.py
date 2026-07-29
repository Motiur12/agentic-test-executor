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

        locator = Locator(page).find(target)

        if locator is None:
            locator = page.get_by_text(target, exact=False).first

        try:
            locator.wait_for(state="visible")
        except Exception as exc:
            raise Exception(f"Verification failed: {target}") from exc

        print(f"✓ Verified '{target}'")
