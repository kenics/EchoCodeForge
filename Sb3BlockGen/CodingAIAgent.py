from openai import OpenAI
import traceback
import re
import os
from datetime import datetime

from Config.ConfigValidator import ConfigValidator 
from Config.ConfigLoader import ConfigLoader

class CodingAIAgent:
    def __init__(self):
        validator = ConfigValidator(os.path.join(os.path.dirname(__file__), "..", "Config", "config.json"))
        if not validator.canrun:
            raise RuntimeError("設定ファイルの整合性チェックに失敗しました")
        
        self.config = ConfigLoader()
        self.model = self.config.get("default_model", "gpt-4")
        self.api_key = self.config.get_secret("openai_api_key")
        if not self.api_key:
            raise ValueError("APIキーが設定ファイルにありません")
         
        # open AI からの回答を保存するファイルのpathの取得
        self.cache_config = self._load_cache_config()

        self.client = OpenAI(api_key=self.api_key)

        self.dsl_globals = {}
        self._prepare_dsl_env()

    def _load_cache_config(self):
        import json
        path = os.path.join(os.path.dirname(__file__), "cache_config.json")
        if not os.path.exists(path):
            raise FileNotFoundError("キャッシュ設定ファイルが見つかりません")  # ✅ ファイル名を非表示に変更
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    def _prepare_dsl_env(self):
        from Sb3BlockGen.Block import Block
        from Sb3BlockGen.Script import Script
        from Sb3BlockGen.Sprite import Sprite
        from Sb3BlockGen.Program import Program
        from Sb3BlockGen.Value import Value

        self.dsl_globals.update({
            "Block": Block,
            "Script": Script,
            "Sprite": Sprite,
            "Program": Program,
            "Value": Value
        })

    def run(self, user_command: str):
        print(f"[STEP 1] ユーザー命令文を受け取り: {user_command}")
        dsl_code = self.ask_chatgpt_for_dsl(user_command)
        print(f"[STEP 2] 生成されたDSLコード:\n{dsl_code}")

        program = self.execute_dsl_code(dsl_code)
        if program is None:
            print("[ERROR] DSL実行に失敗しました")
            return

        print("[STEP 3] project.json を生成")
        project_json = program.to_project_json()

        print("[STEP 4] sb3ファイルを保存")
        format_str = self.cache_config.get("sb3_filename_format")
        if not format_str:
            raise ValueError("出力ファイル名のフォーマットが設定ファイルにありません（sb3_filename_format）")

        output_dir = self.cache_config.get("sb3_output_dir")
        if not output_dir:
            raise ValueError("出力ディレクトリが設定ファイルにありません（sb3_output_dir）")

        os.makedirs(output_dir, exist_ok=True)

        filename = datetime.now().strftime(format_str)
        full_path = os.path.join(output_dir, filename)
        self.save_as_sb3(project_json, full_path)

    def ask_chatgpt_for_dsl(self, prompt: str) -> str:
        cache_path = self.cache_config.get("response_cache_path")
        if not cache_path:
            raise ValueError("キャッシュ保存パスが設定ファイルに存在しません")

        if self.config.get("load_response_from_file", False):
            print("[INFO] DSLコードをファイルから読み込みます")
            with open(cache_path, "r", encoding="utf-8") as f:
                return f.read()

        if not self.config.get("ai_enabled", True):
            raise RuntimeError("OpenAIへの問い合わせは無効化されています（config.ai_enabled=false）")

        # ChatGPTへの問い合わせ
        system_message = {
            "role": "system",
            "content": (
                "あなたはScratch DSLを使ってプロジェクトを生成するPythonコーディングAIです。\n"
                "次のルールに従ってください：\n"
                "- 使用できるクラスは Program, Sprite, Script, Block, Value のみです。\n"
                "- Blockクラスは .values を使用しません。代わりに inputs[\"ARG1\"] のように設定してください。\n"
                "- import 文（例：from scratch.dsl など）は書かないでください。\n"
                "- コメントや説明を含めず、コードのみを出力してください。\n"
                "- 出力は必ず ```python ... ``` のコードブロックにしてください。\n"
                "- コードブロックの外にテキストや説明を付けないでください。"
            )
        }
        user_message = {"role": "user", "content": prompt}

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[system_message, user_message]
        )

        full_text = response.choices[0].message.content

        # ```python ... ``` の中身だけを抽出
        code_blocks = re.findall(r"```(?:python)?\n(.*?)```", full_text, re.DOTALL)
        dsl_code = code_blocks[0].strip() if code_blocks else full_text.strip()

        if self.config.get("save_response_to_file", False):
            os.makedirs(os.path.dirname(cache_path), exist_ok=True)
            with open(cache_path, "w", encoding="utf-8") as f:
                f.write(dsl_code)
            print("[INFO] DSLコードをファイルに保存しました")

        return dsl_code

    def execute_dsl_code(self, dsl_code: str):
        try:
            exec(dsl_code, self.dsl_globals)
            return self.dsl_globals.get("program")
        except Exception:
            traceback.print_exc()
            return None

    def save_as_sb3(self, project_json: dict, output_path: str):
        import zipfile
        import json
        import os

        timestamp = os.path.splitext(os.path.basename(output_path))[0].replace("output_", "")
        compress = self.config.get("do_compress", True)

        # 出力先ディレクトリを取得（必須設定）
        output_dir = self.cache_config.get("sb3_output_dir")
        if not output_dir:
            raise ValueError("出力ディレクトリが設定ファイルにありません（sb3_output_dir）")
        
        if compress:
            temp_dir = "temp_scratch"
        else:
            temp_dir = os.path.join(output_dir, f"sb3_{timestamp}")
        
        os.makedirs(temp_dir, exist_ok=True)

        # project.json を書き出す
        json_path = os.path.join(temp_dir, "project.json")
        with open(json_path, "w", encoding="utf-8") as f:
            if compress:
                json.dump(project_json, f, ensure_ascii=False, separators=(",", ":"))  # 改行なし
            else:
                json.dump(project_json, f, ensure_ascii=False, indent=2)  # 改行あり（可読）
        # ダミーのSVG（コスチュームファイル）
        
        asset_id = "f996b84d5ba4a93f7d31c52e3fd5a3ed"
        svg_path = os.path.join(temp_dir, f"{asset_id}.svg")
        with open(svg_path, "w", encoding="utf-8") as f:
            f.write("<svg xmlns='http://www.w3.org/2000/svg' width='96' height='100'></svg>")

        if compress:
            with zipfile.ZipFile(output_path, "w") as z:
                z.write(os.path.join(temp_dir, "project.json"), arcname="project.json")
                z.write(svg_path, arcname=f"{asset_id}.svg")

            print(f"[DONE] sb3ファイルを生成しました: {output_path}")
        else:
            print(f"[DONE] sb3ファイルの要素ファイルを保存しました: {temp_dir}")
