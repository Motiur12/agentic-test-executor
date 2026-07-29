from datetime import datetime

import config
from actions import ACTIONS
from browser import Browser
from core.resolver import Resolver
from core.session import Session
from workflows.cartup import CartUpWorkflow


class Executor:
    """Run a plan step-by-step. Returns True on full success, False on failure."""

    def __init__(self):
        self.browser = Browser()

    def execute(self, plan) -> bool:
        self.browser.start()

        try:
            # Session file may exist but be expired. Browser detects that and
            # sets authenticated=False. Inject login steps so the plan does
            # not try to click app menus on the login page.
            if not self.browser.authenticated:
                if not CartUpWorkflow._is_login_plan(plan):
                    print(
                        "Not authenticated. Prepending login flow before "
                        "the testcase steps."
                    )
                    plan = {
                        **plan,
                        "steps": CartUpWorkflow._login_steps() + plan["steps"],
                    }
                    print("Updated Execution Plan (login injected)")
                    import json
                    print(json.dumps(plan, indent=4))

            for i, step in enumerate(plan["steps"], start=1):
                step = {
                    key: Resolver.resolve(value)
                    for key, value in step.items()
                }

                action_name = step["action"]
                print(f"\nExecuting Step {i}: {action_name}")

                action = ACTIONS.get(action_name)
                if action is None:
                    print("❌ TEST FAILED")
                    print(f"Unsupported action: {action_name}")
                    self._screenshot(f"unsupported_{action_name}")
                    return False

                try:
                    params = {k: v for k, v in step.items() if k != "action"}
                    action.execute(self.browser.page, **params)

                    if (
                        step["action"] == "verify"
                        and step.get("verify_type", "text") == "text"
                        and step.get("target") == "Dashboard"
                    ):
                        Session.save(self.browser.page)
                        self.browser.authenticated = True

                    print("✓ PASS")

                except Exception as exc:
                    print("✗ FAIL")
                    print(f"Reason: {exc}")
                    self._screenshot(f"step_{i}_{action_name}")
                    print("\n========================")
                    print("❌ TEST FAILED")
                    print("========================")
                    return False

            print("\n========================")
            print("✅ TEST PASSED")
            print("========================")
            return True

        finally:
            self.browser.stop()

    def _screenshot(self, label: str):
        if not config.TAKE_SCREENSHOT_ON_FAILURE:
            return

        try:
            config.SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)
            stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            path = config.SCREENSHOT_DIR / f"fail_{label}_{stamp}.png"
            self.browser.page.screenshot(path=str(path), full_page=True)
            print(f"Screenshot saved: {path}")
        except Exception as exc:
            print(f"Could not save screenshot: {exc}")
