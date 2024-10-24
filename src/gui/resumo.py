import tkinter as tk
from tkinter import filedialog
from src.tarefas_principais import pdf_docx
from PIL import Image, ImageTk



class ResumoGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Resumir")

        # Imagem no topo da janela
        image = Image.open("src/gui/resumir.png")
        image = image.resize((100, 100), Image.LANCZOS)  # Redimensionar a imagem
        icon = ImageTk.PhotoImage(image)
        image_label = tk.Label(root, image=icon)
        image_label.image = icon  # Manter referência
        image_label.pack(pady=10)

        # Frame para upload de PDF/DOCX
        tk.Label(root, text="Escolha o arquivo PDF ou DOCX:").pack()
        tk.Button(root, text="Selecionar arquivo PDF/DOCX", command=self.selecionar_pdf_file).pack(pady=10)

        # Frame para escolher o modo de resumo
        self.modo_var = tk.StringVar(value="geral")
        tk.Radiobutton(root, text="Modo Geral", variable=self.modo_var, value="geral").pack()
        tk.Radiobutton(root, text="Modo Jurisprudência", variable=self.modo_var, value="jurisprudencia").pack()
        tk.Radiobutton(root, text="Modo Personalizado", variable=self.modo_var, value="personalizado").pack()

        # Campo de instrução personalizada (inicialmente escondido)
        self.instrucao_personalizada_text = tk.Text(root, height=4, width=50)
        self.instrucao_personalizada_text.pack_forget()
        self.modo_var.trace('w', self.toggle_instrucao_personalizada)

        # Botão Enviar
        self.enviar_button = tk.Button(root, text="Enviar", command=self.enviar_resumo, state=tk.DISABLED)
        self.enviar_button.pack(pady=10)

    def selecionar_pdf_file(self):
        self.pdf_file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf"), ("Word Files", "*.docx")])
        if self.pdf_file_path:
            self.enviar_button.config(state=tk.NORMAL)

    def toggle_instrucao_personalizada(self, *args):
        if self.modo_var.get() == 'personalizado':
            self.instrucao_personalizada_text.pack(pady=10)
        else:
            self.instrucao_personalizada_text.pack_forget()

    def enviar_resumo(self):
        # Lógica para processar o PDF/DOCX
        modo_resumo = self.modo_var.get()
        instrucao_personalizada = self.instrucao_personalizada_text.get("1.0",
                                                                        tk.END).strip() if modo_resumo == "personalizado" else None
        if hasattr(self, 'pdf_file_path'):
            pdf_docx(self.pdf_file_path, modo_resumo, instrucao_personalizada)
