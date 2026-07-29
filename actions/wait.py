from .base import BaseAction


class WaitAction(BaseAction):
    """Pause execution for a fixed duration (milliseconds)."""

    def execute(self, page, timeout=1000, **kwargs):
        page.wait_for_timeout(int(timeout))
        print(f"✓ Waited {timeout}ms")
