from core.session import Session


class CartUpWorkflow:

    @staticmethod
    def _is_login_plan(plan):
        """Detect a planner-generated login testcase before injecting it again."""
        targets = {
            step.get("target", "").strip().lower()
            for step in plan.get("steps", [])
            if isinstance(step, dict)
        }

        return {"username", "password", "login"}.issubset(targets)

    def process(self, plan):

        is_login_plan = self._is_login_plan(plan)

        # A login testcase must exercise the login form, not reuse a saved
        # dashboard session.
        if is_login_plan and Session.exists():
            print("Login testcase detected. Clearing existing session.")
            Session.delete()

        # Reuse a session only for non-login testcases.
        if Session.exists():
            print("Using existing session.")
            return plan

        print("No session. Injecting login flow.")

        login_steps = [
            {
                "action": "goto",
                "url": "https://pre-prod-admin.cartup.com"
            },
            {
                "action": "enter_text",
                "target": "Username",
                "value": "${USERNAME}"
            },
            {
                "action": "enter_text",
                "target": "Password",
                "value": "${PASSWORD}"
            },
            {
                "action": "click",
                "target": "Login"
            },
            {
                "action": "enter_text",
                "target": "OTP",
                "value": "${OTP}"
            },
            {
                "action": "click",
                "target": "Submit"
            },
            {
                "action": "verify",
                "target": "Dashboard"
            }
        ]

        if is_login_plan:
            print("Login testcase detected. Using the standard login flow.")
            plan["steps"] = login_steps
            return plan

        plan["steps"] = login_steps + plan["steps"]

        return plan
