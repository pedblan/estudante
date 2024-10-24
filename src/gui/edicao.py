import tkinter as tk
from tkinter import filedialog
from src.tarefas_principais import revisar_docx

class EdicaoGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Revisar")
        self.idioma_var = tk.StringVar(value="pt")

        # Frame para upload de DOCX
        tk.Label(root, text="Escolha o arquivo DOCX:").pack()
        tk.Button(root, text="Selecionar arquivo DOCX", command=self.selecionar_docx_file).pack(pady=10)

        # Frame para escolha do idioma
        self.idioma_frame = tk.Frame(root)
        tk.Label(self.idioma_frame, text="Escolha o idioma:").pack()
        idioma_options = ["pt", "en"]
        self.idioma_menu = tk.OptionMenu(self.idioma_frame, self.idioma_var, *idioma_options)
        self.idioma_menu.pack()
        self.idioma_frame.pack(pady=5)

        tk.Button(root, text="Enviar", command=self.enviar_edicao).pack(pady=10)



    def selecionar_docx_file(self):
        self.docx_file_path = filedialog.askopenfilename(filetypes=[("Word Files", "*.docx")])

    def enviar_edicao(self):
        if hasattr(self, 'docx_file_path'):
            revisar_docx(self.docx_file_path, self.idioma_var.get())

