import json
import os

from src.constant import home_path


class ConfigManager:

    def __init__(self, file_path: str):
        self.file_path = file_path
        conf_path = os.path.dirname(os.path.abspath(file_path))
        os.makedirs(conf_path, exist_ok=True)
        if not os.path.exists(file_path):
            open(file_path, "w")

    def _read(self):
        with open(self.file_path, "r", encoding="utf-8") as f:
            content = f.read() or "{}"
            return json.loads(content)

    def _save(self, conf: dict):
        with open(self.file_path, "w", encoding="utf-8") as f:
            f.write(json.dumps(conf))

    def get(self, k, default=None):
        return self._read().get(k, default)

    def set(self, k, v):
        conf = self._read()
        conf[k] = v
        self._save(conf)


class PicRecordManager:
    _PATH = os.path.join(home_path, ".easy_pic/record.json")
    conf_path = os.path.dirname(os.path.abspath(_PATH))
    os.makedirs(conf_path, exist_ok=True)
    if not os.path.exists(_PATH):
        open(_PATH, "w")

    @classmethod
    def add_record(cls, data: dict):
        with open(cls._PATH, "a") as f:
            f.write(json.dumps(data) + "\n")

    @classmethod
    def read_records(cls, lines=20):
        res = []
        with open(cls._PATH, "r") as f:
            for x in f:
                res.insert(0, json.loads(x))
                if len(res) > lines:
                    res.pop()
        return res


default_path = os.path.join(home_path, ".easy_pic/default.json")
default_config_manager = ConfigManager(default_path)

if __name__ == '__main__':
    # for i in range(20):
    #     PicRecordManager.add_record({i: 2})
    print(PicRecordManager.read_records(3))
