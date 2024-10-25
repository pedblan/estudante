import subprocess
import os

def verificar_api_key():
    api_key = os.getenv('OPENAI_API_KEY')
    if api_key is not None:
        return True
    return False

def verificar_ffmpeg_instalado():
    try:
        subprocess.run(["ffmpeg", "-version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("FFmpeg não está instalado ou não está no PATH. Instale o ffmpeg. Disponível em https://www.ffmpeg.org. Caso o instalador pergunte, peça para adicionar o programa à variável de ambiente PATH.")
        return False

def verificar_tesseract_instalado():
    import subprocess
    try:
        subprocess.run(["tesseract", "--version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("Tesseract OCR não está instalado ou não está no PATH. Instale o Tesseract OCR. Disponível em https://github.com/tesseract-ocr/tesseract. Caso o instalador pergunte, peça para adicionar o programa à variável de ambiente PATH.")
        return False


