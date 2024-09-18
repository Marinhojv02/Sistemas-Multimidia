import time
import os
from compressors.rle_compressor import RleCompressor
from compressors.lzw_compressor import LzwCompressor
from compressors._base_compressor import BaseCompressor

def medir_tempo_compressao_descompressao(base_path: str, original_file: str, compressor: BaseCompressor):
    try:
        file_path = os.path.join(base_path, original_file)

        original_text = BaseCompressor().read_text(file_path=file_path)

        if not original_text:
            return

        tamanho_original = len(original_text.encode('utf-8'))

        inicio_compressao = time.time()
        compressed_file_path = compressor.compress(file_path=file_path)
        fim_compressao = time.time()

        if not os.path.exists(compressed_file_path):
            print(f"Arquivo comprimido não encontrado: {compressed_file_path}")
            return

        tamanho_comprimido = os.path.getsize(compressed_file_path)

        inicio_descompressao = time.time()
        descomprimido_file_path = compressor.decompress(file_path=compressed_file_path)
        fim_descompressao = time.time()

        if not os.path.exists(descomprimido_file_path):
            print(f"Arquivo descomprimido não encontrado: {descomprimido_file_path}")
            return

        tamanho_descomprimido = os.path.getsize(descomprimido_file_path)

        porcentagem_reducao = ((tamanho_original - tamanho_comprimido) / tamanho_original) * 100

        print(f"Tamanho do texto original: {tamanho_original} bytes")
        print(f"Tamanho do texto comprimido: {tamanho_comprimido} bytes")
        print(f"Tamanho do texto descomprimido: {tamanho_descomprimido} bytes")
        print(f"Porcentagem de redução: {porcentagem_reducao:.2f}%")

        print(f"Tempo de compressão: {fim_compressao - inicio_compressao:.4f} segundos")
        print(f"Tempo de descompressão: {fim_descompressao - inicio_descompressao:.4f} segundos")
    except Exception as e:
        print(e)
if __name__ == "__main__":
    base_path = './files'
    original_file = '1000_bytes.txt'
    
    print('|******************* LZW COMPRESSOR *******************|')
    lzw_compressor = LzwCompressor()
    medir_tempo_compressao_descompressao(base_path=base_path, original_file=original_file, compressor=lzw_compressor)
    print('|------------------------------------------------------|')
    
    print('|******************* RLE COMPRESSOR *******************|')
    rle_compressor = RleCompressor()
    medir_tempo_compressao_descompressao(base_path=base_path, original_file=original_file, compressor=rle_compressor)
    print('|------------------------------------------------------|')