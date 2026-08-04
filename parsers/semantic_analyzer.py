import re

class SemanticAnalyzer:
    """Map supported natural-language variants to canonical execution steps."""

    def analyze(self, instruction: str):
        if match := re.fullmatch(
            r"(?:open|goto|navigate\s+to)\s+(https?://\S+)", instruction, re.I
        ):
            return {"action": "goto", "url": match.group(1)}

        if match := re.fullmatch(r"(?:click|press|tap|choose)\s+(.+)", instruction, re.I):
            target = match.group(1).strip()
            if len(target) >= 2 and target[0] == target[-1] and target[0] in {'"', "'"}:
                target = target[1:-1].strip()
            return {"action": "click", "target": target}

        if match := re.fullmatch(
            r"(?:check|tick|select)\s+(.+?)\s+(limited|unlimited|yes|no|whitelist|blacklist|both)",
            instruction,
            re.I,
        ):
            group, target = match.groups()
            return {"action": "check", "group": group, "target": target}

        # Combobox / dropdown selection: Select State "Dhaka North"
        # Date picker: Select Date "2026-08-15" / Select Delivery Date "2026-08-15"
        if match := re.fullmatch(
            r"(?:select|choose|pick)\s+(.+?)\s+['\"](.*?)['\"]",
            instruction,
            re.I,
        ):
            target, value = match.groups()
            if re.fullmatch(r"\d{4}-\d{1,2}-\d{1,2}", value.strip()):
                return {"action": "select_date", "target": target, "value": value.strip()}
            return {"action": "select", "target": target, "value": value}

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

        if match := re.fullmatch(
            r"(?:upload|attach)\s+(.+?)\s+['\"](.*?)['\"]", instruction, re.I
        ):
            target, value = match.groups()
            return {"action": "upload", "target": target, "value": value}

        if match := re.fullmatch(
            r"(?:wait|pause|sleep)\s+(\d+)\s*(?:ms|milliseconds?)?",
            instruction,
            re.I,
        ):
            return {"action": "wait", "timeout": int(match.group(1))}

        if match := re.fullmatch(
            r"(?:wait|pause|sleep)\s+(\d+)\s*(?:s|sec|seconds?)",
            instruction,
            re.I,
        ):
            return {"action": "wait", "timeout": int(match.group(1)) * 1000}

        if match := re.fullmatch(
            r"(?:verify|confirm)\s+(?:that\s+)?url\s+(?:contains|includes)\s+['\"](.*?)['\"]",
            instruction,
            re.I,
        ):
            return {
                "action": "verify",
                "verify_type": "url_contains",
                "value": match.group(1),
            }

        if match := re.fullmatch(
            r"(?:verify|confirm)\s+(?:that\s+)?(.+?)\s+(?:is\s+)?(?:displayed|visible|shown|appears)",
            instruction,
            re.I,
        ):
            return {
                "action": "verify",
                "verify_type": "text",
                "target": match.group(1),
            }

        if match := re.fullmatch(r"(?:verify|confirm)\s+(.+)", instruction, re.I):
            return {
                "action": "verify",
                "verify_type": "text",
                "target": match.group(1),
            }

        raise ValueError(f"Unsupported testcase instruction: {instruction}")

    @staticmethod
    def _entry_step(target: str, value: str):
        action = "enter_number" if value.isdigit() else "enter_text"
        return {"action": action, "target": target, "value": value}