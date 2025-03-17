import os
import sys
from os import write

from PyQt6.QtCore import QTimer
from aqt.editor import Editor
from aqt.utils import showInfo

from .config_manager import get_field,get_character_count, write_character_count

addon_dir = os.path.dirname(os.path.realpath(__file__))
vendor_dir = os.path.join(addon_dir, "deepl-1.21.0")
sys.path.append(vendor_dir)

import deepl


# Translate by using Deepl API
def translate(editor: Editor):
    note  = editor.note
    source_field, target_field, api_key, is_safe_mode = get_field()
    translator = deepl.Translator(api_key)
    if source_field not in note:
        showInfo("Source field not found. Check settings in Tools > Greatest Translater Settings.")
        return

    if target_field not in note:
        showInfo(f"Target field '{target_field}' does not exist in the current note.")
        return


    source_text = note[source_field]
    if source_text == "":
        showInfo("Source text must be not empty")

    if not is_safe_mode or check_api_limits(source_text):
        try:
            result = translator.translate_text(source_text, target_lang="FR").text
            note[target_field] = result
            QTimer.singleShot(500, lambda: editor.loadNote())
        except:
            showInfo('Error Occurred. \n Please make sure API key, Fields is correct.\n Check settings in Tools > Greatest Translater Settings.')
    else: # If limit exceeds
        showInfo('The free quota for translations at DeepL may be exceeded. If you still wish to translate, please exit safe mode.')


# Check to see if the API free quota has been exceeded.
def check_api_limits(translated_text):
    character_count_deepl = get_character_count()
    # The original limit was 50,000 characters
    if character_count_deepl + len(translated_text) > 450000:
        return False
    else:
        write_character_count(character_count_deepl + len(translated_text))
        return True



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