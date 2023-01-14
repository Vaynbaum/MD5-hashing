import json
import os


def read_json_file(filename):
    with open(filename, "r", encoding="utf-8") as f:
        return json.load(f)


def read_full_file(filename):
    with open(filename, "r", encoding="utf-8") as f:
        return f.read()


def create_not_exist_dir(path):
    if not os.path.isdir(path):
        os.mkdir(path)


def write_json_file(filename, data):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)


def write_file(filename, data):
    with open(filename, "w", encoding="utf-8") as f:
        f.write(data)
