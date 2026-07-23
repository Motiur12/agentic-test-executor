from abc import ABC, abstractmethod
from playwright.sync_api import Page


class BaseAction(ABC):

    @abstractmethod
    def execute(self, page: Page, **kwargs):
        """
        Execute the action.
        """
        pass