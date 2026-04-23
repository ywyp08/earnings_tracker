import os
from pathlib import Path

# For Python < 3.11
try:
    import tomllib
except ImportError:
    import tomli as tomllib

CONFIG_DIR = Path.home() / ".config" / "earnings_tracker"
CONFIG_FILE = CONFIG_DIR / "config.toml"

DEFAULT_CONFIG = {
    "default_currency": "USD",
    "data_file_path": "~/.local/share/earnings_tracker/earnings.json"
}

def load_config():
    if not CONFIG_FILE.exists():
        return DEFAULT_CONFIG.copy()
    
    with open(CONFIG_FILE, "rb") as f:
        config = tomllib.load(f)
    
    merged = DEFAULT_CONFIG.copy()
    merged.update(config)
    return merged

def get_data_file_path():
    config = load_config()
    path = config["data_file_path"]
    return os.path.expanduser(path)

def get_default_currency():
    config = load_config()
    return config["default_currency"]