import uuid

class Block:
    def __init__(self, opcode=None, inputs=None, type=None):
        self.id = str(uuid.uuid4())
        self.opcode = opcode or type
        self.inputs = inputs or {}
        self.values = []
        self.next = None
        self.parent = None
        self.x = 100
        self.y = 100
        self.topLevel = False

    def set_next(self, next_block):
        self.next = next_block
        next_block.parent = self
        return next_block  # チェーン式に使えるように

    def to_dict(self):
        if self.values:
            for i, val in enumerate(self.values):
                if hasattr(val, 'type') and hasattr(val, 'value'):
                    self.inputs[f"ARG{i+1}"] = [1, [val.value]]
                    
        input_format = {}
        for k, v in self.inputs.items():
            if isinstance(v, str):
                input_format[k] = [1, [v]]
            elif isinstance(v, (int, float)):
                input_format[k] = [1, [v]]
            else:
                input_format[k] = v  # 高度な型用

        return {
            "opcode": self.opcode,
            "next": self.next.id if self.next else None,
            "parent": self.parent.id if self.parent else None,
            "inputs": input_format,
            "fields": {},
            "shadow": False,
            "topLevel": self.topLevel,
            "x": self.x,
            "y": self.y
        }
