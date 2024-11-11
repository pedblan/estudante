from bs4 import BeautifulSoup
import fitz  # PyMuPDF
from docx import Document  # python-docx
import tkinter as tk

def extrair_texto(caminho_arquivo: str) -> str:
    """Extrai o conteúdo do arquivo de acordo com o tipo.

    Args:
        caminho_arquivo (str): Caminho para o arquivo a ser lido.

    Returns:
        str: O conteúdo do arquivo como texto.
    """
    if caminho_arquivo.endswith(".txt"):
        with open(caminho_arquivo, 'r', encoding='utf-8') as f:
            return f.read()

    elif caminho_arquivo.endswith(".pdf"):
        conteudo = ""
        with fitz.open(caminho_arquivo) as pdf:
            for pagina in pdf:
                conteudo += pagina.get_text()
        return conteudo

    elif caminho_arquivo.endswith(".docx"):
        doc = Document(caminho_arquivo)
        return "\n".join(paragrafo.text for paragrafo in doc.paragraphs)

    elif caminho_arquivo.endswith(".html"):
        with open(caminho_arquivo, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f, 'html.parser')
            return soup.get_text(separator=' ', strip=True)

    else:
        raise ValueError("Formato de arquivo não suportado.")

def centralizar_palavra(label: tk.Label, palavra: str, tamanho_fonte: int, negrito: bool) -> None:
    """Exibe a palavra centralizada na janela, aplicando negrito nas três primeiras letras se solicitado.

    Args:
        label (tk.Label): Label onde a palavra será exibida.
        palavra (str): A palavra a ser exibida.
        tamanho_fonte (int): Tamanho da fonte.
        negrito (bool): Se True, aplica negrito nas três primeiras letras.
    """
    if negrito:
        palavra_formatada = f"**{palavra[:3]}**{palavra[3:]}"
    else:
        palavra_formatada = palavra

    # Configura o label com o tamanho e estilo da fonte
    label.config(text=palavra_formatada, font=("Arial", tamanho_fonte))
    label.place(relx=0.5, rely=0.5, anchor="center")
