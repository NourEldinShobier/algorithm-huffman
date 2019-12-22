class HuffmanNode:
    def __init__(self, byte, freq=0, left=None, right=None):
        self.byte = byte
        self.freq = freq
        self.left = left
        self.right = right

    def __lt__(self, other):
        return self.freq < other.freq

    def isLeaf(self):
        return self.left is None and self.right is None
