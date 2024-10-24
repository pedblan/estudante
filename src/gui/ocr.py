import tkinter as tk
from tkinter import filedialog
from src.tarefas_principais import pdf_ocr
from PIL import Image, ImageTk



class OCRGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("OCR")

        # Imagem no topo da janela
        image = Image.open("src/gui/ocr.png")
        image = image.resize((100, 100), Image.LANCZOS)  # Redimensionar a imagem
        icon = ImageTk.PhotoImage(image)
        image_label = tk.Label(root, image=icon)
        image_label.image = icon  # Manter referência
        image_label.pack(pady=10)

        # Frame para upload de PDF
        tk.Label(root, text="Escolha o arquivo PDF:").pack()
        tk.Button(root, text="Selecionar arquivo PDF", command=self.selecionar_pdf_file).pack(pady=10)

        # Botão Enviar
        self.enviar_button = tk.Button(root, text="Enviar", command=self.enviar_ocr, state=tk.DISABLED)
        self.enviar_button.pack(pady=10)

    def selecionar_pdf_file(self):
        self.pdf_file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
        if self.pdf_file_path:
            self.enviar_button.config(state=tk.NORMAL)

    def enviar_ocr(self):
        # Lógica para processar o PDF com OCR
        if hasattr(self, 'pdf_file_path'):
            pdf_ocr(self.pdf_file_path)

