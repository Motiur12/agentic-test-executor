from playwright.sync_api import Page

from .base import BaseAction
from core.locator import Locator


class SelectAction(BaseAction):
    """Select a value in a combobox / React Select control."""

    def execute(self, page: Page, target=None, value=None, **kwargs):
        if not target:
            raise Exception("Select target is required.")
        if value is None:
            raise Exception("Select value is required.")

        Locator(page).enter(target, value)
        print(f"✓ Selected '{value}' in '{target}'")
