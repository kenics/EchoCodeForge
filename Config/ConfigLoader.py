import json
import os

class ConfigLoader:
    CONFIG_PATH = os.path.join(os.path.dirname(__file__), 'config.json')  # ✅ 同じディレクトリに固定

    def __init__(self):
        self.config = self.load_config()

    def load_config(self):
        if not os.path.exists(self.CONFIG_PATH):
            raise FileNotFoundError(f"設定ファイルが見つかりません: {self.CONFIG_PATH}")
        with open(self.CONFIG_PATH, "r", encoding="utf-8") as f:
            return json.load(f)

    def get(self, key, default=None):
        return self.config.get(key, default)
