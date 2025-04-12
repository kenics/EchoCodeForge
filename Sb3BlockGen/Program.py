class Program:
    def __init__(self):
        self.sprites = []

    def add_sprite(self, sprite: "Sprite"):
        self.sprites.append(sprite)

    def to_project_json(self):
        stage = {
            "isStage": True,
            "name": "Stage",
            "variables": {},
            "lists": {},
            "broadcasts": {},
            "blocks": {},
            "currentCostume": 0,
            "costumes": [],
            "sounds": [],
            "volume": 100
        }

        return {
            "targets": [stage] + [s.to_scratch_format() for s in self.sprites],
            "monitors": [],
            "extensions": [],
            "meta": {
                "semver": "3.0.0",
                "vm": "0.2.0",
                "agent": "scratch-coding-ai"
            }
        }
