#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright (c) 2024 Pedro Duarte Blanco
#
# Este software é distribuído sob a Licença MIT.
# Consulte o arquivo LICENSE para obter mais informações.

import subprocess
from src.interface import rodar  # Importa a função que inicializa a interface

# Função para verificar se o ffmpeg está instalado
def verificar_ffmpeg_instalado():
    try:
        subprocess.run(["ffmpeg", "-version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("FFmpeg não está instalado ou não está no PATH. Instale o ffmpeg. Disponível em https://www.ffmpeg.org. Caso o instalador pergunte, peça para adicionar o programa à variável de ambiente PATH.")
        return False


# Função principal para inicializar o app
def main():
    if verificar_ffmpeg_instalado():
        rodar()  # Chama a função de iniciar a interface, que agora está em outro arquivo

if __name__ == "__main__":
    main()
