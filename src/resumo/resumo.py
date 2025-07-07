import tkinter as tk
from tkinter import filedialog
from typing import Optional, Union

from PIL import Image, ImageTk
from docx import Document

from src.utils import extrair_texto, adicionar_com_subtitulos, gravar_documento, abrir_doc_produzido, limpar_temp
from src.utils_gui import imagem_na_janela_secundaria, BaseWindow
from src.utils_ia import resumir_texto


class ResumoGUI(BaseWindow):
    def __init__(self, root: tk.Tk) -> None:
        """Inicializa a GUI de resumo.

        Args:
            root (tk.Tk): A instância raiz do Tkinter.
        """
        super().__init__(root, "Resumo")
        caminho_arquivo_imagem = "src/resumo/resumir.png"

        # Imagem no topo da janela
        imagem_na_janela_secundaria(self.main_frame, caminho_arquivo_imagem)

        # Frame para upload de texto
        tk.Label(self.main_frame, text="Escolha o arquivo de texto:").pack()
        tk.Button(self.main_frame, text="Selecionar arquivo de texto", command=self.selecionar_texto).pack(pady=10)

        # Seleção do modo de resumo
        tk.Label(self.main_frame, text="Escolha o modo de resumo:").pack()
        self.modo_resumo = tk.StringVar(value="geral")
        modos = [("Geral", "geral"), ("Jurisprudência", "jurisprudencia"), ("Retórica", "retorica"), ("Personalizado", "personalizado")]
        for texto, valor in modos:
            tk.Radiobutton(self.main_frame, text=texto, variable=self.modo_resumo, value=valor, command=self.toggle_prompt).pack(anchor=tk.W)

        # Caixa de texto para o prompt personalizado
        self.prompt_text = tk.Text(self.main_frame, height=10, width=50)
        self.prompt_text.pack(padx=20, pady=10)
        self.prompt_text.pack_forget()

        # Botão Enviar
        self.botao_enviar = tk.Button(self.main_frame, text="Enviar", command=self.enviar_resumo, state=tk.DISABLED if not hasattr(self, 'caminho_texto') else tk.NORMAL)
        self.botao_enviar.pack(pady=10)

    def selecionar_texto(self) -> None:
        """Abre um diálogo para selecionar um arquivo de texto."""
        self.caminho_texto = filedialog.askopenfilename(filetypes=[("PDF", "*.pdf"), ("DOCX", "*.docx"), ("TXT", "*.txt")])
        if self.caminho_texto:
            self.botao_enviar.config(state=tk.NORMAL)

    def toggle_prompt(self) -> None:
        """Alterna a visibilidade do prompt personalizado."""
        if self.modo_resumo.get() == "personalizado":
            self.prompt_text.pack(padx=20, pady=10)
        else:
            self.prompt_text.pack_forget()

    def enviar_resumo(self) -> None:
        """Envia o arquivo de texto para resumo."""
        if hasattr(self, 'caminho_texto'):
            instrucao_personalizada = self.prompt_text.get("1.0", tk.END) if self.modo_resumo.get() == "personalizado" else None
            pdf_docx(self.caminho_texto, self.modo_resumo.get(), instrucao_personalizada)

def pdf_docx(caminho_arquivo: str, modo_resumo: str, instrucao_personalizada: Optional[str] = None) -> Union[bool, None]:
    """Processa o resumo de um arquivo PDF ou DOCX e salva o resultado em um documento Word.

    Args:
        caminho_arquivo (str): Caminho do arquivo PDF ou DOCX.
        modo_resumo (str): Modo de resumo ('geral', 'jurisprudencia' ou 'personalizado').
        instrucao_personalizada (Optional[str]): Instrução personalizada para o resumo.

    Returns:
        Union[bool, None]: True se o documento foi aberto com sucesso, None caso contrário.
    """
    try:
        titulo, texto = extrair_texto(caminho_arquivo)
        resumo = resumir_texto(texto, modo=modo_resumo, instrucao_personalizada=instrucao_personalizada)
        doc = Document()
        doc = adicionar_com_subtitulos(doc, resumo)
        caminho_arquivo_salvo = gravar_documento(titulo, doc)
        return abrir_doc_produzido(caminho_arquivo_salvo)
    except Exception as e:
        print(f"Erro ao processar PDF ou DOCX: {str(e)}")
        return False
    finally:
        limpar_temp()
