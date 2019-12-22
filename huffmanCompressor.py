import os
import ctypes
from queue import PriorityQueue
from huffmanNode import HuffmanNode


class FILE_META_INFO(ctypes.Structure):
    _fields_ = [
        # ('name', ctypes.),
        # ('extension', XINPUT_GAMEPAD),
    ]


class HuffmanCompressor:
    def __init__(self):
        self.fileName = ''
        self.queue = PriorityQueue()

    def compressFile(self, inputFileName: str):
        self.fileName = inputFileName

        # Read file as binary
        bytesList = open(inputFileName, 'rb').read()

        frequencyTable = self.buildFrequencyTable(bytesList)
        huffmanTree = self.buildTree(frequencyTable)
        lookupTable = self.buildLookupTable(huffmanTree)
        encodedBytes = self.buildEncodedBytes(bytesList, lookupTable)

        self.save(huffmanTree, encodedBytes)
        self.calcCompressionRatio()

    def buildFrequencyTable(self, bytesList):
        # Convert bytes list to sorted set.
        bytesSet = set(bytesList)

        # Initialize frequencies dictionary.
        frequencyTable = {byte: 0 for byte in bytesSet}

        # Calculate frequency of each byte.
        for byte in bytesList:
            frequencyTable[byte] += 1

        return frequencyTable

    def buildTree(self, frequencyTable):
        for byte, frequency in frequencyTable.items():
            self.queue.put(HuffmanNode(byte, frequency))

        # Build tree
        while self.queue.qsize() > 1:
            left, right = self.queue.get(), self.queue.get()
            parent = HuffmanNode(None, left.freq + right.freq, left, right)
            self.queue.put(parent)

        return self.queue.get()

    def buildLookupTable(self, huffmanTree: HuffmanNode):
        lookupTable = {}

        self.buildLookupTableImpl(huffmanTree, "", lookupTable)

        # If the file contains single repeated byte
        if len(lookupTable) == 1:
            key = next(iter(lookupTable))
            lookupTable[key] = '1'

        return lookupTable

    def buildLookupTableImpl(self, node: HuffmanNode, code, lookupTable):
        if node.isLeaf():
            lookupTable[node.byte] = code
        else:
            self.buildLookupTableImpl(node.left, code + "0", lookupTable)
            self.buildLookupTableImpl(node.right, code + "1", lookupTable)

    def buildEncodedBytes(self, bytesList, lookupTable):
        encodedBytes = ""

        for byte in bytesList:
            encodedBytes += lookupTable[byte]

        return encodedBytes

    def encodeTree(self, node: HuffmanNode, text):
        if node.isLeaf():
            text += "1"
            text += f"{node.byte:08b}"
        else:
            text += "0"
            text = self.encodeTree(node.left, text)
            text = self.encodeTree(node.right, text)

        return text

    def addPadding(self, encodedTree: str, encodedBytes: str):
        num = 8 - (len(encodedBytes) + len(encodedTree)) % 8
        if num != 0:
            encodedBytes = num * "0" + encodedBytes

        return f"{encodedTree}{num:08b}{encodedBytes}"

    def save(self, tree: HuffmanNode, encodedBytes: str):
        encodedTree = self.encodeTree(tree, '')
        outputBytes = self.addPadding(encodedTree, encodedBytes)
        outputFile = open(self.fileName + '.huf', "wb")

        b_arr = bytearray()

        for i in range(0, len(outputBytes), 8):
            b_arr.append(int(outputBytes[i:i + 8], 2))

        outputFile.write(b_arr)

    def calcCompressionRatio(self):
        inputFileName = self.fileName
        outputFileName = self.fileName + '.huf'

        sizeBefore = os.path.getsize(inputFileName)
        sizeAfter = os.path.getsize(outputFileName)
        percent = round(100 - sizeAfter / sizeBefore * 100, 1)

        print(f"before: {sizeBefore}bytes, after: {sizeAfter}bytes, "f"compression {percent}%")

    def compress_folder(self, folder):

        total_bytes = b""
        for file in os.listdir(folder):
            total_bytes += bytes(file.split('.')[1], 'utf8') + open(folder + '\\' + file, 'rb').read() + b'\x11\x22\x33'

        frequency_table = self.buildFrequencyTable(total_bytes)
        huffman_tree = self.buildTree(frequency_table)
        lookup_table = self.buildLookupTable(huffman_tree)
        encoded_bytes = self.buildEncodedBytes(total_bytes, lookup_table)

        self.save(huffman_tree, encoded_bytes)
        # self.calcCompressionRatio()
