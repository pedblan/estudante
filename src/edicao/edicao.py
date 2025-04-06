import tkinter as tk
from tkinter import filedialog
from typing import Union

from PIL import Image, ImageTk

from src.utils import gravar_documento, abrir_doc_produzido
from src.utils_ia import revisar
from src.utils_gui import imagem_na_janela_secundaria

class EdicaoGUI:
    def __init__(self, root: tk.Tk) -> None:
        """Inicializa a GUI de edição.

        Args:
            root (tk.Tk): A instância raiz do Tkinter.
        """
        self.root = root
        self.root.title("Revisar")
        self.idioma_var = tk.StringVar(value="pt")

        self.caminho_arquivo_imagem = "src/edicao/editar.png"

        # Imagem no topo da janela
        imagem_na_janela_secundaria(self.root, self.caminho_arquivo_imagem)

        # Frame para upload de DOCX
        tk.Label(root, text="Escolha o arquivo DOCX:").pack()
        tk.Button(root, text="Selecionar arquivo DOCX", command=self.selecionar_docx).pack(pady=10)

        # Frame para escolha do idioma
        self.frame_idioma = tk.Frame(root)
        tk.Label(self.frame_idioma, text="Escolha o idioma:").pack()
        opcoes_idioma = ["pt", "en"]
        self.menu_idioma = tk.OptionMenu(self.frame_idioma, self.idioma_var, *opcoes_idioma)
        self.menu_idioma.pack()
        self.frame_idioma.pack(pady=5)

        # Botão Enviar
        self.botao_enviar = tk.Button(root, text="Enviar", command=self.enviar_edicao, state=tk.DISABLED)
        self.botao_enviar.pack(pady=10)

    def selecionar_docx(self) -> None:
        """Abre um diálogo para selecionar um arquivo DOCX."""
        self.caminho_docx = filedialog.askopenfilename(filetypes=[("Word Files", "*.docx")])
        if self.caminho_docx:
            self.botao_enviar.config(state=tk.NORMAL)

    def enviar_edicao(self) -> None:
        """Envia o arquivo DOCX para revisão."""
        if hasattr(self, 'caminho_docx'):
            revisar_docx(self.caminho_docx, self.idioma_var.get())


def revisar_docx(caminho_arquivo: str, idioma: str) -> Union[bool, None]:
    """Revisa um documento Word, destacando adjetivos, advérbios e verbos na voz passiva.

    Args:
        caminho_arquivo (str): Caminho do arquivo Word.
        idioma (str): Idioma do texto.

    Returns:
        Union[bool, None]: True se o documento foi aberto com sucesso, None caso contrário.
    """
    try:
        titulo, doc = revisar(caminho_arquivo, idioma)
        caminho_arquivo_salvo = gravar_documento(titulo, doc)
        return abrir_doc_produzido(caminho_arquivo_salvo)
    except Exception as e:
        print(f"Erro ao processar DOCX: {str(e)}")
        return False

