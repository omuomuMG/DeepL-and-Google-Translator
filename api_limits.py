import json
import os
import datetime

deepl_api_limits = 450000           # Originally 500000
google_cloud_api_limits = 450000    # Originally 500000

# reset "character_count" of json
def reset_api_usage(translate_mode):
    addon_dir = os.path.dirname(os.path.realpath(__file__))
    json_path = os.path.join(addon_dir, 'setting.json')
    with open(json_path, 'r+') as json_open:
        json_load = json.load(json_open)
        if translate_mode == 'DeepL':
            json_load['character_count']['Deepl'] = 0
        else:
            json_load['character_count']['Google'] = 0
        json_open.seek(0)
        json.dump(json_load, json_open, indent=4)
        json_open.truncate()

