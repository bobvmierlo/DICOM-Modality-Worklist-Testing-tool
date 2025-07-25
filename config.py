# config.py
import json
import os

SETTINGS_FILE = os.path.join(os.path.dirname(__file__), "resources/settings.json")

DEFAULT_CONFIG = {
    "ae_title": "MY_AE",
    "server_ae_title": "DMWL_AE",
    "server_ip": "127.0.0.1",
    "server_port": 11112
}

def load_config():
    try:
        with open(SETTINGS_FILE, "r") as f:
            return json.load(f)
    except Exception:
        return DEFAULT_CONFIG

CONFIG = load_config()
