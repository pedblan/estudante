import tkinter as tk
from tkinter import PhotoImage, filedialog, scrolledtext
from src.gui.transcricao import TranscricaoGUI
from src.gui.resumo import ResumoGUI
from src.gui.ocr import OCRGUI
from src.gui.edicao import EdicaoGUI
from PIL import Image, ImageTk
from ..requisitos import verificar_api_key
import webbrowser

api_available = verificar_api_key()

class MainGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Estudante v1.1")

        self.root.iconbitmap("src/gui/icone.ico")

        # Frame para organizar os botões horizontalmente
        button_frame = tk.Frame(root)
        button_frame.pack(pady=10)

        # Função para criar cada botão com ícone e texto
        def create_icon_button(frame, image_path, text, command, state=tk.NORMAL):
            image = Image.open(image_path)
            image = image.resize((50, 50), Image.LANCZOS)  # Redimensionar para tamanho padrão
            icon = ImageTk.PhotoImage(image)
            button = tk.Button(frame, image=icon, text=text, compound="top", command=command, state=state)
            button.image = icon
            button.pack(side="left", padx=10)

        # Botões principais com ícones
        create_icon_button(button_frame, "src/gui/transcrever.png", "Transcrever", self.abrir_transcricao)
        create_icon_button(button_frame, "src/gui/resumir.png", "Resumir", self.abrir_resumo,
                           state=tk.NORMAL if api_available else tk.DISABLED)
        create_icon_button(button_frame, "src/gui/ocr.png", "OCR", self.abrir_ocr,
                           state=tk.NORMAL if api_available else tk.DISABLED)
        create_icon_button(button_frame, "src/gui/editar.png", "Editar", self.abrir_edicao)
        create_icon_button(button_frame, "src/gui/leia_me.png", "Leia-me", self.abrir_leiame_html,
                           state=tk.NORMAL if api_available else tk.DISABLED)

        # Créditos
        credit_label = tk.Label(root, text=f"Desenvolvido por Pedro Duarte Blanco", fg="blue", cursor="hand2",
                                font=("Arial", 14))
        credit_label.pack(pady=(2, 15))
        credit_label.bind("<Button-1>", lambda e: webbrowser.open("http://pedblan.wordpress.com"))

    def abrir_transcricao(self):
        nova_janela = tk.Toplevel(self.root)
        TranscricaoGUI(nova_janela)

    def abrir_resumo(self):
        nova_janela = tk.Toplevel(self.root)
        ResumoGUI(nova_janela)

    def abrir_ocr(self):
        nova_janela = tk.Toplevel(self.root)
        OCRGUI(nova_janela)

    def abrir_edicao(self):
        nova_janela = tk.Toplevel(self.root)
        EdicaoGUI(nova_janela)

    def abrir_leiame_html(self):
        # Abre o conteúdo do arquivo leiame.html na própria GUI
        leiame_path = "src/leiame.html"
        with open(leiame_path, "r", encoding="utf-8") as file:
            content = file.read()

        leiame_window = tk.Toplevel(self.root)
        leiame_window.title("Leia-me")
        text_area = scrolledtext.ScrolledText(leiame_window, wrap=tk.WORD, width=80, height=30, font=("Arial", 12))
        text_area.insert(tk.INSERT, content)
        text_area.configure(state='disabled')  # Tornar a área de texto apenas para leitura
        text_area.pack(pady=10, padx=10)







if __name__ == "__main__":
    root = tk.Tk()
    app = MainGUI(root)
    root.mainloop()