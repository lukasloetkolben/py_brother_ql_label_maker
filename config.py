import json
import os
from pathlib import Path

# Directories
BASE = os.path.dirname(os.path.abspath(__file__))
HOME_DIR = Path.home()
CONFIG_DIR = Path(HOME_DIR, ".config", "pbqllm")
TEMP_DIR = Path(HOME_DIR, ".local", "share", "pbqllm", "temp")
ASSETS_DIR = Path(BASE, "assets")
ICONS_DIR = Path(ASSETS_DIR, "icons")

# Files
SETTINGS_FILE = Path(CONFIG_DIR, "settings.json")  # default settings file
STYLE = Path(ASSETS_DIR, "style.qss")
COLORS_FILE = Path(ASSETS_DIR, "colors.json")

with open(COLORS_FILE) as f:
    COLORS = json.load(f)
