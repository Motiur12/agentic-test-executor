from .goto import GotoAction
from .click import ClickAction
from .enter_text import EnterTextAction
from .verify import VerifyAction
from .upload import UploadAction
from .enter_number import EnterNumberAction
from .check import CheckAction
from .wait_for_navigation import WaitForNavigationAction
from .select import SelectAction
from .select_date import SelectDateAction
from .wait import WaitAction

ACTIONS = {
    "goto": GotoAction(),
    "click": ClickAction(),
    "enter_text": EnterTextAction(),
    "verify": VerifyAction(),
    "upload": UploadAction(),
    "enter_number": EnterNumberAction(),
    "check": CheckAction(),
    "wait_for_navigation": WaitForNavigationAction(),
    "select": SelectAction(),
    "select_date": SelectDateAction(),
    "wait": WaitAction(),
}