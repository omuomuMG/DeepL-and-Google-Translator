from aqt import mw
from aqt.qt import *
from anki.hooks import addHook

from .date_management import check_update_date
from .utils import symbol_button, setting_button, add_browser_menu_button
from .config_manager import setting, get_field
from aqt import gui_hooks

# Check API update date
check_update_date()




gui_hooks.browser_will_show.append(add_browser_menu_button)

addHook("setupEditorButtons", symbol_button)
addHook("setupEditorButtons", setting_button)

action = QAction("Greatest-Translater", mw)

action.triggered.connect(lambda: setting(False))


mw.form.menuTools.addAction(action)
