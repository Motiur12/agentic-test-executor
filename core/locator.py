from playwright.sync_api import Page

class Locator:

    def __init__(self, page: Page):
        self.page = page

    def _roots(self):
        """Active dialog first (if one is open), then the whole page."""
        dialogs = self.page.get_by_role("dialog")

        if dialogs.count() > 0:
            return [dialogs.last, self.page]

        return [self.page]

    def _first(self, strategy):
        try:
            locator = strategy()

            count = locator.count()

            for i in range(count):
                candidate = locator.nth(i)

                if candidate.is_visible():
                    return candidate

        except Exception:
            pass

        return None

    def _first_scoped(self, build):
        """Try `build(root)` against each root (active dialog first, then
        the whole page), returning the first visible match."""
        for root in self._roots():
            locator = self._first(lambda: build(root))

            if locator:
                return locator

        return None

    def _last(self, strategy):
        """Like _first, but returns the innermost (last) visible match.
        Needed for broad selectors like `*` with has_text, where matches
        include every ancestor and the most specific element is last."""
        try:
            locator = strategy()

            count = locator.count()

            for i in range(count - 1, -1, -1):
                candidate = locator.nth(i)

                if candidate.is_visible():
                    return candidate

        except Exception:
            pass

        return None

    def _last_scoped(self, build):
        """Dialog-scoped version of _last."""
        for root in self._roots():
            locator = self._last(lambda: build(root))

            if locator:
                return locator

        return None

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
            lambda: self._first(lambda: self.page.get_by_test_id(target)),
            lambda: self._first_scoped(
                lambda root: root.get_by_role("heading", name=target, exact=True)
            ),
            lambda: self._first_scoped(
                lambda root: root.get_by_role("heading", name=target, exact=False)
            ),
            lambda: self._first_scoped(
                lambda root: root.get_by_text(target, exact=True)
            ),
            lambda: self._first_scoped(
                lambda root: root.get_by_text(target, exact=False)
            ),
            lambda: self._first(lambda: self.page.locator(f'[aria-label="{target}"]')),

            lambda: self._first(lambda: self.page.locator(f'[aria-label*="{target}" i]')),
            lambda: self._first_scoped(
                lambda root: root.get_by_label(target, exact=True)
            ),
            lambda: self._first_scoped(
                lambda root: root.get_by_label(target, exact=True)
            ),
            lambda: self._first_scoped(
                lambda root: root.get_by_label(target, exact=False)
            ),
            lambda: self._first_scoped(
                lambda root: root.get_by_placeholder(target, exact=True)
            ),
            lambda: self._first_scoped(
                lambda root: root.get_by_placeholder(target, exact=False)
            ),
            lambda: self._first_scoped(
                lambda root: root.get_by_text(target, exact=True)
            ),
            lambda: self._first_scoped(
                lambda root: root.get_by_text(target, exact=False)
            ),
            lambda: self._last_scoped(
                lambda root: root.locator("*").filter(has_text=target)
            ),
            lambda: self._first(lambda: self.page.locator(f'[title="{target}"]')),
            lambda: self._first(lambda: self.page.locator(f'[title*="{target}" i]')),
            lambda: self._first(lambda: self.page.locator(f'text="{target}"')),
        ]

        for strategy in strategies:
            locator = strategy()

            if locator:
                return locator

        return None

    # -------------------------
    # CLICK
    # -------------------------

    def find_clickable(self, target: str, timeout=5000):

        target = self.normalize(target)

        strategies = [

            lambda: self._first(lambda: self.page.get_by_test_id(target)),

            lambda: self._first_scoped(
                lambda root: root.get_by_role("button", name=target, exact=True)
            ),

            lambda: self._first_scoped(
                lambda root: root.get_by_role("button", name=target, exact=False)
            ),

            lambda: self._first_scoped(
                lambda root: root.get_by_role("link", name=target, exact=True)
            ),

            lambda: self._first_scoped(
                lambda root: root.get_by_role("link", name=target, exact=False)
            ),

            lambda: self._first_scoped(
                lambda root: root.get_by_label(target, exact=True)
            ),

            lambda: self._first_scoped(
                lambda root: root.get_by_label(target, exact=False)
            ),

            lambda: self._first_scoped(
                lambda root: root.get_by_text(target, exact=True)
            ),

            lambda: self._first_scoped(
                lambda root: root.get_by_text(target, exact=False)
            ),

            lambda: self._last_scoped(
                lambda root: root.locator("*").filter(has_text=target)
            ),

            lambda: self._first(lambda: self.page.locator(f'[title="{target}"]')),

            lambda: self._first(lambda: self.page.locator(f'[title*="{target}" i]')),

            lambda: self._first(lambda: self.page.locator(f'text="{target}"'))

        ]

        attempts = max(1, timeout // 250)

        for attempt in range(attempts):

            for strategy in strategies:
                locator = strategy()

                if locator:
                    return locator

            if attempt < attempts - 1:
                self.page.wait_for_timeout(250)

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

            lambda: self._first(lambda: self.page.get_by_test_id(target)),

            lambda: self._first(lambda: self.page.locator(f'[name="{target}"]')),

            lambda: self._first(lambda: self.page.locator(f'[name="{field_name}"]')),

            lambda: self._first(lambda: self.page.locator(f'input[name="{field_name}"]')),

            lambda: self._first(lambda: self.page.locator(f'textarea[name="{field_name}"]')),

            lambda: self._first_scoped(
                lambda root: root.get_by_placeholder(f"Enter {target.title()}", exact=False)
            ),

            lambda: self._first_scoped(
                lambda root: root.get_by_label(target, exact=True)
            ),

            lambda: self._first_scoped(
                lambda root: root.get_by_label(target, exact=False)
            ),

            lambda: self._first_scoped(
                lambda root: root.get_by_role("textbox", name=target, exact=True)
            ),

            lambda: self._first_scoped(
                lambda root: root.get_by_role("textbox", name=target, exact=False)
            ),

            lambda: self._first_scoped(
                lambda root: root.get_by_role("spinbutton", name=target, exact=True)
            ),

            lambda: self._first_scoped(
                lambda root: root.get_by_role("spinbutton", name=target, exact=False)
            ),

            lambda: self._first_scoped(
                lambda root: root.get_by_role("combobox", name=target, exact=True)
            ),

            lambda: self._first_scoped(
                lambda root: root.get_by_role("combobox", name=target, exact=False)
            ),

            lambda: self._first(
                lambda: self.page.locator(
                    f'label:text-is("{target.title()}") + div input[role="combobox"]'
                )
            ),

            lambda: self._first(lambda: self.page.locator(f'[title="{target}"]')),

            lambda: self._first(lambda: self.page.locator(f'[title*="{target}" i]'))

        ]

        for strategy in strategies:
            locator = strategy()

            if locator:
                return locator

        return None

    # -------------------------
    # COMBOBOX (React Select / MUI Autocomplete / AntD Select, etc.)
    # -------------------------

    def find_combobox(self, target: str):
        """Return the first visible combobox-style element matching target.

        Search order: Label -> Role=combobox -> aria-label -> Placeholder.
        """
        target = self.normalize(target)

        if not target:
            return None

        strategies = [
            lambda: self._first_scoped(
                lambda root: root.get_by_label(target, exact=True)
            ),
            lambda: self._first_scoped(
                lambda root: root.get_by_label(target, exact=False)
            ),
            lambda: self._first_scoped(
                lambda root: root.get_by_role("combobox", name=target, exact=True)
            ),
            lambda: self._first_scoped(
                lambda root: root.get_by_role("combobox", name=target, exact=False)
            ),
            lambda: self._first(lambda: self.page.locator(f'[aria-label="{target}"]')),
            lambda: self._first(lambda: self.page.locator(f'[aria-label*="{target}" i]')),
            lambda: self._first_scoped(
                lambda root: root.get_by_placeholder(target, exact=True)
            ),
            lambda: self._first_scoped(
                lambda root: root.get_by_placeholder(target, exact=False)
            ),
        ]

        for strategy in strategies:
            locator = strategy()

            if locator:
                return locator

        return None

    # -------------------------
    # ENTER
    # -------------------------

    def enter(self, target, value):

        locator = self.find_input(target)

        if locator is None:
            raise Exception(f"Could not find input: {target}")

        role = locator.get_attribute("role")

        if role == "combobox":

            locator.click()

            locator.type(str(value), delay=30)

            locator.press("Enter")

            return

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
