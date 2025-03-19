import json
from aqt.qt import *

from .Supported_Languages import DEEPL_LANGUAGES, GOOGLE_LANGUAGES


def setting(from_browser = False):
    settings = get_field()
    source_field = settings.get('source_field')
    target_field = settings.get('target_field')
    deepl_api_key = settings.get('DEEPL_API_KEY')
    google_cloud_api_key = settings.get('GOOGLE_CLOUD_API_KEY')
    translate_mode = settings.get('translation_mode')
    target_language_index_deepl = settings.get('target_language_index_deepl')
    target_language_index_google = settings.get('target_language_index_google')
    is_safe_mode = settings.get('is_safe_mode')

    dialog = QDialog()
    dialog.setWindowTitle('Setting')
    dialog.resize(300, 200)

    layout = QVBoxLayout()

    # about source field
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
        deepl_api_text = QLineEdit(f"{deepl_api_key}")
        layout.addWidget(deepl_api_label)
        layout.addWidget(deepl_api_text)

        # about Google Cloud API KEY
        deepl_api_label = QLabel("Google Could API KEY:")
        google_cloud_api_text = QLineEdit(f"{google_cloud_api_key}")
        layout.addWidget(deepl_api_label)
        layout.addWidget(google_cloud_api_text)


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
        mode_label = QLabel(f"ℹ️Current Mode : ---{translate_mode}---\n\nMode and API key can only changed form Setting.\n\nCheck settings in Tools > Greatest Translater Settings.")
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

    button = QPushButton('Save')
    button.clicked.connect(dialog.accept)
    layout.addWidget(button)

    dialog.setLayout(layout)
    dialog.exec()

    addon_dir = os.path.dirname(os.path.realpath(__file__))
    json_path = os.path.join(addon_dir, 'setting.json')

    # Save setting
    with open(json_path, 'r+') as json_open:
        json_load = json.load(json_open)
        json_load['setting']['source_field'] = source_text.text()
        json_load['setting']['target_field'] = target_text.text()

        if not from_browser:
            json_load['setting']['DEEPL_API_KEY'] = deepl_api_text.text()
            json_load['setting']['GOOGLE_CLOUD_API_KEY'] = google_cloud_api_text.text()

        if translate_mode == "Google" and from_browser  or (not from_browser and radio_google.isChecked()):  # Google mode
            json_load['setting']['translation_mode'] = "Google"
            json_load['setting']['target_language_index_google'] = language_combo.currentIndex()
            json_load['setting']['target_language_google'] = language_combo.currentData()
        else:  # DeepL mode
            json_load['setting']['translation_mode'] = "DeepL"
            json_load['setting']['target_language_index_deepl'] = language_combo.currentIndex()
            json_load['setting']['target_language_deepl'] = language_combo.currentData()

        json_load['setting']['is_safe_mode'] = safe_mode_checkbox.isChecked()

        json_open.seek(0)
        json.dump(json_load, json_open, indent=4)
        json_open.truncate()


def get_field():
    addon_dir = os.path.dirname(os.path.realpath(__file__))
    json_path = os.path.join(addon_dir, 'setting.json')

    with open(json_path, 'r+') as json_open:
        json_load = json.load(json_open)
        settings = json_load.get('setting', {})
        json_open.seek(0)
        json.dump(json_load, json_open, indent=4)
        json_open.truncate()
    return settings



# Read character count from Json
def get_character_count():
    addon_dir = os.path.dirname(os.path.realpath(__file__))
    json_path = os.path.join(addon_dir, 'setting.json')

    with open(json_path, 'r+') as json_open:
        json_load = json.load(json_open)
        if json_load['setting']['translation_mode'] == 'DeepL':
            character_count = json_load['character_count']['deepl']
        else:
            character_count = json_load['character_count']['google']

        json_open.seek(0)
        json.dump(json_load, json_open, indent=4)
        json_open.truncate()

    return character_count

# Write character count to Json
def write_character_count(total_character_length):
    addon_dir = os.path.dirname(os.path.realpath(__file__))
    json_path = os.path.join(addon_dir, 'setting.json')
    with open(json_path, 'r+') as json_open:
        json_load = json.load(json_open)
        if json_load['setting']['translation_mode'] == 'DeepL':
            json_load['character_count']['deepl'] = total_character_length
        else:
            json_load['character_count']['google'] = total_character_length
        json_open.seek(0)
        json.dump(json_load, json_open, indent=4)
        json_open.truncate()