class Value:
    def __init__(self, type, value):
        self.type = type.lower()
        self.value = value

    def as_input(self):
        # Scratch形式: [1, [<type_code>, <value>]]
        type_code_map = {
            "number": 4,
            "string": 10,
            "boolean": 6
        }
        type_code = type_code_map.get(self.type, 10)  # 未知の型は文字列扱い

        return [1, [type_code, self.value]]
