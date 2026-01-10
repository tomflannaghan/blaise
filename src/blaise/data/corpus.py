"""Loads large bodies of text"""

from io import BytesIO
import tarfile
import requests
from blaise.data.core import load_data, save_data

_DATA_TYPE = "corpus"


def load_corpus(name) -> str:
    try:
        return load_data(_DATA_TYPE, name)
    except FileNotFoundError:
        if name in _KNOWN_NAMES:
            data = _KNOWN_NAMES[name]()
            save_data(data, _DATA_TYPE, "en_wiki")
            return data
        raise


def save_corpus(data: str, name: str):
    if name in _KNOWN_NAMES:
        raise ValueError(
            f"Cannot use a known corpus name: {', '.join(_KNOWN_NAMES.keys())}"
        )
    save_data(data, _DATA_TYPE, "en_wiki")


def download_en_wiki() -> str:
    print("Downloading en_wiki")
    req = requests.get(
        "https://github.com/LGDoor/Dump-of-Simple-English-Wiki/raw/refs/heads/master/corpus.tgz"
    )
    req.raise_for_status()
    print("Download succeeded")
    with tarfile.open(fileobj=BytesIO(req.content), mode="r") as f:
        corpus = f.extractfile("corpus.txt")
        if corpus is None:
            raise ValueError("corpus.txt not found")
        raw_data = corpus.read()
    return raw_data.decode()


_KNOWN_NAMES = {"en_wiki": download_en_wiki}
