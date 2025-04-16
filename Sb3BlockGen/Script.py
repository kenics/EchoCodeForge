class Script:
    def __init__(self, starting_block=None):
        self.starting_block = starting_block
        self.blocks = []
        if starting_block:
            starting_block.topLevel = True
            self.blocks.append(starting_block)

    def add_block(self, block):
        if not self.starting_block:
            self.starting_block = block
            block.topLevel = True
        else:
            current = self.starting_block
            while current.next:
                current = current.next
            current.set_next(block)

    def collect_blocks(self):
        current = self.starting_block
        collected = []
        while current:
            collected.append(current)
            current = current.next
        return collected
