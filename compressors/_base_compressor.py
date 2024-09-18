import os
from struct import pack, unpack

class BaseCompressor:
    def __init__(self):
        ...

    def read_text(self, file_path: str):
            try:
                with open(file_path, 'r') as arquivo:
                    conteudo = arquivo.read()
                return conteudo
            except FileNotFoundError:
                print(f"O arquivo {file_path} não foi encontrado.")
                return None
            except Exception as e:
                print(f"Ocorreu um erro ao ler o arquivo: {e}")
                return None

    def read_compressed_text(self, file_path: str):
            try:
                with open(file_path, "rb") as file:
                    compressed_data = []

                    while True:
                        rec = file.read(2)
                        if len(rec) != 2:
                            break
                        (data, ) = unpack('>H', rec)
                        compressed_data.append(data)
                return compressed_data
            except FileNotFoundError:
                print(f"O arquivo {file_path} não foi encontrado.")
                return None
            except Exception as e:
                print(f"Ocorreu um erro ao ler o arquivo: {e}")
                return None

    def write_text(self, text: str, file_path: str):
        try:
            with open(file_path, 'w') as arquivo:
                arquivo.write(text)
        except Exception as e:
            print(f"Ocorreu um erro ao escrever no arquivo: {e}")
            
    def write_compressed_text(self, text: str, file_path: str):
        try:
            output_file = open(file_path, "wb")
            for data in text:
                output_file.write(pack('>H',int(data)))
                
            output_file.close()
        except Exception as e:
            print(f"Ocorreu um erro ao escrever no arquivo: {e}")

    def compress(self, file_path: str) -> str:
        raise Exception("Função não implementada")
    
    def decompress(self, file_path: str) -> str:
        raise Exception("Função não implementada")
    
    def _add_suffix_to_filename(self, file_path: str, suffix: str, file_extension: str) -> str:
        file_name, extension = os.path.splitext(file_path)
        return f"{file_name}{suffix}{file_extension}"