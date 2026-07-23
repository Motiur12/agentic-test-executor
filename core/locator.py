from playwright.sync_api import Page


class Locator:

    def __init__(self, page: Page):
        self.page = page

    def normalize(self, target: str):

        words = [
            "button",
            "textbox",
            "text box",
            "input",
            "field",
            "link",
            "dropdown",
            "menu",
            "icon"
        ]

        target = target.lower()

        for word in words:
            target = target.replace(word, "")

        return " ".join(target.split())

    def find(self, target: str):

        target = self.normalize(target)

        strategies = [

            lambda: self.page.get_by_label(target, exact=False),

            lambda: self.page.get_by_label(target),

            lambda: self.page.get_by_placeholder(target),

            lambda: self.page.get_by_role(
                "button",
                name=target,
                exact=False
            ),

            lambda: self.page.get_by_role(
                "link",
                name=target,
                exact=False
            ),

            lambda: self.page.get_by_text(
                target,
                exact=False
            ),

            lambda: self.page.locator(
                f'text="{target}"'
            )

        ]

        for strategy in strategies:

            try:

                locator = strategy()

                if locator.count() > 0:

                    return locator.first

            except:
                pass

        return None