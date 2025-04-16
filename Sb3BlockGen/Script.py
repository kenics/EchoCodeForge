class Script:
    def __init__(self, starting_block=None):
        self.starting_block = starting_block
        self.blocks = []  # 手動追加されたブロックを保持
        if starting_block:
            starting_block.topLevel = True
            self.blocks.append(starting_block)

    def add_block(self, block):
        """古い set_next チェーン形式にも対応可能"""
        if not self.starting_block:
            self.starting_block = block
            block.topLevel = True
        else:
            current = self.starting_block
            while current.next:
                current = current.next
            current.set_next(block)

    def collect_blocks(self):
        """project.json の blocks フィールド出力用"""
        return self.blocks  # append されたブロックをそのまま返す
