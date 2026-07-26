import re

from parsers.semantic_analyzer import SemanticAnalyzer

TEST_CASE_HEADER = re.compile(r"^test case id\s*:", re.I)


class TestCaseParser:
    """Convert the project's plain-text testcase syntax into execution steps."""

    def __init__(self):
        self.semantic_analyzer = SemanticAnalyzer()

    def parse(self, test_case: str):
        blocks = self._split_into_blocks(test_case)
        plans = [self._parse_block(block) for block in blocks]

        # A file with a single "Test Case ID:" (or none at all) keeps
        # returning a single plan dict, unchanged from before.
        if len(plans) == 1:
            return plans[0]

        # Multiple "Test Case ID:" blocks -> one independent plan per block,
        # so each can be executed with its own fresh browser session.
        return plans

    def _split_into_blocks(self, test_case: str):
        blocks = []
        current = []

        for raw_line in test_case.splitlines():
            if TEST_CASE_HEADER.match(raw_line.strip()):
                if current:
                    blocks.append("\n".join(current))
                current = [raw_line]
            else:
                current.append(raw_line)

        if current:
            blocks.append("\n".join(current))

        return blocks or [test_case]

    def _parse_block(self, block: str):
        steps = []

        for raw_line in block.splitlines():
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