import json
from datetime import datetime
from pathlib import Path

from aqt.qt import *
from aqt import mw
import os
from .fields_management import fetch_fields, save_fields
import json

from .api_limits import deepl_api_limits, google_cloud_api_limits
from .Supported_Languages import DEEPL_LANGUAGES, GOOGLE_LANGUAGES
from .date_management import check_update_date, get_date_from_json



def setting(from_browser = False, editor = None):
    settings = get_field()

    if from_browser:
        source_field, target_field, target_language_deepl, target_language_google, target_language_index_deepl, target_language_index_google = fetch_fields(False, editor)
    else:  
        source_field, target_field, target_language_deepl, target_language_google, target_language_index_deepl, target_language_index_google = fetch_fields(True, editor)

    deepl_api_key = settings.get('DEEPL_API_KEY')
    google_cloud_api_key = settings.get('GOOGLE_CLOUD_API_KEY')
    translate_mode = settings.get('translation_mode')
    is_safe_mode = settings.get('is_safe_mode')



    dialog = QDialog()
    dialog.setWindowTitle('Setting')
    dialog.resize(300, 200)

    layout = QVBoxLayout()

    if from_browser:
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
        note_type = mw.col.models.get(note_type_id)
        available_fields = [field['name'] for field in note_type['flds']]
        
        source_label = QLabel("Source Field:")
        source_combo = QComboBox()
        source_combo.addItems(available_fields)
        if source_field in available_fields:
            source_combo.setCurrentText(source_field)
        layout.addWidget(source_label)
        layout.addWidget(source_combo)
        
        # about target field
        target_label = QLabel("Target Field:")
        target_combo = QComboBox()
        target_combo.addItems(available_fields)
        if target_field in available_fields:
            target_combo.setCurrentText(target_field)
        layout.addWidget(target_label)
        layout.addWidget(target_combo)
    else:
        source_label = QLabel("Source Field:")
        source_text = QLineEdit(f"{source_field}")
        layout.addWidget(source_label)
        layout.addWidget(source_text)

        # about target field
        target_label = QLabel("Target Field:")
        target_text = QLineEdit(f"{target_field}")
        layout.addWidget(target_label)
        layout.addWidget(target_text)

    # User can change API key and mode only from Menu
    if not from_browser:
        # about Deepl API KEY
        deepl_api_label = QLabel("DeepL API KEY:")
        # if deepl_api_key:
        deepl_api_text = QLineEdit()
        if deepl_api_key:
            deepl_api_text.setText(deepl_api_key)
        deepl_api_text.setPlaceholderText("********-****-****-****-************:fx")
        layout.addWidget(deepl_api_label)
        layout.addWidget(deepl_api_text)

        # about Google Cloud API KEY
        deepl_api_label = QLabel("Google Could API KEY:")

        # if google_cloud_api_key:
        google_cloud_api_text = QLineEdit()
        if google_cloud_api_key:
            google_cloud_api_text.setText(google_cloud_api_key)
        google_cloud_api_text.setPlaceholderText("****************************************")
        layout.addWidget(deepl_api_label)
        layout.addWidget(google_cloud_api_text)

        # about initial date of DeepL api key
        dates = get_date_from_json()
        start_date_deepl = dates.get('DeepL')
        start_date_deepl = datetime.strptime(start_date_deepl, '%Y-%m-%d')

        date_label = QLabel("Please enter the start date of the Current usage period about DeepL api key:")
        layout.addWidget(date_label)
        date_input = QDateEdit()
        date_input.setCalendarPopup(True)
        date_input.setDate(QDate(start_date_deepl.year, start_date_deepl.month, start_date_deepl.day))
        layout.addWidget(date_input)


        # Select Translation Mode Google Could or DeepL
        mode_label = QLabel("Mode:")
        layout.addWidget(mode_label)
        mode_layout = QHBoxLayout()

        # Radio button about mode
        radio_google = QRadioButton("Google Cloud")
        radio_deepl = QRadioButton("DeepL")
        mode_group = QButtonGroup()
        mode_group.addButton(radio_google)
        mode_group.addButton(radio_deepl)
        mode_layout.addWidget(radio_google)
        mode_layout.addWidget(radio_deepl)
        layout.addLayout(mode_layout)

        if translate_mode == "DeepL":
            radio_deepl.setChecked(True)
        else:
            radio_google.setChecked(True)
    else:
        mode_label = QLabel(f"ℹ️Current Mode ---{translate_mode}---\n\nMode and API key can only changed form Setting.\n\nCheck settings in Tools > Greatest Translater Settings.")
        layout.addWidget(mode_label)

    # Select target language
    target_language_label = QLabel("Target Language:")
    layout.addWidget(target_language_label)
    language_combo = QComboBox()

    layout.addWidget(language_combo)

    # update language lists depend on translation mode
    def update_language_options():
        language_combo.blockSignals(True)
        language_combo.clear()

        if (translate_mode == "Google" and from_browser) or (not from_browser and radio_google.isChecked()):  # Google mode
            languages = GOOGLE_LANGUAGES
            index = target_language_index_google
        else: # Deepl mode
            languages = DEEPL_LANGUAGES
            index = target_language_index_deepl

        for idx, (display, code) in enumerate(languages):
            language_combo.addItem(display, code)
            if code == translate_mode:
                index = idx

        language_combo.setCurrentIndex(index)
        language_combo.blockSignals(False)

    if not from_browser:
        # Change immediately.
        radio_google.toggled.connect(update_language_options)
        radio_deepl.toggled.connect(update_language_options)

    update_language_options()

    # Safe Mode
    safe_mode_checkbox = QCheckBox("Enable Safe Mode")
    safe_mode_checkbox.setChecked(is_safe_mode)
    layout.addWidget(safe_mode_checkbox)

    deepl_api_usage = get_character_count("DeepL")
    deepl_meter_label = QLabel(f"DeepL: {deepl_api_usage} / {deepl_api_limits} chars used: {round(deepl_api_usage / deepl_api_limits * 100,2)} %")
    layout.addWidget(deepl_meter_label)

    deepl_progress_bar = QProgressBar()
    deepl_progress_bar.setMinimum(0)
    deepl_progress_bar.setMaximum(100)

    deepl_progress_bar.setValue(deepl_api_usage/deepl_api_limits * 100)
    layout.addWidget(deepl_progress_bar)

    google_api_usage = get_character_count("Google")
    google_meter_label = QLabel(
        f"Google Cloud Translation: {google_api_usage} / {google_cloud_api_limits} chars used: {round(google_api_usage / google_cloud_api_limits * 100, 2)} %")
    layout.addWidget(google_meter_label)

    google_progress_bar = QProgressBar()
    google_progress_bar.setMinimum(0)
    google_progress_bar.setMaximum(100)

    google_progress_bar.setValue(google_api_usage/google_cloud_api_limits * 100)
    layout.addWidget(google_progress_bar)

    button = QPushButton('Save')
    button.clicked.connect(dialog.accept)
    layout.addWidget(button)


    dialog.setLayout(layout)
    dialog.exec()

    profile_dir = Path(mw.pm.profileFolder())
    json_path = profile_dir / "DandGTranslatorSetting.json"

    # Save setting
    with open(json_path, 'r+') as json_open:
        json_load = json.load(json_open)
        if from_browser:
            selected_source_field = source_combo.currentText()
            selected_target_field = target_combo.currentText()
        else:
            selected_source_field = source_text.text()
            selected_target_field = target_text.text()
            
        json_load['setting']['source_field'] = selected_source_field
        json_load['setting']['target_field'] = selected_target_field

        # Only from menu
        if not from_browser:
            json_load['setting']['DEEPL_API_KEY'] = deepl_api_text.text()
            json_load['setting']['GOOGLE_CLOUD_API_KEY'] = google_cloud_api_text.text()
            json_load['date']['DeepL'] = date_input.date().toString("yyyy-MM-dd")
        # Google mode
        if translate_mode == "Google" and from_browser  or (not from_browser and radio_google.isChecked()):
            json_load['setting']['translation_mode'] = "Google"
            json_load['setting']['target_language_index_google'] = language_combo.currentIndex()
            json_load['setting']['target_language_google'] = language_combo.currentData()
        else:  # DeepL mode
            json_load['setting']['translation_mode'] = "DeepL"
            json_load['setting']['target_language_index_deepl'] = language_combo.currentIndex()
            json_load['setting']['target_language_deepl'] = language_combo.currentData()

        json_load['setting']['is_safe_mode'] = safe_mode_checkbox.isChecked()

        target_language_deepl = json_load['setting']['target_language_deepl']
        target_language_google = json_load['setting']['target_language_google']
        target_language_index_deepl = json_load['setting']['target_language_index_deepl']
        target_language_index_google = json_load['setting']['target_language_index_google']

        json_open.seek(0)
        json.dump(json_load, json_open, indent=4)
        json_open.truncate()

    if from_browser:
        save_fields(source_combo.currentText(), target_combo.currentText(), target_language_deepl, target_language_google, target_language_index_deepl, target_language_index_google, False, editor=editor)
    else:  
        save_fields(source_text.text(), target_text.text(),target_language_deepl, target_language_google, target_language_index_deepl, target_language_index_google, True, editor=editor)
    

    
    check_update_date()

def get_field():
    profile_dir = Path(mw.pm.profileFolder())
    json_path = profile_dir / "DandGTranslatorSetting.json"

    with open(json_path, 'r+') as json_open:
        json_load = json.load(json_open)
        settings = json_load.get('setting', {})
        json_open.seek(0)
        json.dump(json_load, json_open, indent=4)
        json_open.truncate()
    return settings



# Read character count from Json
def get_character_count(translate_mode):
    profile_dir = Path(mw.pm.profileFolder())
    json_path = profile_dir / "DandGTranslatorSetting.json"

    with open(json_path, 'r+') as json_open:
        json_load = json.load(json_open)
        if translate_mode == 'DeepL':
            character_count = json_load['character_count']['DeepL']
        else:
            character_count = json_load['character_count']['Google']

        json_open.seek(0)
        json.dump(json_load, json_open, indent=4)
        json_open.truncate()

    return character_count

# Write character count to Json
def write_character_count(total_character_length):
    profile_dir = Path(mw.pm.profileFolder())
    json_path = profile_dir / "DandGTranslatorSetting.json"
    
    with open(json_path, 'r+') as json_open:
        json_load = json.load(json_open)
        if json_load['setting']['translation_mode'] == 'DeepL':
            json_load['character_count']['DeepL'] = total_character_length
        else:
            json_load['character_count']['Google'] = total_character_length
        json_open.seek(0)
        json.dump(json_load, json_open, indent=4)
        json_open.truncate()