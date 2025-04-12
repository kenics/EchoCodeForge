class Script:
    def __init__(self, starting_block: "Block"):
        self.starting_block = starting_block
        self.starting_block.topLevel = True

    def collect_blocks(self):
        current = self.starting_block
        collected = []
        while current:
            collected.append(current)
            current = current.next
        return collected
