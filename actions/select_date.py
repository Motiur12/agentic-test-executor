from playwright.sync_api import Page

from .base import BaseAction
from core.locator import Locator


class SelectDateAction(BaseAction):
    """Pick a date in a calendar-style date picker (e.g. PrimeReact Calendar).

    Opens the date field (by target label, or the first date field on the
    page if no specific target resolves), pages the calendar to the target
    month/year using the prev/next controls, then clicks the matching day.
    """

    def execute(self, page: Page, target=None, value=None, **kwargs):
        if value is None:
            raise Exception("Select Date value is required (expected YYYY-MM-DD).")

        Locator(page).select_date(target, value)
        print(f"✓ Selected date '{value}' in '{target}'")