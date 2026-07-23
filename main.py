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

# Generate execution plan
planner = Planner()
plan = planner.plan(testcase)

# Apply CartUp rules
workflow = CartUpWorkflow()
plan = workflow.process(plan)

print("Execution Plan")
print(json.dumps(plan, indent=4))

# Execute
executor = Executor()
executor.execute(plan)