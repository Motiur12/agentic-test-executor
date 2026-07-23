from .goto import GotoAction
from .click import ClickAction
from .enter_text import EnterTextAction
from .verify import VerifyAction
from .wait_for_navigation import WaitForNavigationAction

ACTIONS = {
    "goto": GotoAction(),
    "click": ClickAction(),
    "enter_text": EnterTextAction(),
    "verify": VerifyAction(),
    "wait_for_navigation": WaitForNavigationAction(),
}