from browser import Browser
from actions import ACTIONS
from core.resolver import Resolver
from core.session import Session


class Executor:

    def __init__(self):
        self.browser = Browser()

    def execute(self, plan):

        self.browser.start()

        try:

            for i, step in enumerate(plan["steps"], start=1):

                step = {
                    key: Resolver.resolve(value)
                    for key, value in step.items()
                }

                action_name = step["action"]

                print(f"\nExecuting Step {i}: {action_name}")

                action = ACTIONS.get(action_name)

                if action is None:
                    print(f"❌ TEST FAILED")
                    print(f"Unsupported action: {action_name}")
                    return

                try:
                    params = dict(step)
                    params.pop("action", None)

                    action.execute(self.browser.page, **params)

                    # Save session after successful dashboard login
                    if (
                        step["action"] == "verify"
                        and step.get("verify_type", "text") == "text"
                        and step.get("target") == "Dashboard"
                    ):
                        Session.save(self.browser.page)

                    print("✓ PASS")

                except Exception as e:

                    print("✗ FAIL")
                    print(f"Reason: {e}")

                    print("\n========================")
                    print("❌ TEST FAILED")
                    print("========================")

                    return

            print("\n========================")
            print("✅ TEST PASSED")
            print("========================")

        finally:
            self.browser.stop()