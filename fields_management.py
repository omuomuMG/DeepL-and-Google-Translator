from pathlib import Path
from aqt import mw
import os
import json




def fetch_fields(DefaltMode = False, editor = None):
    if DefaltMode:
        deck_name = "GreatestTranslatorDefault"
    else:
        deck_name = mw.col.decks.name(mw.col.decks.get_current_id())
    if editor is not None:
        if editor is not None and hasattr(editor, 'nids') and editor.nids:
            note = mw.col.getNote(editor.nids[0])
        else:
            # fallback if editor.note is available
            note = editor.note
            # Use note.mid if available, otherwise fall back to note['mid']. mid is a attribute about the note type id.
        if hasattr(note, "mid"):
            note_type_id = note.mid
        else:
            note_type_id = note['mid']
    else:
        note_type_id = ""
    
    deck_name = deck_name + str(note_type_id)

    profile_dir = Path(mw.pm.profileFolder())
    json_path = profile_dir / "GreatestTranslatorFieldsSetting.json"
    
    if os.path.exists(json_path):
        with open(json_path, 'r', encoding='utf-8') as f:
            try:
                fields_settings = json.load(f)
            except json.JSONDecodeError:
                # if the JSON file is empty or corrupted, initialize an empty dictionary
                fields_settings = {}
    else:
        # if the JSON file does not exist, create an empty dictionary
        fields_settings = {}

    if "GreatestTranslatorDefault" not in fields_settings:
        fields_settings["GreatestTranslatorDefault"] = {"Front": "Front", "Back": "Back", "target_language_deepl": "JA", "target_language_google": "ja", "target_language_index_deepl": 16, "target_language_index_google": 84}
        # write back to JSON so that default entry is persisted
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(fields_settings, f, ensure_ascii=False, indent=2)
    
    # search for the deck name in the JSON data
    if deck_name in fields_settings:
        source_field = fields_settings[deck_name].get("Front", "")
        target_field = fields_settings[deck_name].get("Back", "")
        target_language_deepl = fields_settings[deck_name].get("target_language_deepl", "")
        target_language_google = fields_settings[deck_name].get("target_language_google", "")
        target_language_index_deepl = fields_settings[deck_name].get("target_language_index_deepl", "")
        target_language_index_google = fields_settings[deck_name].get("target_language_index_google", "")
        
        
        return source_field, target_field, target_language_deepl, target_language_google, int(target_language_index_deepl), int(target_language_index_google)
    else:
        #  if the deck name is not found

        source_field = fields_settings["GreatestTranslatorDefault"].get("Front", "")
        target_field = fields_settings["GreatestTranslatorDefault"].get("Back", "")
        target_language_deepl = fields_settings["GreatestTranslatorDefault"].get("target_language_deepl", "")
        target_language_google = fields_settings["GreatestTranslatorDefault"].get("target_language_google", "")
        target_language_index_deepl = fields_settings["GreatestTranslatorDefault"].get("target_language_index_deepl", "")
        target_language_index_google = fields_settings["GreatestTranslatorDefault"].get("target_language_index_google", "")

        fields_settings[deck_name] = {
            "Front": source_field,
            "Back": target_field,
            "target_language_deepl": target_language_deepl,
            "target_language_google": target_language_google,
            "target_language_index_deepl": target_language_index_deepl,
            "target_language_index_google": target_language_index_google
        }
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(fields_settings, f, ensure_ascii=False, indent=2)
        
        return source_field, target_field, target_language_deepl, target_language_google, int(target_language_index_deepl), int(target_language_index_google)

def save_fields(source_field, target_field, target_langueage_deepl, target_language_google, target_language_index_deepl, target_language_index_google, DefaltMode = False, editor = None):
    if DefaltMode:
        deck_name = "GreatestTranslatorDefault"
    else:
        deck_name = mw.col.decks.name(mw.col.decks.get_current_id())

    if editor is not None:
        if editor is not None and hasattr(editor, 'nids') and editor.nids:
            note = mw.col.getNote(editor.nids[0])
        else:
            # fallback if editor.note is available
            note = editor.note

            # Use note.mid if available, otherwise fall back to note['mid']. mid is a attribute about the note type id.
        if hasattr(note, "mid"):
            note_type_id = note.mid
        else:
            note_type_id = note['mid']
    else:
        note_type_id = ""

    deck_name = deck_name + str(note_type_id)
    
    profile_dir = Path(mw.pm.profileFolder())
    json_path = profile_dir / "GreatestTranslatorFieldsSetting.json"
    
    if os.path.exists(json_path):
        with open(json_path, 'r', encoding='utf-8') as f:
            try:
                fields_settings = json.load(f)
            except json.JSONDecodeError:
                # if the JSON file is empty or corrupted, initialize an empty dictionary
                fields_settings = {}
    else:
        # if the JSON file does not exist, create an empty dictionary
        fields_settings = {}
    
    # save the current deck name and its fields to the JSON data
    fields_settings[deck_name] = {
        "Front": source_field,
        "Back": target_field,
        "target_language_deepl": target_langueage_deepl,
        "target_language_google": target_language_google,
        "target_language_index_deepl": target_language_index_deepl,
        "target_language_index_google": target_language_index_google
    }
    
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(fields_settings, f, ensure_ascii=False, indent=2) 