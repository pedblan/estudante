import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
from src.tarefas_principais import revisar_docx

class EdicaoGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Revisar")
        self.idioma_var = tk.StringVar(value="pt")

        # Imagem no topo da janela
        image = Image.open("src/gui/editar.png")
        image = image.resize((100, 100), Image.LANCZOS)  # Redimensionar a imagem
        icon = ImageTk.PhotoImage(image)
        image_label = tk.Label(root, image=icon)
        image_label.image = icon  # Manter referência
        image_label.pack(pady=10)

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

        # Botão Enviar
        self.enviar_button = tk.Button(root, text="Enviar", command=self.enviar_edicao, state=tk.DISABLED)
        self.enviar_button.pack(pady=10)

    def selecionar_docx_file(self):
        self.docx_file_path = filedialog.askopenfilename(filetypes=[("Word Files", "*.docx")])
        if self.docx_file_path:
            self.enviar_button.config(state=tk.NORMAL)

    def enviar_edicao(self):
        if hasattr(self, 'docx_file_path'):
            revisar_docx(self.docx_file_path, self.idioma_var.get())

