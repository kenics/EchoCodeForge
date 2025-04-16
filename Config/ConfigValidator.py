import json
import os
import sys

class ConfigValidator:
    def __init__(self, config_path):
        self.canrun = False
        self._validate(config_path)

    def _validate(self, path):
        if not os.path.exists(path):
            raise FileNotFoundError("設定ファイル(パラメータ)が見つかりません")

        with open(path, "r", encoding="utf-8") as f:
            try:
                config = json.load(f)
            except json.JSONDecodeError:
                raise ValueError("設定ファイル(パラメータ)の形式が不正です")

        # 1) default_model が空でないか
        default_model = config.get("default_model", "").strip()
        if not default_model:
            print("[ERROR] default_model が未設定または空文字列です")
            sys.exit(1)

        # 2) ai_enabled と load_response_from_file は真偽が逆
        ai_enabled = config.get("ai_enabled", False)
        load_from_file = config.get("load_response_from_file", False)
        if ai_enabled == load_from_file:
            print("[ERROR] ai_enabled と load_response_from_file が同じ値です。正反対である必要があります")
            print(f"[ERROR] ai_enabledtrue:{'true' if ai_enabled else 'false'}")
            print(f"[ERROR] load_response_from_file:{'true' if load_from_file else 'false'}")
            sys.exit(1)

        # 3) load_response_from_file = true のとき、save_response_to_file も true
        save_response = config.get("save_response_to_file", False)
        if load_from_file and not save_response:
            print("[ERROR] load_response_from_file が true のときは save_response_to_file も true でなければなりません")
            sys.exit(1)

        # すべて問題なし
        self.canrun = True
