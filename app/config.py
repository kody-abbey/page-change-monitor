from platformdirs import user_config_dir
from pathlib import Path

APP_NAME = "page-update-monitor"
BASE_DIR = Path(user_config_dir())

CONFIG_DIR = BASE_DIR / APP_NAME
CONFIG_DIR.mkdir(parents=True, exist_ok=True)

CONFIG_FILE = CONFIG_DIR / "sites.json"
STATE_FILE = CONFIG_DIR / "state.json"

LOG_DIR = CONFIG_DIR / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

LOG_FILE = LOG_DIR / "app.log"