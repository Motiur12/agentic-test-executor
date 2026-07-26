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

    # -------------------------
    # VERIFY
    # -------------------------

    def find(self, target: str):
        """Return the first element matching visible text or an accessible name."""
        target = self.normalize(target)

        if not target:
            return None

        strategies = [
            lambda: self.page.get_by_role(
                "heading",
                name=target,
                exact=False
            ),
            lambda: self.page.get_by_text(
                target,
                exact=False
            ),
            lambda: self.page.get_by_label(
                target,
                exact=False
            ),
            lambda: self.page.locator(f'text="{target}"'),
        ]

        for strategy in strategies:
            try:
                locator = strategy()

                if locator.count() > 0:
                    return locator.first

            except Exception:
                continue

        return None

    # -------------------------
    # CLICK
    # -------------------------

    def find_clickable(self, target: str):

        target = self.normalize(target)

        strategies = [

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

            lambda: self.page.get_by_label(
                target,
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

    # -------------------------
    # INPUT
    # -------------------------

    def find_input(self, target: str):

        target = self.normalize(target)

        camel = target.split()

        if camel:

            field_name = camel[0] + "".join(
                word.capitalize()
                for word in camel[1:]
            )

        else:

            field_name = ""

        strategies = [

            lambda: self.page.locator(
                f'input[name="{field_name}"]'
            ),

            lambda: self.page.locator(
                f'textarea[name="{field_name}"]'
            ),

            lambda: self.page.get_by_placeholder(
                f"Enter {target.title()}",
                exact=False
            ),

            lambda: self.page.get_by_label(
                target,
                exact=False
            ),

            lambda: self.page.get_by_role(
                "textbox",
                name=target,
                exact=False
            ),

            lambda: self.page.get_by_role(
                "spinbutton",
                name=target,
                exact=False
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

    # -------------------------
    # ENTER
    # -------------------------

    def enter(self, target, value):

        locator = self.find_input(target)

        if locator is None:

            raise Exception(
                f"Could not find input: {target}"
            )

        role = locator.get_attribute("role")

        if role == "spinbutton":

            locator.click()

            locator.press("Control+A")

            locator.press("Backspace")

            locator.type(str(value), delay=30)

            locator.press("Tab")

            return

        locator.fill(str(value))

    def enter_number(self, target, value):

        locator = self.find_input(target)

        if locator is None:
            raise Exception(f"Could not find input: {target}")

        locator.click()
        locator.press("Control+A")
        locator.press("Backspace")
        locator.type(str(value), delay=30)
        locator.press("Tab")
