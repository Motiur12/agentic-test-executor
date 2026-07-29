import argparse
import json
import sys
from pathlib import Path

from agents.executor import Executor
from agents.planner import Planner
from workflows.cartup import CartUpWorkflow


def parse_args():
    parser = argparse.ArgumentParser(
        description="Agentic UI test executor for CartUp admin."
    )
    parser.add_argument(
        "testcase",
        nargs="?",
        default="testcases/login.txt",
        help="Path to a plain-text testcase file (default: testcases/login.txt)",
    )
    parser.add_argument(
        "--quiet-plan",
        action="store_true",
        help="Do not print the full execution plan JSON",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    testcase_path = Path(args.testcase)

    if not testcase_path.is_file():
        print(f"Testcase file not found: {testcase_path}")
        return 1

    testcase = testcase_path.read_text(encoding="utf-8")

    plan = Planner().plan(testcase)
    test_cases = plan if isinstance(plan, list) else [plan]

    workflow = CartUpWorkflow()
    failures = 0

    for index, case_plan in enumerate(test_cases, start=1):
        if len(test_cases) > 1:
            print(f"\n===== Test Case {index}/{len(test_cases)} =====")

        case_plan = workflow.process(case_plan)

        if not args.quiet_plan:
            print("Execution Plan")
            print(json.dumps(case_plan, indent=4))

        ok = Executor().execute(case_plan)
        if not ok:
            failures += 1

    if failures:
        print(f"\n{failures}/{len(test_cases)} test case(s) failed.")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
