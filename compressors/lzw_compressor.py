from ._base_compressor import BaseCompressor
from struct import *

class LzwCompressor(BaseCompressor):
    def __init__(self):
        super().__init__()
        
    def compress(self, file_path: str) -> str:
        text: str = super().read_text(file_path=file_path)

        size = len(text.encode('utf-8'))
        compressed_data: str = self.lzw_compress(uncompressed=text, size=size)

        compressed_file_path = super()._add_suffix_to_filename(file_path, '_lzw_compressed', '.lzw')
        
        super().write_compressed_text(text=compressed_data, file_path=compressed_file_path)

        return compressed_file_path

    def decompress(self, file_path: str) -> str:
        text: str = super().read_compressed_text(file_path=file_path)

        decompressed: str = self.lzw_decompress(compressed=text)

        decompressed_file_path = super()._add_suffix_to_filename(file_path, '_lzw_decompressed', '.lzw')
        super().write_text(text=decompressed, file_path=decompressed_file_path)

        return decompressed_file_path

    def lzw_compress(self, uncompressed: str, size: int) -> list:
        maximum_table_size = pow(2,int(size))    

        dictionary_size = 256                   
        dictionary = {chr(i): i for i in range(dictionary_size)}    
        string = ""
        compressed_data = []

        for symbol in uncompressed:                     
            string_plus_symbol = string + symbol
            if string_plus_symbol in dictionary: 
                string = string_plus_symbol
            else:
                compressed_data.append(dictionary[string])
                if(len(dictionary) <= maximum_table_size):
                    dictionary[string_plus_symbol] = dictionary_size
                    dictionary_size += 1
                string = symbol

        if string in dictionary:
            compressed_data.append(dictionary[string])

        return compressed_data

    def lzw_decompress(self, compressed) -> str:
        decompressed_data = ""
        string = ""
        next_code = 256

        dictionary_size = 256
        dictionary = dict([(x, chr(x)) for x in range(dictionary_size)])

        for code in compressed:
            if not (code in dictionary):
                dictionary[code] = string + (string[0])
            decompressed_data += dictionary[code]
            if not(len(string) == 0):
                dictionary[next_code] = string + (dictionary[code][0])
                next_code += 1
            string = dictionary[code]
            
        return decompressed_data