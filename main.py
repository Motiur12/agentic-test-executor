import sys
import json

from agents.planner import Planner
from agents.executor import Executor
from workflows.cartup import CartUpWorkflow

# Default test case
testcase_file = "testcases/login.txt"

# If user provides a file
if len(sys.argv) > 1:
    testcase_file = sys.argv[1]

# Read test case
with open(testcase_file, "r", encoding="utf-8") as f:
    testcase = f.read()

# Generate execution plan(s) - one per "Test Case ID:" block, if present
planner = Planner()
plan = planner.plan(testcase)

test_cases = plan if isinstance(plan, list) else [plan]

# Apply CartUp rules and execute each test case with its own fresh browser
workflow = CartUpWorkflow()

for index, case_plan in enumerate(test_cases, start=1):

    if len(test_cases) > 1:
        print(f"\n===== Test Case {index}/{len(test_cases)} =====")

    case_plan = workflow.process(case_plan)

    print("Execution Plan")
    print(json.dumps(case_plan, indent=4))

    executor = Executor()
    executor.execute(case_plan)