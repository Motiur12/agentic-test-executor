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
            "icon",
            "select"
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
                lambda root: root.get_by_label(target, exact=False)
            ),
            lambda: self._first_scoped(
                lambda root: root.get_by_placeholder(target, exact=True)
            ),
            lambda: self._first_scoped(
                lambda root: root.get_by_placeholder(target, exact=False)
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

        React Select (and similar) often expose no accessible name and put the
        visible label in a sibling placeholder <div>, not the HTML placeholder
        attribute. Strategies therefore try both the raw target and a lightly
        normalized form, then fall back to locating by nearby visible text.
        """
        raw = (target or "").strip()
        # Keep "Select State" intact for placeholder matching; only drop noise
        # words that are never part of the visible label.
        soft = raw.lower()
        for word in ("button", "textbox", "text box", "input", "field", "link",
                     "dropdown", "menu", "icon"):
            soft = soft.replace(word, "")
        soft = " ".join(soft.split())

        if not raw and not soft:
            return None

        variants = []
        for v in (raw, soft, self.normalize(raw)):
            if v and v not in variants:
                variants.append(v)

        strategies = []

        for v in variants:
            strategies.extend([
                lambda v=v: self._first_scoped(
                    lambda root: root.get_by_label(v, exact=True)
                ),
                lambda v=v: self._first_scoped(
                    lambda root: root.get_by_label(v, exact=False)
                ),
                lambda v=v: self._first_scoped(
                    lambda root: root.get_by_role("combobox", name=v, exact=True)
                ),
                lambda v=v: self._first_scoped(
                    lambda root: root.get_by_role("combobox", name=v, exact=False)
                ),
                lambda v=v: self._first(
                    lambda: self.page.locator(f'[aria-label="{v}"]')
                ),
                lambda v=v: self._first(
                    lambda: self.page.locator(f'[aria-label*="{v}" i]')
                ),
                lambda v=v: self._first_scoped(
                    lambda root: root.get_by_placeholder(v, exact=True)
                ),
                lambda v=v: self._first_scoped(
                    lambda root: root.get_by_placeholder(v, exact=False)
                ),
                # React Select: placeholder is a <div>, not an attribute.
                # Find visible text, climb to the control that owns a combobox.
                lambda v=v: self._first(
                    lambda: self.page.get_by_text(v, exact=False)
                    .locator(
                        'xpath=ancestor::*[.//input[@role="combobox"]][1]'
                    )
                    .locator('input[role="combobox"]')
                ),
                # Same idea, scoped to common react-select container patterns
                # without hard-coding emotion CSS hashes.
                lambda v=v: self._first(
                    lambda: self.page.locator(
                        f'div:has(> div:text-is("{v}")), '
                        f'div:has([class*="placeholder"]:text-is("{v}"))'
                    ).locator('input[role="combobox"]').first
                ),
            ])

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
            locator = self.find_combobox(target)

        if locator is None:
            raise Exception(f"Could not find input: {target}")

        role = locator.get_attribute("role")

        if role == "combobox":
            self._fill_combobox(locator, value)
            return

        if role == "spinbutton":

            locator.click()

            locator.press("Control+A")

            locator.press("Backspace")

            locator.type(str(value), delay=30)

            locator.press("Tab")

            return

        locator.fill(str(value))

    def _fill_combobox(self, locator, value):
        """Type into a combobox and confirm the matching option.

        Works for React Select, MUI Autocomplete, and native-ish listboxes:
        open → type filter → pick option by role or visible text → fallback Enter.
        """
        value = str(value)

        locator.click()
        # Clear any previous selection text so filtering starts clean.
        locator.press("Control+A")
        locator.press("Backspace")
        locator.type(value, delay=30)

        # Prefer an explicit option click (React Select listbox).
        option = None
        option_strategies = [
            lambda: self.page.get_by_role("option", name=value, exact=True),
            lambda: self.page.get_by_role("option", name=value, exact=False),
            lambda: self.page.locator(
                f'[id*="option"]:text-is("{value}")'
            ),
            lambda: self.page.locator(
                f'[class*="option"]:text-is("{value}")'
            ),
            lambda: self.page.get_by_text(value, exact=True),
        ]

        for strategy in option_strategies:
            try:
                candidate = strategy().first
                candidate.wait_for(state="visible", timeout=1500)
                if candidate.is_visible():
                    option = candidate
                    break
            except Exception:
                continue

        if option is not None:
            option.click()
        else:
            locator.press("Enter")

        # Let dependent fields (City after State, Zone after City) render.
        self.page.wait_for_timeout(300)

    def enter_number(self, target, value):

        locator = self.find_input(target)

        if locator is None:
            raise Exception(f"Could not find input: {target}")

        locator.click()
        locator.press("Control+A")
        locator.press("Backspace")
        locator.type(str(value), delay=30)
        locator.press("Tab")