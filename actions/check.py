import re

from actions.base import BaseAction


class CheckAction(BaseAction):

    def execute(self, page, group=None, target=None, timeout=5000, **kwargs):

        if not group:
            raise Exception("Checkbox group is required.")

        if not target:
            raise Exception("Checkbox target is required.")

        # Case-insensitive, whole-string match: fixes "limited" not matching
        # "Limited" on case, and stops "limited" from also matching inside
        # "Unlimited" as a loose substring.
        pattern = re.compile(rf"^{re.escape(target.strip())}$", re.I)

        option_label = None
        attempts = max(1, int(timeout) // 250)

        for attempt in range(attempts):

            group_label = page.get_by_text(group).first
            options = group_label.locator("xpath=following-sibling::div[1]")
            candidate = options.get_by_text(pattern).first

            if candidate.count() > 0:
                option_label = candidate
                break

            if attempt < attempts - 1:
                page.wait_for_timeout(250)

        if option_label is None:
            raise Exception(
                f"Could not find option '{target}' in group '{group}'"
            )

        row = option_label.locator("xpath=..")

        checkbox_input = row.locator(
            'input[type="checkbox"], input[type="radio"]'
        ).first

        if checkbox_input.count() == 0:
            raise Exception(
                f"No checkbox/radio input found near option '{target}'"
            )

        if checkbox_input.is_checked():
            print(f"✓ '{group} -> {target}' already checked")
            return

        clickable = row.locator(".p-checkbox, .p-radiobutton").first

        if clickable.count() == 0:
            clickable = checkbox_input

        clickable.click()

        print(f"✓ Checked '{group} -> {target}'")