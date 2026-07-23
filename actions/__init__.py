from .goto import GotoAction
from .click import ClickAction
from .enter_text import EnterTextAction
from .verify import VerifyAction

ACTIONS = {
    "goto": GotoAction(),
    "click": ClickAction(),
    "enter_text": EnterTextAction(),
    "verify": VerifyAction(),
}