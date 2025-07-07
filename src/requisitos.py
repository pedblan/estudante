import subprocess
import os
import stat
import platform
from pathlib import Path
from src.paths import OUTPUT_DIR


def definir_permissoes(diretorio: Path = OUTPUT_DIR) -> bool:
    """Define permissões para o diretório informado."""
    try:
        os.chmod(diretorio, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)
        return True
    except Exception:
        return False

def verificar_api_key() -> bool:
    """Verifica se a chave da API está configurada.

    Returns:
        bool: True se a chave da API estiver configurada, False caso contrário.
    """
    return os.getenv("OPENAI_API_KEY") is not None

def verificar_ffmpeg_instalado() -> bool:
    """Verifica se o FFmpeg está instalado e disponível no PATH.

    Returns:
        bool: True se o FFmpeg estiver instalado, False caso contrário.
    """
    try:
        subprocess.run(["ffmpeg", "-version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
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
        return False

import subprocess
import os
import platform

def instalar_tesseract() -> bool:
    """Instala o Tesseract OCR usando o gerenciador de pacotes nativo do sistema operacional."""
    sistema = platform.system()
    try:
        if sistema == "Darwin":  # macOS
            subprocess.run(["brew", "install", "tesseract"], check=True)
        elif sistema == "Windows":
            subprocess.run(["winget", "install", "--id", "UB-Mannheim.Tesseract-OCR", "-e"], check=True)
        else:
            return False
        return True
    except subprocess.CalledProcessError:
        return False

def instalar_ffmpeg() -> bool:
    """Instala o FFmpeg usando o gerenciador de pacotes nativo do sistema operacional."""
    sistema = platform.system()
    try:
        if sistema == "Darwin":  # macOS
            subprocess.run(["brew", "install", "ffmpeg"], check=True)
        elif sistema == "Windows":
            subprocess.run(["winget", "install", "--id", "Gyan.FFmpeg", "-e"], check=True)
        else:
            return False
        return True
    except subprocess.CalledProcessError:
        return False

def garantir_pacotes_no_path() -> bool:
    """Garante que os pacotes Tesseract e FFmpeg estejam no PATH."""
    sistema = platform.system()
    if sistema == "Darwin":  # macOS
        os.environ["PATH"] += ":/usr/local/bin"
    elif sistema == "Windows":
        os.environ["PATH"] += ";C:\\Program Files\\Tesseract-OCR;C:\\Program Files\\ffmpeg\\bin"
    else:
        return False
    return True
