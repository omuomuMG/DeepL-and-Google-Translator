import datetime
import json
import os
from pathlib import Path
import sys

from aqt import mw

from .api_limits import  reset_api_usage

def get_date_from_json():
    profile_dir = Path(mw.pm.profileFolder())
    json_path = profile_dir / "DandGTranslatorSetting.json"

    if not json_path.exists():
        default_config = {"setting": {"source_field": "Front","target_field": "Back","DEEPL_API_KEY": "INSERT YOUR API","GOOGLE_CLOUD_API_KEY": "INSERT YOUR API","translation_mode": "Google","target_language_deepl": "JA","target_language_index_deepl": 16,"target_language_google": "ja","target_language_index_google": 84,"is_safe_mode": True,"target_language": "eu"},"character_count": {"DeepL": 0,"Google": 0},"date": {"DeepL": "2020-04-01","Google": "2020-04-01"}}
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(default_config, f, indent=4)

    with open(json_path, 'r+') as json_open:
        json_load = json.load(json_open)
        dates = json_load.get('date', {})
        json_open.seek(0)
        json.dump(json_load, json_open, indent=4)
        json_open.truncate()
    return dates

def check_update_date():
    addon_dir = os.path.dirname(os.path.realpath(__file__))
    vendor_dir = os.path.join(addon_dir, "python-dateutil")
    sys.path.append(vendor_dir)

    from dateutil.relativedelta import relativedelta

    dates = get_date_from_json()


    #-----DeepL------

    # date from json
    read_date = dates.get("DeepL")
    read_date = datetime.datetime.strptime(read_date, '%Y-%m-%d').date()

    # current date
    current_date = datetime.date.today()
    current_year = current_date.year
    current_month = current_date.month

    # Update date
    if read_date <= current_date:
        new_update_date = datetime.date(current_year, current_month, read_date.day)
        new_update_date = new_update_date + relativedelta(months=1)
        write_date("DeepL", new_update_date.strftime('%Y-%m-%d'))

        reset_api_usage("DeepL")


    #-----Google-----

    # date from json
    read_date = dates.get("Google")
    read_date = datetime.datetime.strptime(read_date, '%Y-%m-%d').date()


    # current date
    current_date = datetime.date.today()
    current_year = current_date.year
    current_month = current_date.month

    if read_date <= current_date:
        new_update_date = datetime.date(current_year, current_month, 1)
        new_update_date = new_update_date + relativedelta(months=1)
        write_date("Google", new_update_date.strftime('%Y-%m-%d'))

        reset_api_usage("Google")

# Update date in Json "date"
def write_date(translate_mode, date):
    profile_dir = Path(mw.pm.profileFolder())
    json_path = profile_dir / "DandGTranslatorSetting.json"

    if not json_path.exists():
        default_config = {"setting": {"source_field": "Front","target_field": "Back","DEEPL_API_KEY": "INSERT YOUR API","GOOGLE_CLOUD_API_KEY": "INSERT YOUR API","translation_mode": "Google","target_language_deepl": "JA","target_language_index_deepl": 16,"target_language_google": "ja","target_language_index_google": 84,"is_safe_mode": True,"target_language": "eu"},"character_count": {"DeepL": 0,"Google": 0},"date": {"DeepL": "2020-04-01","Google": "2025-04-01"}}
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(default_config, f, indent=4)

    with open(json_path, 'r+') as json_open:
        json_load = json.load(json_open)
        if translate_mode == 'DeepL':
            json_load['date']['DeepL'] = date
        else:
            json_load['date']['Google'] = date
        json_open.seek(0)
        json.dump(json_load, json_open, indent=4)
        json_open.truncate()
