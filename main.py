import time

from HuffmanDeCompressor import HuffmanDeCompressor
from huffmanCompressor import HuffmanCompressor


def main():
    value = input('(1) Compress file:, (2) Compress folder:, (3) Decompress file:, (4) Decompress folder: ')
    name = input('Enter name: ')

    startTime = time.time()

    if value == '1':
        encoder = HuffmanCompressor()
        encoder.compressFile(name)
    elif value == '2':
        encoder = HuffmanCompressor()
        encoder.compress_folder(name)
    elif value == '3':
        decompressor = HuffmanDeCompressor()
        decompressor.decompressFile(name)
    else:
        decompressor = HuffmanDeCompressor()
        decompressor.decompress_folder(name)

    print("\n--- %s seconds ---" % (time.time() - startTime))


main()
