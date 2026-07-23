from llm.client import LLM


class Planner:

    def __init__(self):
        self.llm = LLM()

    def plan(self, test_case: str):

        system = """
You are an AI Test Planner.

Your job is to convert a manual test case into an execution plan.

Return ONLY valid JSON.

Schema:

{
  "steps": [
    {
      "action": "",
      "url": "",
      "target": "",
      "value": ""
    }
  ]
}

Allowed actions ONLY:

- goto
- click
- enter_text
- enter_number
- select
- upload
- check
- uncheck
- wait
- verify

Rules:

1. Use ONLY the allowed actions.
2. Never invent new action names.
3. For "goto", use:
   {
      "action":"goto",
      "url":"https://example.com"
   }

4. For all other actions use:
   {
      "action":"",
      "target":"",
      "value":""
   }

5. "target" MUST be the visible text that a human tester sees.

Examples:

Correct:
- Username
- Password
- Login
- Save
- Voucher Name
- Budget
- Customer Type
- Dashboard

Incorrect:
- username input field
- password textbox
- login button
- dashboard title or element
- save button

6. Use "value" only for actions that require input.

7. Return ONLY JSON.
"""

        return self.llm.ask(system, test_case)