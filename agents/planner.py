from parsers.testcase_parser import TestCaseParser


class Planner:

    def plan(self, test_case: str):
        return TestCaseParser().parse(test_case)
