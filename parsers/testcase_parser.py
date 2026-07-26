import re

from parsers.semantic_analyzer import SemanticAnalyzer


class TestCaseParser:
    """Convert the project's plain-text testcase syntax into execution steps."""

    def __init__(self):
        self.semantic_analyzer = SemanticAnalyzer()

    def parse(self, test_case: str):
        steps = []

        for raw_line in test_case.splitlines():
            line = self._clean_line(raw_line)

            if (
                not line
                or line.casefold().startswith("test case:")
                or line.casefold().startswith("test case id:")
                or line.casefold().startswith("test case description:")
                or line.casefold().rstrip(":") == "steps"
            ):
                continue

            steps.append(self.semantic_analyzer.analyze(line))

        if not steps:
            raise ValueError("The testcase contains no executable instructions.")

        return {"steps": steps}

    @staticmethod
    def _clean_line(line: str) -> str:
        line = line.strip()
        line = re.sub(r"^\d+[.)]\s*", "", line)
        return line.rstrip(".").strip()
