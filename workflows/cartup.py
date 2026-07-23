from core.session import Session


class CartUpWorkflow:

    def process(self, plan):

        # If session exists, use the plan as-is
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

        plan["steps"] = login_steps + plan["steps"]

        return plan