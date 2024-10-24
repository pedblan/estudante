#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright (c) 2024 Pedro Duarte Blanco
#
# Este software é distribuído sob a Licença MIT.
# Consulte o arquivo LICENSE para obter mais informações.

"""Constam deste script todas as funções que empregam IA para processar as demandas."""
import spacy
from docx import Document
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

from openai import OpenAI
import whisper
import os
import tiktoken

MODELO_ANALISE = "gpt-4o"
MODELO_TRANSCRICAO_API = "whisper-1"  # Empregado quando API==True
WHISPER_MODE = ['tiny', 'base', 'small', 'medium', 'large']  # Define o modelo Whisper como "base" por padrão

def get_openai_client():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise EnvironmentError("A chave da API OpenAI não foi encontrada nas variáveis de ambiente.")
    return OpenAI(api_key=api_key)

def verificar_tokens(texto, modelo=MODELO_ANALISE, limite_tokens=8192):
    """Verifica se o número de tokens de um texto excede o limite permitido. Retorna True ou False."""
    codificador = tiktoken.encoding_for_model(modelo)
    tokens = codificador.encode(texto)
    num_tokens = len(tokens)

    if num_tokens > limite_tokens:
        print(f"O número de tokens ({num_tokens}) excede o limite permitido ({limite_tokens}).")
        return False
    else:
        print(f"Sucesso: O número de tokens ({num_tokens}) está dentro do limite permitido.")
        return True


def resumir_texto(texto, modelo=MODELO_ANALISE, modo='geral', instrucao_personalizada=None):
    """Recorre à API da OpenAI para resumir texto segundo instrução do usuário. Retorna texto resumido."""
    client = get_openai_client()
    try:
        if modo == 'geral':
            instrucao = (
                "Você ajuda um analista de textos jornalísticos, políticos, jurídicos ou culturais. "
                "Sua função é a de sumarizar textos longos, destacando em tópicos os seguintes pontos:\n"
                "- principais pressupostos e premissas implícitas\n"
                "- pontos principais do argumento\n"
                "- detalhes e exemplos de cada ponto principal\n"
                "- identifique vulnerabilidades e possíveis vieses da argumentação."
            )
        elif modo == 'jurisprudencia':
            instrucao = (
                "Identifique a controvérsia jurídica em tela. Indique os argumentos empregados, "
                "identificando aquele que norteou o voto vencedor. Identifique vulnerabilidades nesse argumento."
            )
        elif modo == 'personalizado' and instrucao_personalizada:
            instrucao = instrucao_personalizada

        response = client.chat.completions.create(
            model=f"{modelo}",
            messages=[
                {"role": "system", "content": instrucao},
                {"role": "user", "content": f"Analise a argumentação do seguinte texto: {texto}."}
            ],
            temperature=0.5,
            max_tokens=4000,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        return response.choices[0].message.content

    except Exception as e:
        return f"Ocorreu um erro ao tentar resumir o texto: {str(e)}"

def transcrever(arquivo_de_audio, idioma, api):
    """Recebe um arquivo de áudio e realiza a transcrição usando API da OpenAI ou Whisper Local."""
    client = get_openai_client()
    try:
        if api:
            with open(arquivo_de_audio, "rb") as audio_file:
                return client.audio.transcriptions.create(
                    model=MODELO_TRANSCRICAO_API,
                    file=audio_file,
                    language=idioma
                ).text
        else:
            model = whisper.load_model(WHISPER_MODE[1]) # seleciona o modelo 'base'
            return model.transcribe(arquivo_de_audio, language=idioma)['text']

    except Exception as e:
        return f"Erro ao transcrever o áudio: {str(e)}"

def ajustar_texto(texto, modelo=MODELO_ANALISE):
    client = get_openai_client()
    try:
        instrucao = (
            "Você é um revisor de texto especializado em ajustar textos importados de imagens fotografadas.\n"
            "Os textos foram importados mediante OCR (tesseract).\n"
            "Você deve:"
            "- detectar o idioma em que o texto está escrito e ajustar erros decorrentes do mau reconhecimento de letras e palavras."
            "- completar lacunas decorrentes do mau enquadramento do livro na fotografia, indicando com {completado} quando tiver feito isso\n"
            "- retornar o texto integral, com os ajustes."
        )

        response = client.chat.completions.create(
            model=f"{modelo}",
            messages=[
                {"role": "system", "content": instrucao},
                {"role": "user", "content": f"Ajuste a redação do seguinte texto: {texto}. Retorne todo o texto, com os devidos ajustes feitos."}
            ],
            temperature=1,
            max_tokens=8000,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        return response.choices[0].message.content

    except Exception as e:
        return f"Ocorreu um erro ao tentar ajustar o texto: {str(e)}"

def dividir_texto(texto):
    ...


def revisar(caminho_arquivo, idioma):
    if idioma == 'pt':
        nlp = spacy.load('pt_core_news_md')
    if idioma == 'en':
        nlp = spacy.load('en_core_web_md')
    def is_passive(verb):
        return 'Voice=Pass' in verb.morph
    def add_highlight(run):
        highlight = parse_xml(r'<w:highlight {} w:val="yellow"/>'.format(nsdecls('w')))
        run._r.get_or_add_rPr().append(highlight)

    doc = Document(caminho_arquivo)

    for para in doc.paragraphs:
        doc_para = nlp(para.text)
        runs = []

        # Percorre cada token e aplica o destaque conforme necessário
        for token in doc_para:
            run = para.add_run(token.text)
            if token.pos_ in ['ADJ', 'ADV'] or (token.pos_ == 'VERB' and is_passive(token)):
                add_highlight(run)
            runs.append(run)

            # Adiciona o espaço em branco após o token
            if token.whitespace_:
                run = para.add_run(token.whitespace_)
                runs.append(run)

        # Substitui o conteúdo do parágrafo preservando a formatação original
        para.clear()
        for run in runs:
            para._element.append(run._element)

    titulo = os.path.splitext(os.path.basename(caminho_arquivo))[0]

    return titulo, doc
