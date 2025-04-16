import uuid
from Sb3BlockGen.Value import Value

# type名 → opcode名のマッピング表
OPCODE_MAP = {
    "say": "looks_say",
    "think": "looks_think",
    "move": "motion_move",
    "turnRight": "motion_turnright",
    "turnLeft": "motion_turnleft"
    # 他にも必要ならここに追加
}

class Block:
    def __init__(self, opcode=None, inputs=None, type=None):
        self.id = str(uuid.uuid4())
        self.opcode = OPCODE_MAP.get(opcode or type, opcode or type)
        self.inputs = inputs or {}
        self.values = []
        self.fields = {}
        self.next = None
        self.parent = None
        self.x = 100
        self.y = 100
        self.topLevel = True

    def set_next(self, next_block):
        self.next = next_block
        next_block.parent = self
        return next_block  # チェーン式に使えるように

    def to_dict(self):
        # self.values が存在し、inputs が未設定なら自動補完
        if self.values and not self.inputs:
            for i, val in enumerate(self.values):
                if isinstance(val, Value):
                    self.inputs[f"ARG{i+1}"] = val.as_input()
                elif isinstance(val, str):
                    self.inputs[f"ARG{i+1}"] = [1, [val]]
                elif isinstance(val, (int, float)):
                    self.inputs[f"ARG{i+1}"] = [1, [val]]
                else:
                    self.inputs[f"ARG{i+1}"] = val

        # inputs を Scratch 標準形式へ
        input_format = {}
        for k, v in self.inputs.items():
            if isinstance(v, Value):
                input_format[k] = v.as_input()
            elif isinstance(v, str):
                input_format[k] = [1, [v]]
            elif isinstance(v, (int, float)):
                input_format[k] = [1, [v]]
            else:
                input_format[k] = v  # dict型などそのまま渡す

        return {
            "opcode": self.opcode,
            "next": self.next.id if self.next else None,
            "parent": self.parent.id if self.parent else None,
            "inputs": input_format,
            "fields": self.fields,
            "shadow": False,
            "topLevel": self.topLevel,
            "x": self.x,
            "y": self.y
        }
