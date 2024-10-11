#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright (c) 2024 Pedro Duarte Blanco
#
# Este software é distribuído sob a Licença MIT.
# Consulte o arquivo LICENSE para obter mais informações.

import platform
import subprocess
from src.gui import rodar  # Importa a função que inicializa a interface

# Função para verificar se o ffmpeg está instalado
def verificar_ffmpeg_instalado():
    try:
        subprocess.run(["ffmpeg", "-version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("FFmpeg não está instalado ou não está no PATH.")
        return False

# Função para solicitar autorização do usuário
def pedir_autorizacao():
    resposta = input("FFmpeg não está instalado. Deseja instalá-lo agora? (s/n): ").strip().lower()
    return resposta == 's'

# Função para instalar ffmpeg no macOS
def instalar_ffmpeg_mac():
    try:
        subprocess.run(["brew", "install", "ffmpeg"], check=True)
        print("FFmpeg instalado com sucesso!")
    except subprocess.CalledProcessError:
        print("Erro ao tentar instalar o FFmpeg. Certifique-se de que o Homebrew está instalado.")

# Função para instalar ffmpeg no Linux
def instalar_ffmpeg_linux():
    try:
        subprocess.run(["sudo", "apt", "install", "-y", "ffmpeg"], check=True)
        print("FFmpeg instalado com sucesso!")
    except subprocess.CalledProcessError:
        print("Erro ao tentar instalar o FFmpeg. Certifique-se de que o apt está funcionando corretamente.")

# Função para instalar ffmpeg no Windows
def instalar_ffmpeg_windows():
    try:
        subprocess.run(["choco", "install", "ffmpeg", "-y"], check=True)
        print("FFmpeg instalado com sucesso!")
    except subprocess.CalledProcessError:
        print("Erro ao tentar instalar o FFmpeg. Certifique-se de que o Chocolatey está instalado.")

# Função para verificar e instalar ffmpeg com base no sistema operacional
def verificar_ou_instalar_ffmpeg():
    if verificar_ffmpeg_instalado():
        return

    if pedir_autorizacao():  # Solicita autorização do usuário
        sistema = platform.system()
        if sistema == "Darwin":  # macOS
            instalar_ffmpeg_mac()
        elif sistema == "Linux":  # Linux
            instalar_ffmpeg_linux()
        elif sistema == "Windows":  # Windows
            instalar_ffmpeg_windows()
        else:
            print(f"Sistema operacional {sistema} não suportado para instalação automática do FFmpeg.")
    else:
        print("Instalação do FFmpeg foi cancelada pelo usuário.")

# Função principal para inicializar o app
def main():
    verificar_ou_instalar_ffmpeg()
    rodar()  # Chama a função de iniciar a interface, que agora está em outro arquivo

if __name__ == "__main__":
    main()
