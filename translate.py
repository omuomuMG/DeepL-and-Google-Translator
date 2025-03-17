import os
import sys

from PyQt6.QtCore import QTimer
from aqt.editor import Editor
from aqt.utils import showInfo


from .config_manager import get_field

addon_dir = os.path.dirname(os.path.realpath(__file__))
vendor_dir = os.path.join(addon_dir, "deepl-1.21.0")
sys.path.append(vendor_dir)

import deepl


def translate(editor: Editor):
    note  = editor.note
    source_field, target_field, api_key = get_field()
    translator = deepl.Translator(api_key)
    # source_text = note[source_field]
    if source_field not in note:
        showInfo("Source field not found. Check settings in Tools > Pronounce Symbol Generator Settings.")
        return

    if target_field not in note:
        showInfo(f"Target field '{target_field}' does not exist in the current note.")
        return
    # result = "This is temp val"
    result = translator.translate_text("Hello, world!", target_lang="FR").text


    print(type(result))

    # print("source_field_text:")
    # print("result:" + result)

    note[target_field] = result
    QTimer.singleShot(500, lambda: editor.loadNote())

    return "a"


def convert_word(editor: Editor):
    source_field, target_field, api_key = get_field()

    if not editor.note:
        showInfo("No note selected.")
        return

    note = editor.note

    if source_field not in note:
        showInfo("Source field not found. Check settings in Tools > Pronounce Symbol Generator Settings.")
        return

    if target_field not in note:
        showInfo(f"Target field '{target_field}' does not exist in the current note.")
        return

    source_text = note[source_field]


    succeeded = True




    QTimer.singleShot(500, lambda: editor.loadNote())