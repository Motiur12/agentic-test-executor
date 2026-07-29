import config
from core.session import Session


class CartUpWorkflow:
    """CartUp-specific rules: session reuse and automatic login injection."""

    LOGIN_TARGETS = frozenset({"username", "password", "login"})

    @classmethod
    def _is_login_plan(cls, plan):
        """Detect a planner-generated login testcase before injecting it again."""
        targets = {
            step.get("target", "").strip().lower()
            for step in plan.get("steps", [])
            if isinstance(step, dict)
        }
        return cls.LOGIN_TARGETS.issubset(targets)

    @staticmethod
    def _login_steps():
        return [
            {"action": "goto", "url": config.BASE_URL},
            {
                "action": "enter_text",
                "target": "Username",
                "value": "${USERNAME}",
            },
            {
                "action": "enter_text",
                "target": "Password",
                "value": "${PASSWORD}",
            },
            {"action": "click", "target": "Login"},
            {
                "action": "enter_text",
                "target": "OTP",
                "value": "${OTP}",
            },
            {"action": "click", "target": "Submit"},
            {"action": "verify", "target": "Dashboard"},
        ]

    def process(self, plan):
        is_login_plan = self._is_login_plan(plan)

        if is_login_plan and Session.exists():
            print("Login testcase detected. Clearing existing session.")
            Session.delete()

        if Session.exists():
            print("Using existing session.")
            return plan

        print("No session. Injecting login flow.")
        login_steps = self._login_steps()

        if is_login_plan:
            print("Login testcase detected. Using the standard login flow.")
            plan["steps"] = login_steps
            return plan

        plan["steps"] = login_steps + plan["steps"]
        return plan
