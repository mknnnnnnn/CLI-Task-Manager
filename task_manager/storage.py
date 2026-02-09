import json
from pathlib import Path


class StorageError(Exception):
    pass

def load_task(path):
    p = Path(path)

    if not p.exists():
        return []

    try:
        with p.open(mode= "r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        raise StorageError("Uszkodzony plik JSON") from e
    except OSError as e:
        raise StorageError("Błąd odczytu") from e
    
    if not isinstance(data, list):
        raise StorageError("Json musi zawierać listę zadań")

    return data

def save_task(path, task):
    p = Path(path)

    try:
        p.write_text(json.dumps(task, ensure_ascii=False, indent=2), encoding="utf-8")
    except OSError as e:
        raise StorageError("Błąd zapisu") from e