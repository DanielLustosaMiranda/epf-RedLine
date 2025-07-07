import json
import os

DATA_FOLDER = os.path.join(os.path.dirname(__file__), 'data')

def get_data_path(filename):
    os.makedirs(DATA_FOLDER, exist_ok=True)
    return os.path.join(DATA_FOLDER, filename)

def read_data(filename):
    filepath = get_data_path(filename)
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return []

def write_data(filename, data):
    """Escreve dados em um arquivo JSON."""
    filepath = get_data_path(filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)