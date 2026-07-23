from .goto import GotoAction
from .click import ClickAction
from .enter_text import EnterTextAction
from .verify import VerifyAction
from .upload import UploadAction
from .wait_for_navigation import WaitForNavigationAction

ACTIONS = {
    "goto": GotoAction(),
    "click": ClickAction(),
    "enter_text": EnterTextAction(),
    "verify": VerifyAction(),
    "upload": UploadAction(),
    "wait_for_navigation": WaitForNavigationAction(),
}