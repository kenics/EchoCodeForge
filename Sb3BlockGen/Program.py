import uuid

class Program:
    def __init__(self):
        self.sprites = []
        self.variables = {}
        self.variable_added = False  #ユーザー定義の変数が追加されたかどうか
        self.sounds = []
        self.stage_costumes = [] # ステージ用コスチューム(背景)

    def add_stage_costume(self, name, assetId, dataFormat="svg", rotationCenterX=240, rotationCenterY=180):
        md5ext = f"{assetId}.{dataFormat}"
        self.stage_costumes.append({
            "name": name,
            "dataFormat": dataFormat,
            "assetId": assetId,
            "md5ext": md5ext,
            "rotationCenterX": rotationCenterX,
            "rotationCenterY": rotationCenterY
        })


    def add_sprite(self, sprite: "Sprite"):
        self.sprites.append(sprite)
    
    def add_variable(self, name, initial_value=0):
        self.variable_added = True
        var_id = str(uuid.uuid4())
        self.variables[var_id] = [name, initial_value]
        return var_id
    
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
    
    def to_project_json(self):
        if not self.variables:
            default_id = "`jEk@4|i[#Fk?(8x)AV.-my variable"
            self.variables[default_id] = ["変数", 0]

        if not self.sounds:
            self.sounds.append({
                "name": "ポップ",
                "assetId": "83a9787d4cb6f3b7632b4ddfebf74367",
                "dataFormat": "wav",
                "format": "",
                "rate": 48000,
                "sampleCount": 1123,
                "md5ext": "83a9787d4cb6f3b7632b4ddfebf74367.wav"
            })
        
        # コスチューム未定義の場合「背景1」を追加
            if not self.stage_costumes:
                self.stage_costumes.append({
                    "name": "背景1",
                    "dataFormat": "svg",
                    "assetId": "cd21514d0531fdffb22204e0ec5ed84a",
                    "md5ext": "cd21514d0531fdffb22204e0ec5ed84a.svg",
                    "rotationCenterX": 240,
                    "rotationCenterY": 180
                })
        
        stage = {
            "isStage": True,
            "name": "Stage",
            "variables": self.variables,
            "lists": {},
            "broadcasts": {},
            "blocks": {},
            "currentCostume": 0,
            "costumes": self.stage_costumes,
            "sounds": self.sounds,
            "volume": 100,
            "layerOrder": 0,
            "tempo": 60,
            "videoTransparency": 50,
            "videoState": "on",
            "textToSpeechLanguage": None
        }

        return {
            "targets": [stage] + [s.to_scratch_format() for s in self.sprites],
            "monitors": [],
            "extensions": [],
            "meta": {
                "semver": "3.0.0",
                "vm": "11.0.0-beta.2",
                "agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36"
            }
        }
