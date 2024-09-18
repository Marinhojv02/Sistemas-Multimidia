import re
from ._base_compressor import BaseCompressor
import os

class RleCompressor(BaseCompressor):
    def __init__(self):
        super().__init__()
        
    def compress(self, file_path: str) -> str:
        text: str = super().read_text(file_path=file_path)

        substrings: set = self.get_substrings(text=text)
        compressed = self.run_length_encoding_substrings(text, substrings)

        compressed_file_path = super()._add_suffix_to_filename(file_path, '_rle_compressed', '.rle')
        super().write_text(text=compressed, file_path=compressed_file_path)

        return compressed_file_path

    def decompress(self, file_path: str) -> str:
        text: str = super().read_text(file_path=file_path)

        decompressed: str = self.run_length_encoding_decompress(text)

        decompressed_file_path = super()._add_suffix_to_filename(file_path, '_rle_decompressed', '.rle')
        super().write_text(text=decompressed, file_path=decompressed_file_path)

        return decompressed_file_path

    def get_substrings(self, text: str) -> set:
        pattern = r"(.+?)\1+"
        matches = re.finditer(pattern, text)
        result = set()

        for match in matches:
            result.add(match.group(1))

        return result

    def run_length_encoding_substrings(self, text: str, substrings: set):
        replacements = []
        
        for substring in substrings:
            pattern = f"({re.escape(substring)})+"
            matches = re.finditer(pattern, text)
            
            for match in matches:
                full_match = match.group(0)
                count = len(full_match) // len(substring)
                if count > 2:
                    replacements.append((full_match, f"{count}{substring}#"))

        for full_match, compressed in replacements:
            text = text.replace(full_match, compressed)

        return text
    
    def run_length_encoding_decompress(self, text: str):
        pattern = r"(\d+)([a-zA-Z]+)#"

        matches = re.finditer(pattern, text)

        for match in matches:
            substring = match.group(2)
            count = int(match.group(1))
            text = text.replace(f"{count}{substring}#", substring * count)

        return text