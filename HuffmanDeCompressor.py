from huffmanNode import HuffmanNode
import array


class HuffmanDeCompressor:
    def __init__(self):
        self.fileName = ''
        self.fileExtension = ''

    def decompressFile(self, inputFileName: str):
        self.fileName = inputFileName.split('.')[0]
        self.fileExtension = inputFileName.split('.')[1]

        outputFileName = f"{self.fileName}.{self.fileExtension}"

        fileBytes: str = self.readFile(inputFileName)
        decodedBytes: list = self.decode(fileBytes)

        self.save(outputFileName, decodedBytes)

    def readFile(self, inputFileName: str):
        inputFile = open(inputFileName, "rb")
        encodedBytes = ""

        # Read the file byte by byte
        byte = inputFile.read(1)

        while len(byte) > 0:
            encodedBytes += f"{bin(ord(byte))[2:]:0>8}"
            byte = inputFile.read(1)

        return encodedBytes

    def decode(self, encodedBytes: str):
        # Convert bytes to stream (list) of bits.
        bitsStream = list(encodedBytes)
        # --> bits stream contains (tree,padding,compressed data)
        tree = self.decodeTree(bitsStream)
        reversedLookupTable = self.buildReversedLookupTable(tree)
        # --> bits stream contains (padding,compressed data)
        bitsStream = self.removePadding(bitsStream)
        # --> bits stream contains (compressed data)

        encodedBytes = ''.join(bitsStream)

        outputBytes = []
        byteKey = ''

        for bit in encodedBytes:
            byteKey += bit
            byteValue = reversedLookupTable.get(byteKey)

            if byteValue is not None:
                outputBytes.append(byteValue)
                byteKey = ''

        return outputBytes

    def decodeTree(self, bitsStream):
        # bitsStream: List of bits

        bit = bitsStream[0]
        del bitsStream[0]

        if bit == "1":
            # Leaf node
            # Read the byte value
            byte = ""
            for _ in range(8):
                byte += bitsStream[0]
                del bitsStream[0]

            return HuffmanNode(int(byte, 2))
        else:
            # Internal node
            left = self.decodeTree(bitsStream)
            right = self.decodeTree(bitsStream)

            return HuffmanNode(None, left=left, right=right)

    def removePadding(self, bitsStream):
        numOfZeros_Bin = bitsStream[:8]
        numOfZeros_Int = int("".join(numOfZeros_Bin), 2)
        bitsStream = bitsStream[8:]
        bitsStream = bitsStream[numOfZeros_Int:]

        return bitsStream

    def buildReversedLookupTable(self, huffmanTree: HuffmanNode):
        lookupTable = {}

        self.buildReversedLookupTableImpl(huffmanTree, "", lookupTable)

        # If the file contains single repeated byte
        if len(lookupTable) == 1:
            key = next(iter(lookupTable))
            lookupTable[key] = '1'

        # Return reversed lookupTable

        return {v: k for k, v in lookupTable.items()}

    def buildReversedLookupTableImpl(self, node: HuffmanNode, code, lookupTable):
        if node.isLeaf():
            lookupTable[node.byte] = code
        else:
            self.buildReversedLookupTableImpl(node.left, code + "0", lookupTable)
            self.buildReversedLookupTableImpl(node.right, code + "1", lookupTable)

    def save(self, outputFileName: str, outputBytesNum):
        outputBytes = ''

        for num in outputBytesNum:
            outputBytes += format(num, '08b')

        b_arr = bytearray()

        for i in range(0, len(outputBytes), 8):
            b_arr.append(int(outputBytes[i:i + 8], 2))

        outputFile = open(f"OP-{outputFileName}", "wb")
        outputFile.write(b_arr)

    def decompress_folder(self, folder):

        total_bytes: str = self.readFile(folder)
        decoded_bytes: list = self.decode(total_bytes)
        splitted = array.array('B', decoded_bytes).tobytes().split(b'\x11\x22\x33')

        for i, file in enumerate(splitted[0:len(splitted) - 1]):
            self.save(str(i) + '.' + splitted[i][0:3].decode("utf-8"), splitted[i][3:len(splitted[i])])
