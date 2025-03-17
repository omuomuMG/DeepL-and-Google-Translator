import json
from aqt.qt import *


def setting(source_field, target_field, deepl_api_key, google_cloud_api_key, translate_mode, is_safe_mode):

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

    mode_label = QLabel("Mode:")
    layout.addWidget(mode_label)
    mode_layout = QHBoxLayout()
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

    with open(json_path, 'r+') as json_open:
        json_load = json.load(json_open)
        json_load['setting']['source_field'] = source_text.text()
        json_load['setting']['target_field'] = target_text.text()
        json_load['setting']['DEEPL_API_KEY'] = deepl_api_text.text()
        json_load['setting']['GOOGLE_CLOUD_API_KEY'] = google_cloud_api_text.text()
        if radio_google.isChecked():
            json_load['setting']['translation_mode'] = "Google"
        else:
            json_load['setting']['translation_mode'] = "DeepL"
        json_load['setting']['is_safe_mode'] = safe_mode_checkbox.isChecked()



        json_open.seek(0)
        json.dump(json_load, json_open, indent=4)
        json_open.truncate()


def get_field():
    addon_dir = os.path.dirname(os.path.realpath(__file__))
    json_path = os.path.join(addon_dir, 'setting.json')

    with open(json_path, 'r+') as json_open:
        json_load = json.load(json_open)
        source_field = json_load['setting']['source_field']
        target_field = json_load['setting']['target_field']
        deepl_api_key = json_load['setting']['DEEPL_API_KEY']
        google_cloud_api_key = json_load['setting']['GOOGLE_CLOUD_API_KEY']
        translate_mode = json_load['setting']['translation_mode']
        is_safe_mode = json_load['setting']['is_safe_mode']

        json_open.seek(0)
        json.dump(json_load, json_open, indent=4)
        json_open.truncate()
    return  source_field, target_field, deepl_api_key, google_cloud_api_key, translate_mode, is_safe_mode


def get_character_count():
    addon_dir = os.path.dirname(os.path.realpath(__file__))
    json_path = os.path.join(addon_dir, 'setting.json')

    with open(json_path, 'r+') as json_open:
        json_load = json.load(json_open)
        character_count_deepl = json_load['character_count']['deepl']
        json_open.seek(0)
        json.dump(json_load, json_open, indent=4)
        json_open.truncate()

    return character_count_deepl

def write_character_count(total_character_length_deepl):
    addon_dir = os.path.dirname(os.path.realpath(__file__))
    json_path = os.path.join(addon_dir, 'setting.json')
    with open(json_path, 'r+') as json_open:
        json_load = json.load(json_open)
        json_load['character_count']['deepl'] = total_character_length_deepl
        json_open.seek(0)
        json.dump(json_load, json_open, indent=4)
        json_open.truncate()