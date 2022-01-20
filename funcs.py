import json
import os


def get_config(absolute_path):
    if os.path.isfile(absolute_path):
        with open(absolute_path) as file:
            config = json.loads(file.read())
    return config
