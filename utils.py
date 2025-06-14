import yaml
import requests
import os

def save_audio_from_url(url, file_path):
    # Ensure the output directory exists
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    res = requests.get(url)
    with open(file_path, "wb") as f:
        f.write(res.content)

def load_config(path):
    with open(path, "r") as f:
        return yaml.safe_load(f)
