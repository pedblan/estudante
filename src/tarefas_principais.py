#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright (c) 2024 Pedro Duarte Blanco
#
# Este software é distribuído sob a Licença MIT.
# Consulte o arquivo LICENSE para obter mais informações.

"""Este script contém as tarefas principais do aplicativo: transcrever arquivo de áudio, transcrever vídeo de YouTube, resumir documento e abrir arquivo de Leia-me."""

from src.subtarefas import *
import webbrowser
import os


def youtube(youtube_url, idioma, api, max_palavras, com_timestamp):
    """Processa a transcrição de um vídeo de streaming e salva o resultado em um documento Word."""
    try:
        # Baixar áudio do vídeo do YouTube ou outro serviço de streaming
        titulo, caminho_audio_temp = download_yt(youtube_url)

        # Dividir áudio em partes
        _, partes_temp, duracao_total = dividir_audio(caminho_audio_temp)

        # Transcrever as partes
        doc = transcrever_partes(partes_temp, idioma, api, duracao_total, max_palavras, com_timestamp)

        # Salvar o documento
        caminho_arquivo_salvo = gravar_documento(titulo, doc)

        # Abrir o documento Word
        return abrir_doc_produzido(caminho_arquivo_salvo)

    except Exception as e:
        print(f"Erro ao processar vídeo de streaming: {str(e)}")
        return False

    finally:
        limpar_temp()


def audio(caminho_arquivo, idioma, api, max_palavras, com_timestamp):
    """Processa a transcrição de um arquivo de áudio e salva o resultado em um documento Word."""
    try:
        # Dividir o áudio em partes
        titulo, partes_temp, duracao_total = dividir_audio(caminho_arquivo)

        # Transcrever as partes
        doc = transcrever_partes(partes_temp, idioma, api, duracao_total, max_palavras, com_timestamp)

        # Salvar o documento
        caminho_arquivo_salvo = gravar_documento(titulo, doc)

        # Abrir o documento Word
        return abrir_doc_produzido(caminho_arquivo_salvo)

    except Exception as e:
        print(f"Erro ao processar áudio: {str(e)}")
        return False

    finally:
        limpar_temp()


def pdf_docx(caminho_arquivo, modo_resumo, instrucao_personalizada=None):
    """Processa o resumo de um arquivo PDF ou DOCX e salva o resultado em um documento Word."""
    try:
        # Extrair texto do arquivo (pode ser PDF ou DOCX)
        titulo, texto = extrair_texto(caminho_arquivo)

        # Resumir o texto
        resumo = resumir_texto(texto, modo=modo_resumo, instrucao_personalizada=instrucao_personalizada)

        # Adicionar o resumo ao documento Word
        doc = Document()
        doc = adicionar_com_subtitulos(doc, resumo)

        # Salvar o documento
        caminho_arquivo_salvo = gravar_documento(titulo, doc)

        # Abrir o documento Word
        return abrir_doc_produzido(caminho_arquivo_salvo)

    except Exception as e:
        print(f"Erro ao processar PDF ou DOCX: {str(e)}")
        return False

    finally:
        limpar_temp()

def pdf_ocr(caminho_arquivo: str) -> str:
    try:
        titulo, texto = reconhecer_ocr(caminho_arquivo)
        doc = Document()
        doc = adicionar_com_subtitulos(doc, texto)
        caminho_arquivo_salvo = gravar_documento(titulo, doc)
        return abrir_doc_produzido(caminho_arquivo_salvo)
    except Exception as e:
        print(f"Erro ao processar PDF: {str(e)}")
        return False


def abrir_leiame_html():
    # Caminho completo do arquivo leiame.html
    leiame_path = os.path.join(os.getcwd(), 'leiame.html')

    # Verifica se o arquivo existe
    if os.path.exists(leiame_path):
        webbrowser.open(f"file://{leiame_path}")
    else:
        print("Arquivo LEIAME não encontrado.")


def verificar_requisitos_sistema():
    if verificar_ffmpeg_instalado():
        if verificar_tesseract_instalado():
            return True

