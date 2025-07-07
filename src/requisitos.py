import subprocess
import os
import stat
import platform
from src.paths import OUTPUT_DIR


def definir_permissoes() -> None:
    """Define permissões de leitura, escrita e execução para o diretório especificado."""
    try:
        os.chmod(OUTPUT_DIR, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)
    except PermissionError:
        print(f"Permissão negada ao tentar definir permissões para {OUTPUT_DIR}. Rode o programa com privilégios de administrador.")
    except Exception as e:
        print(f"Erro ao definir permissões: {e}")

def verificar_api_key() -> bool:
    """Verifica se a chave da API está configurada.

    Returns:
        bool: True se a chave da API estiver configurada, False caso contrário.
    """
    api_key = os.getenv('OPENAI_API_KEY')
    if api_key is not None:
        return True
    print("OpenAI API KEY não encontrada na variável de ambiente. Você terá funcionalidades limitadas.")
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

import subprocess
import os
import platform

def instalar_tesseract() -> None:
    """Instala o Tesseract OCR usando o gerenciador de pacotes nativo do sistema operacional."""
    sistema = platform.system()
    try:
        if sistema == "Darwin":  # macOS
            subprocess.run(["brew", "install", "tesseract"], check=True)
        elif sistema == "Windows":
            subprocess.run(["winget", "install", "--id", "UB-Mannheim.Tesseract-OCR", "-e"], check=True)
        else:
            print(f"Sistema operacional {sistema} não suportado para instalação automática do Tesseract.")
    except subprocess.CalledProcessError as e:
        print(f"Erro ao instalar o Tesseract: {e}")

def instalar_ffmpeg() -> None:
    """Instala o FFmpeg usando o gerenciador de pacotes nativo do sistema operacional."""
    sistema = platform.system()
    try:
        if sistema == "Darwin":  # macOS
            subprocess.run(["brew", "install", "ffmpeg"], check=True)
        elif sistema == "Windows":
            subprocess.run(["winget", "install", "--id", "Gyan.FFmpeg", "-e"], check=True)
        else:
            print(f"Sistema operacional {sistema} não suportado para instalação automática do FFmpeg.")
    except subprocess.CalledProcessError as e:
        print(f"Erro ao instalar o FFmpeg: {e}")

def garantir_pacotes_no_path() -> None:
    """Garante que os pacotes Tesseract e FFmpeg estejam no PATH."""
    sistema = platform.system()
    if sistema == "Darwin":  # macOS
        os.environ["PATH"] += ":/usr/local/bin"
    elif sistema == "Windows":
        os.environ["PATH"] += ";C:\\Program Files\\Tesseract-OCR;C:\\Program Files\\ffmpeg\\bin"
    else:
        print(f"Sistema operacional {sistema} não suportado para configuração automática do PATH.")
