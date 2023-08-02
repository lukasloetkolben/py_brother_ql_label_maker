import json
import sys

import config


class Settings:
    DPI = 60 if sys.platform == 'darwin' else 80

    @staticmethod
    def save_setting_json():
        settings_file = config.SETTINGS_FILE
        settings = {
            "dpi": Settings.DPI,
        }
        with open(settings_file, "w") as out_file:
            json.dump(settings, out_file)

    @staticmethod
    def read_js(settings_json, param, value):
        s = settings_json.get(value)
        if s is None:
            return param
        else:
            return s

    @staticmethod
    def read_setting_json():
        settings_file = config.SETTINGS_FILE
        if settings_file.is_file():
            with open(settings_file, "r") as json_file:
                settings_json = json.load(json_file)
                Settings.DPI = Settings.read_js(settings_json, Settings.DPI, "dpi")

        Settings.save_setting_json()
