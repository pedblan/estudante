import tkinter as tk
from tkinter import filedialog
from tarefas_principais import pdf_ocr


class OCRGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("OCR de Documentos PDF")

        # Frame para upload de PDF
        tk.Label(root, text="Escolha o arquivo PDF:").pack()
        tk.Button(root, text="Selecionar arquivo PDF", command=self.selecionar_pdf_file).pack(pady=10)

        # Botão Enviar
        tk.Button(root, text="Enviar", command=self.enviar_ocr).pack(pady=10)

    def selecionar_pdf_file(self):
        self.pdf_file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])

    def enviar_ocr(self):
        # Lógica para processar o PDF com OCR
        if hasattr(self, 'pdf_file_path'):
            pdf_ocr(self.pdf_file_path)
