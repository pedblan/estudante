import tkinter as tk
from tkinter import filedialog
from tarefas_principais import pdf_docx


class ResumoGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Resumo de Documentos")

        # Frame para upload de PDF/DOCX
        tk.Label(root, text="Escolha o arquivo PDF ou DOCX:").pack()
        tk.Button(root, text="Selecionar arquivo PDF/DOCX", command=self.selecionar_pdf_file).pack(pady=10)

        # Frame para escolher o modo de resumo
        self.modo_var = tk.StringVar(value="geral")
        tk.Radiobutton(root, text="Modo Geral", variable=self.modo_var, value="geral").pack()
        tk.Radiobutton(root, text="Modo Jurisprudência", variable=self.modo_var, value="jurisprudencia").pack()
        tk.Radiobutton(root, text="Modo Personalizado", variable=self.modo_var, value="personalizado").pack()

        # Campo de instrução personalizada
        self.instrucao_personalizada_text = tk.Text(root, height=4, width=50)
        self.instrucao_personalizada_text.pack()

        # Botão Enviar
        tk.Button(root, text="Enviar", command=self.enviar_resumo).pack(pady=10)

    def selecionar_pdf_file(self):
        self.pdf_file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf"), ("Word Files", "*.docx")])

    def enviar_resumo(self):
        # Lógica para processar o PDF/DOCX
        modo_resumo = self.modo_var.get()
        instrucao_personalizada = self.instrucao_personalizada_text.get("1.0",
                                                                        tk.END).strip() if modo_resumo == "personalizado" else None
        if hasattr(self, 'pdf_file_path'):
            pdf_docx(self.pdf_file_path, modo_resumo, instrucao_personalizada)
