import glob
import json
import os
from functools import lru_cache
from typing import Any

BUILT_IN_DATA_PATH = os.path.abspath(os.path.dirname(__file__))
USER_DATA_PATH = os.environ.get("BLAISE_DATA_PATH", os.path.join(os.path.expanduser("~"), ".blaise", "data"))


@lru_cache(10000)
def load_data(data_type: str, data_name: str) -> Any:
    """
    Searches the built in and user defined paths for a data item and returns it. The built in path takes precedence.
    """
    built_in_path = os.path.join(BUILT_IN_DATA_PATH, data_type, f"{data_name}.json")
    user_path = os.path.join(USER_DATA_PATH, data_type, f"{data_name}.json")
    if os.path.exists(built_in_path):
        with open(built_in_path, "r") as f:
            return json.load(f)
    elif os.path.exists(user_path):
        with open(user_path, "r") as f:
            return json.load(f)
    raise FileNotFoundError(f"No data file found for {data_type}/{data_name}")


def save_data(data: Any, data_type: str, data_name: str, save_to_built_in=False):
    """
    Saves data to the user data folder. If data already exists, it will overwrite.
    """
    built_in_path = os.path.join(BUILT_IN_DATA_PATH, data_type, f"{data_name}.json")
    if save_to_built_in:
        path = built_in_path
    elif os.path.exists(built_in_path):
        raise ValueError(f"Cannot overwrite a built in data item {data_type}/{data_name}")
    else:
        path = os.path.join(USER_DATA_PATH, data_type, f"{data_name}.json")

    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        json.dump(data, f)
    load_data.cache_clear()


def list_data(data_type: str, data_name: str = "*") -> list[str]:
    """
    List available data items in a given data type. `data_name` is a glob search string (excl extension)
    """
    file_pattern = f"{data_name}.json"
    data_types = []
    for dir in [BUILT_IN_DATA_PATH, USER_DATA_PATH]:
        for f in glob.glob(os.path.join(dir, data_type, file_pattern)):
            data_types.append(os.path.basename(f).rsplit(".", 1)[0])
    return sorted(set(data_types))
