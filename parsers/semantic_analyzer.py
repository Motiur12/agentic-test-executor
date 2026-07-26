import re


class SemanticAnalyzer:
    """Map supported natural-language variants to canonical execution steps."""

    def analyze(self, instruction: str):
        if match := re.fullmatch(r"(?:open|goto|navigate\s+to)\s+(https?://\S+)", instruction, re.I):
            return {"action": "goto", "url": match.group(1)}

        if match := re.fullmatch(r"(?:click|press|tap|choose)\s+(.+)", instruction, re.I):
            return {"action": "click", "target": match.group(1)}

        if match := re.fullmatch(
            r"(?:type|fill)\s+['\"](.*?)['\"]\s+(?:in|into)\s+(.+)",
            instruction,
            re.I,
        ):
            value, target = match.groups()
            return self._entry_step(target, value)

        if match := re.fullmatch(
            r"fill\s+(.+?)\s+with\s+['\"](.*?)['\"]", instruction, re.I
        ):
            target, value = match.groups()
            return self._entry_step(target, value)

        if match := re.fullmatch(
            r"(?:enter|ernter|type|fill)\s+(.+?)\s+['\"](.*?)['\"]",
            instruction,
            re.I,
        ):
            target, value = match.groups()
            return self._entry_step(target, value)

        if match := re.fullmatch(r"(?:upload|attach)\s+(.+?)\s+['\"](.*?)['\"]", instruction, re.I):
            target, value = match.groups()
            return {"action": "upload", "target": target, "value": value}

        if match := re.fullmatch(
            r"(?:verify|confirm)\s+(?:that\s+)?url\s+(?:contains|includes)\s+['\"](.*?)['\"]",
            instruction,
            re.I,
        ):
            return {"action": "verify", "verify_type": "url_contains", "value": match.group(1)}

        if match := re.fullmatch(
            r"(?:verify|confirm)\s+(?:that\s+)?(.+?)\s+(?:is\s+)?(?:displayed|visible|shown|appears)",
            instruction,
            re.I,
        ):
            return {"action": "verify", "verify_type": "text", "target": match.group(1)}

        if match := re.fullmatch(r"(?:verify|confirm)\s+(.+)", instruction, re.I):
            return {"action": "verify", "verify_type": "text", "target": match.group(1)}

        raise ValueError(f"Unsupported testcase instruction: {instruction}")

    @staticmethod
    def _entry_step(target: str, value: str):
        action = "enter_number" if value.isdigit() else "enter_text"
        return {"action": action, "target": target, "value": value}
