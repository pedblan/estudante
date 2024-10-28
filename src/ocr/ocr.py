import tkinter as tk
from tkinter import filedialog
from typing import Union

from PIL import Image, ImageTk
from docx import Document

from src.utils import reconhecer_ocr, adicionar_com_subtitulos, gravar_documento, abrir_doc_produzido
from src.utils_gui import imagem_na_janela_secundaria, checkbox_mostrar_log_simplificado

class OCRGUI:
    def __init__(self, root: tk.Tk) -> None:
        """Inicializa a GUI de OCR.

        Args:
            root (tk.Tk): A instância raiz do Tkinter.
        """
        self.root = root
        self.root.title("OCR")

        self.caminho_arquivo_imagem = "src/ocr/ocr.png"

        # Imagem no topo da janela
        imagem_na_janela_secundaria(self.root, self.caminho_arquivo_imagem)

        # Frame para upload de PDF
        tk.Label(root, text="Escolha o arquivo PDF:").pack()
        tk.Button(root, text="Selecionar arquivo PDF", command=self.selecionar_pdf).pack(pady=10)

        # Botão Enviar
        self.botao_enviar = tk.Button(root, text="Enviar", command=self.enviar_ocr, state=tk.DISABLED)
        self.botao_enviar.pack(pady=10)

    def selecionar_pdf(self) -> None:
        """Abre um diálogo para selecionar um arquivo PDF."""
        self.caminho_pdf = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
        if self.caminho_pdf:
            self.botao_enviar.config(state=tk.NORMAL)

    def enviar_ocr(self) -> None:
        """Envia o arquivo PDF para processamento OCR."""
        if hasattr(self, 'caminho_pdf'):
            pdf_ocr(self.caminho_pdf)


def pdf_ocr(caminho_arquivo: str) -> Union[bool, None]:
    """Processa o reconhecimento de texto em um arquivo PDF usando OCR e salva o resultado em um documento Word.

    Args:
        caminho_arquivo (str): Caminho do arquivo PDF.

    Returns:
        Union[bool, None]: True se o documento foi aberto com sucesso, None caso contrário.
    """
    print("Processando OCR...")
    try:
        titulo, texto = reconhecer_ocr(caminho_arquivo)
        doc = Document()
        doc = adicionar_com_subtitulos(doc, texto)
        caminho_arquivo_salvo = gravar_documento(titulo, doc)
        return abrir_doc_produzido(caminho_arquivo_salvo)
    except Exception as e:
        print(f"Erro ao processar PDF: {str(e)}")
        return False
