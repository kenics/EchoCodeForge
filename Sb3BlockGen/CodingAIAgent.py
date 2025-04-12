from openai import OpenAI
import traceback
import re
from Config.ConfigLoader import ConfigLoader


class CodingAIAgent:
    def __init__(self):
        self.config = ConfigLoader()
        self.model = self.config.get("default_model", "gpt-4")
        self.api_key = self.config.get("openai_api_key")
        if not self.api_key:
            raise ValueError("APIキーが設定ファイルにありません: 'openai_api_key'")

        self.client = OpenAI(api_key=self.api_key)

        self.dsl_globals = {}
        self._prepare_dsl_env()

    def _prepare_dsl_env(self):
        from Sb3BlockGen.Block import Block
        from Sb3BlockGen.Script import Script
        from Sb3BlockGen.Sprite import Sprite
        from Sb3BlockGen.Program import Program
        from Sb3BlockGen.Value import Value  # 使う場合のみ定義

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
        self.save_as_sb3(project_json, "output.sb3")

    def ask_chatgpt_for_dsl(self, prompt: str) -> str:
        system_message = {
            "role": "system",
            "content": (
                "あなたはScratch DSLを使ってプロジェクトを生成するPythonコーディングAIです。\n"
                "次のルールに従ってください：\n"
                "- 使用できるクラスは Program, Sprite, Script, Block, Value のみです。\n"
                "- import 文（例：from scratch.dsl ...）は書かないでください。\n"
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

        # コードブロックの中だけを抽出
        code_blocks = re.findall(r"```(?:python)?\n(.*?)```", full_text, re.DOTALL)
        return code_blocks[0].strip() if code_blocks else full_text.strip()

    def execute_dsl_code(self, dsl_code: str):
        try:
            exec(dsl_code, self.dsl_globals)
            return self.dsl_globals.get("program")
        except Exception:
            traceback.print_exc()
            return None

    def save_as_sb3(self, project_json: dict, filename: str):
        import os, zipfile, json

        temp_dir = "temp_scratch"
        os.makedirs(temp_dir, exist_ok=True)

        with open(os.path.join(temp_dir, "project.json"), "w", encoding="utf-8") as f:
            json.dump(project_json, f, ensure_ascii=False, indent=2)

        # ダミー画像（コスチューム必須）
        asset_id = "f996b84d5ba4a93f7d31c52e3fd5a3ed"
        svg_path = os.path.join(temp_dir, f"{asset_id}.svg")
        with open(svg_path, "w", encoding="utf-8") as f:
            f.write("<svg xmlns='http://www.w3.org/2000/svg' width='96' height='100'></svg>")

        with zipfile.ZipFile(filename, "w") as z:
            z.write(os.path.join(temp_dir, "project.json"), arcname="project.json")
            z.write(svg_path, arcname=f"{asset_id}.svg")

        print(f"[DONE] sb3ファイルを生成しました: {filename}")
