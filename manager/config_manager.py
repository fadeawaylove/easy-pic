import json
import os

from constant import home_path


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


default_path = os.path.join(home_path, ".easy_pic/default.json")
default_config_manager = ConfigManager(default_path)
