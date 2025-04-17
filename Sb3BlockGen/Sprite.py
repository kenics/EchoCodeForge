from Sb3BlockGen.Script import Script  # 必要な型ヒント・依存関係
from Sb3BlockGen.Block import Block    # blocks に Block を追加する前提なら必要
from Sb3BlockGen.Value import Value    # inputs に Value 型を使う前提なら必要

class Sprite:
    def __init__(self, name="Sprite1"):
        self.name = name
        self.scripts = []
        self.sounds = []
        self.costumes = []

    def add_script(self, script: "Script"):
        self.scripts.append(script)

    def add_sound(self, name, assetId, dataFormat="wav", format="", rate=48000, sampleCount=1123):
        md5ext = f"{assetId}.{dataFormat}"
        sound = {
            "name": name,
            "assetId": assetId,
            "dataFormat": dataFormat,
            "format": format,
            "rate": rate,
            "sampleCount": sampleCount,
            "md5ext": md5ext
        }
        self.sounds.append(sound)

    def add_costume(self, name, assetId, dataFormat="svg", rotationCenterX=240, rotationCenterY=180):
        md5ext = f"{assetId}.{dataFormat}"
        self.costumes.append({
            "name": name,
            "assetId": assetId,
            "dataFormat": dataFormat,
            "md5ext": md5ext,
            "rotationCenterX": rotationCenterX,
            "rotationCenterY": rotationCenterY
        })

    def to_scratch_format(self):
        blocks = {}
        for script in self.scripts:
            script.link_blocks()
            for block in script.collect_blocks():
                blocks[block.id] = block.to_dict()

        # デフォルトのサウンド（なければ「ニャー」を追加）
        if not self.sounds:
            self.sounds.append({
                "name": "ニャー",
                "assetId": "83c36d806dc92327b9e7049a565c6bff",
                "dataFormat": "wav",
                "format": "",
                "rate": 48000,
                "sampleCount": 40681,
                "md5ext": "83c36d806dc92327b9e7049a565c6bff.wav"
            })

        # デフォルトのコスチューム（なければ2枚追加）
        if not self.costumes:
            self.costumes.extend([
                {
                    "name": "コスチューム1",
                    "bitmapResolution": 1,
                    "dataFormat": "svg",
                    "assetId": "bcf454acf82e4504149f7ffe07081dbc",
                    "md5ext": "bcf454acf82e4504149f7ffe07081dbc.svg",
                    "rotationCenterX": 48,
                    "rotationCenterY": 50
                },
                {
                    "name": "コスチューム2",
                    "bitmapResolution": 1,
                    "dataFormat": "svg",
                    "assetId": "0fb9be3e8397c983338cb71dc84d0b25",
                    "md5ext": "0fb9be3e8397c983338cb71dc84d0b25.svg",
                    "rotationCenterX": 46,
                    "rotationCenterY": 53
                }
            ])

        return {
            "isStage": False,
            "name": self.name,
            "variables": {},
            "lists": {},
            "broadcasts": {},
            "blocks": blocks,
            "currentCostume": 0,
            "costumes": self.costumes,
            "sounds": self.sounds,
            "volume": 100,
            "layerOrder": 1,
            "visible": True,
            "x": 0,
            "y": 0,
            "size": 100,
            "direction": 90,
            "draggable": False,
            "rotationStyle": "all around"
        }
