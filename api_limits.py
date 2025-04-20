import json
import os
import datetime
from pathlib import Path

from aqt import mw

deepl_api_limits = 450000           # Originally 500000
google_cloud_api_limits = 450000    # Originally 500000

# reset "character_count" of json
def reset_api_usage(translate_mode):
    profile_dir = Path(mw.pm.profileFolder())
    json_path = profile_dir / "GreatestTranslatorSetting.json"
    with open(json_path, 'r+') as json_open:
        json_load = json.load(json_open)
        if translate_mode == 'DeepL':
            json_load['character_count']['Deepl'] = 0
        else:
            json_load['character_count']['Google'] = 0
        json_open.seek(0)
        json.dump(json_load, json_open, indent=4)
        json_open.truncate()

