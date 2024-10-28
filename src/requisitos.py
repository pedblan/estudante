import subprocess
import os

def verificar_api_key() -> bool:
    """Verifica se a chave da API está configurada.

    Returns:
        bool: True se a chave da API estiver configurada, False caso contrário.
    """
    api_key = os.getenv('OPENAI_API_KEY')
    if api_key is not None:
        return True
    return False

def verificar_ffmpeg_instalado() -> bool:
    """Verifica se o FFmpeg está instalado e disponível no PATH.

    Returns:
        bool: True se o FFmpeg estiver instalado, False caso contrário.
    """
    try:
        subprocess.run(["ffmpeg", "-version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("FFmpeg não está instalado ou não está no PATH. Instale o ffmpeg. Disponível em https://www.ffmpeg.org. Caso o instalador pergunte, peça para adicionar o programa à variável de ambiente PATH.")
        return False

def verificar_tesseract_instalado() -> bool:
    """Verifica se o Tesseract OCR está instalado e disponível no PATH.

    Returns:
        bool: True se o Tesseract OCR estiver instalado, False caso contrário.
    """
    try:
        subprocess.run(["tesseract", "--version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("Tesseract OCR não está instalado ou não está no PATH. Instale o Tesseract OCR. Disponível em https://github.com/tesseract-ocr/tesseract. Caso o instalador pergunte, peça para adicionar o programa à variável de ambiente PATH.")
        return False


def verificar_requisitos_sistema() -> bool:
    """Verifica se os requisitos do sistema estão atendidos.

    Returns:
        bool: True se todos os requisitos estiverem atendidos, False caso contrário.
    """
    if not verificar_api_key():
        print("OpenAI API KEY não encontrada na variável de ambiente. Iniciando versão lite do programa.")
    if verificar_ffmpeg_instalado() and verificar_tesseract_instalado():
        return True
    return False
