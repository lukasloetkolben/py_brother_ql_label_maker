import json
import sys

import config

class Settings:
    DPI = 60 if sys.platform == 'darwin' else 80
    PRINTER_MODEL = ""
    PRINTER_IDENTIFIER = ""
    LABEL_TYPE = ""
    SAVE_AS_PATH = config.HOME_DIR

    @staticmethod
    def get_all_variables():
        out = []
        for i, j in Settings.__dict__.items():
            if not i.startswith("_") and not callable(j) and not isinstance(j, staticmethod):
                out.append((i.lower(), j))

        return out

    @staticmethod
    def save_setting_json():
        settings_file = config.SETTINGS_FILE
        settings = {}
        for key, value in Settings.get_all_variables():
            settings[key] = value

        with open(settings_file, "w") as out_file:
            json.dump(settings, out_file)

    @staticmethod
    def read_setting_json():
        settings_file = config.SETTINGS_FILE
        if settings_file.is_file():
            with open(settings_file, "r") as json_file:
                settings_json = json.load(json_file)
                for var, value in Settings.get_all_variables():
                    key = var.lower()  # Convert variable name to lowercase as per the JSON format
                    if key in settings_json:
                        setattr(Settings, var.upper(), settings_json[key])  # Set the value of the variable

        Settings.save_setting_json()


if __name__ == '__main__':
    Settings.read_setting_json()
