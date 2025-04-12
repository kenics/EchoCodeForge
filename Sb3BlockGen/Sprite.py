class Sprite:
    def __init__(self, name="Sprite1"):
        self.name = name
        self.scripts = []

    def add_script(self, script: "Script"):
        self.scripts.append(script)

    def to_scratch_format(self):
        blocks = {}
        for script in self.scripts:
            for block in script.collect_blocks():
                blocks[block.id] = block.to_dict()

        costume = {
            "assetId": "f996b84d5ba4a93f7d31c52e3fd5a3ed",
            "name": "costume1",
            "bitmapResolution": 1,
            "md5ext": "f996b84d5ba4a93f7d31c52e3fd5a3ed.svg",
            "dataFormat": "svg",
            "rotationCenterX": 48,
            "rotationCenterY": 50
        }

        return {
            "isStage": False,
            "name": self.name,
            "variables": {},
            "lists": {},
            "broadcasts": {},
            "blocks": blocks,
            "currentCostume": 0,
            "costumes": [costume],
            "sounds": [],
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
