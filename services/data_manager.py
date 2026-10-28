import json
import os
from config import DATA_DIR


def get_data_path(filename: str) -> str:
    os.makedirs(DATA_DIR, exist_ok=True)
    return os.path.join(DATA_DIR, filename)


def read_data(filename: str) -> list:
    filepath = get_data_path(filename)
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data if isinstance(data, list) else []
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def write_data(filename: str, data: list) -> None:
    filepath = get_data_path(filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def next_id(items: list) -> int:
    if not items:
        return 1
    return max((int(item.get('id', 0)) for item in items if item.get('id') is not None), default=0) + 1
