import json
from aqt.qt import *


def setting(source_field, target_field, api_key):

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


    # about API KEY
    api_label = QLabel("API KEY:")
    api_text = QLineEdit(f"{api_key}")
    layout.addWidget(api_label)
    layout.addWidget(api_text)


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
        json_load['setting']['DEEPL_API_KEY'] = api_text.text()


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
        api_key = json_load['setting']['DEEPL_API_KEY']

        # Move file pointer to the beginning of the file and dump updated data
        json_open.seek(0)
        json.dump(json_load, json_open, indent=4)
        json_open.truncate()
    return  source_field, target_field, api_key


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