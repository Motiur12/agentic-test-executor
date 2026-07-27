from actions.base import BaseAction


class CheckAction(BaseAction):

    def execute(self, page, group=None, target=None, **kwargs):

        if not group:
            raise Exception("Checkbox group is required.")

        if not target:
            raise Exception("Checkbox target is required.")

        group_label = page.get_by_text(group)

        options = group_label.locator("xpath=following-sibling::div[1]")

        option = options.get_by_text(target, exact=True)

        option.click()

        print(f"✓ Checked '{group} -> {target}'")