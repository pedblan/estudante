import tkinter as tk
from tkinter import filedialog
from typing import Union
import pikepdf, os
from PIL import Image, ImageTk
from docx import Document
from dotenv import load_dotenv
from src.utils import reconhecer_ocr, adicionar_com_subtitulos, gravar_documento, abrir_doc_produzido
from src.utils_gui import imagem_na_janela_secundaria, BaseWindow
from src.requisitos import verificar_tesseract_instalado

load_dotenv()
ajustar_com_api = os.getenv("USAR_API_OCR", "False") == "True"

tesseract_instalado : bool = verificar_tesseract_instalado()



class PDFGUI(BaseWindow):
    def __init__(self, root: tk.Tk) -> None:
        """Inicializa a GUI de OCR e desbloqueio de PDF.

        Args:
            root (tk.Tk): A instância raiz do Tkinter.
        """
        super().__init__(root, "PDF")

        self.caminho_arquivo_imagem = "src/pdf/pdf.png"

        # Imagem no topo da janela
        imagem_na_janela_secundaria(self.main_frame, self.caminho_arquivo_imagem)

        # Frame para upload de PDF
        tk.Label(self.main_frame, text="Escolha o arquivo PDF:").pack()
        tk.Button(self.main_frame, text="Selecionar arquivo PDF", command=self.selecionar_pdf).pack(pady=10)

        # Frame para escolha do modo
        self.modo_var = tk.StringVar(value="ocr")
        tk.Label(self.main_frame, text="Escolha o modo:").pack()
        tk.Radiobutton(
            self.main_frame,
            text="OCR",
            variable=self.modo_var,
            value="ocr",
            state=tk.NORMAL if tesseract_instalado else tk.DISABLED,
        ).pack(anchor=tk.W)
        tk.Radiobutton(self.main_frame, text="Desbloquear", variable=self.modo_var, value="desbloquear").pack(anchor=tk.W)

        # Botão Enviar
        self.botao_enviar = tk.Button(self.main_frame, text="Enviar", command=self.enviar, state=tk.DISABLED)
        self.botao_enviar.pack(pady=10)

    def selecionar_pdf(self) -> None:
        """Abre um diálogo para selecionar um arquivo PDF."""
        self.caminho_pdf = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
        if self.caminho_pdf:
            self.botao_enviar.config(state=tk.NORMAL)

    def enviar(self) -> None:
        """Envia o arquivo PDF para o processamento selecionado."""
        if hasattr(self, 'caminho_pdf'):
            if self.modo_var.get() == "ocr":
                pdf_ocr(self.caminho_pdf, ajustar_com_api)
            elif self.modo_var.get() == "desbloquear":
                desbloquear(self.caminho_pdf)


def pdf_ocr(caminho_arquivo: str, ajustar_com_api) -> Union[bool, None]:
    """Processa o reconhecimento de texto em um arquivo PDF usando OCR e salva o resultado em um documento Word.

    Args:
        caminho_arquivo (str): Caminho do arquivo PDF.

    Returns:
        Union[bool, None]: True se o documento foi aberto com sucesso, None caso contrário.
    """
    print("Processando OCR...")
    try:
        titulo, texto = reconhecer_ocr(caminho_arquivo, ajustar_com_api)
        doc = Document()
        doc = adicionar_com_subtitulos(doc, texto)
        caminho_arquivo_salvo = gravar_documento(titulo, doc)
        return abrir_doc_produzido(caminho_arquivo_salvo)
    except Exception as e:
        print(f"Erro ao processar PDF: {str(e)}")
        return False

def desbloquear(caminho_arquivo: str) -> Union[bool, None]:
    """
    Desbloqueia um arquivo PDF protegido e salva as alterações.

    Args:
        caminho_arquivo (str): O caminho do arquivo PDF a ser desbloqueado.

    Returns:
        Union[bool, None]: Retorna True se o PDF foi desbloqueado com sucesso,
        None caso contrário.
    """
    try:
        print("Desbloqueando PDF...")
        with pikepdf.open(caminho_arquivo, allow_overwriting_input=True) as pdf:
            pdf.save(caminho_arquivo)
        print(f"PDF {caminho_arquivo} desbloqueado com sucesso!")
        return True
    except Exception as e:
        print(f"Erro no desbloqueio do PDF: {str(e)}")
        return False
