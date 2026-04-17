import logging
from pathlib import Path
from logging.handlers import RotatingFileHandler

BASE_DIR = Path(__file__).resolve().parents[2]
LOG_DIR = BASE_DIR / "logs"
LOG_FILE = LOG_DIR / "app.log"

file_handler = RotatingFileHandler(
    LOG_FILE,
    maxBytes=1_000_000,  # 1MB
    backupCount=3
)

def setup_logger():
    LOG_DIR.mkdir(exist_ok=True)

    logger = logging.getLogger("app")
    logger.setLevel(logging.INFO)

    # 重複防止
    if logger.hasHandlers():
        return logger

    formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(message)s"
    )

    # ファイル出力
    file_handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
    file_handler.setFormatter(formatter)

    # コンソール出力
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger