import datetime
import json
import os
import sys

from .api_limits import  reset_api_usage

def get_date_from_json():
    addon_dir = os.path.dirname(os.path.realpath(__file__))
    json_path = os.path.join(addon_dir, 'setting.json')

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
    addon_dir = os.path.dirname(os.path.realpath(__file__))
    json_path = os.path.join(addon_dir, 'setting.json')
    with open(json_path, 'r+') as json_open:
        json_load = json.load(json_open)
        if translate_mode == 'DeepL':
            json_load['date']['DeepL'] = date
        else:
            json_load['date']['Google'] = date
        json_open.seek(0)
        json.dump(json_load, json_open, indent=4)
        json_open.truncate()
