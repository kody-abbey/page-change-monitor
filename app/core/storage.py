# core/storage.py
import json

def load_json(path, default):
    if not path.exists():
        save_json(path, default)
        return default
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except:
        return []

def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)