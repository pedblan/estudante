#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright (c) 2024 Pedro Duarte Blanco
#
# Este software é distribuído sob a Licença MIT.
# Consulte o arquivo LICENSE para obter mais informações.



"""Constam deste módulo todas as funções que empregam IA para processar as demandas."""
from openai import OpenAI
import whisper
import os


MODELO_ANALISE = "gpt-4o"
MODELO_TRANSCRICAO_API = "whisper-1"  # Empregado quando API==True
WHISPER_MODE = ['tiny', 'base', 'small', 'medium', 'large']  # Define o modelo Whisper como "base" por padrão

def get_openai_client():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise EnvironmentError("A chave da API OpenAI não foi encontrada nas variáveis de ambiente.")
    return OpenAI(api_key=api_key)

def tiktoken(texto, modelo=MODELO_ANALISE, limite_tokens=8192):
    """Verifica se o número de tokens de um texto excede o limite permitido."""
    codificador = tiktoken.encoding_for_model(modelo)
    tokens = codificador.encode(texto)
    num_tokens = len(tokens)

    if num_tokens > limite_tokens:
        print(f"Erro: O número de tokens ({num_tokens}) excede o limite permitido ({limite_tokens}).")
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
