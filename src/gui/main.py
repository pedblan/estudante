import tkinter as tk
from src.gui.transcricao import TranscricaoGUI
from src.gui.resumo import ResumoGUI
from src.gui.ocr import OCRGUI
from src.gui.edicao import EdicaoGUI
from src.gui.subtarefas_gui import load_image
import webbrowser
from ..requisitos import verificar_api_key

api_available = verificar_api_key()

class MainGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Estudante v1.1")

        self.root.iconbitmap("src/gui/b.ico")

        image_tk = load_image("src/gui/b.png", max_width=400, max_height=300)
        if image_tk:
            image_label = tk.Label(root, image=image_tk)
            image_label.image = image_tk  # Manter referência
            image_label.pack(pady=10)

        # Botões principais para escolher a funcionalidade
        tk.Button(root, text="Transcrever", command=self.abrir_transcricao).pack(pady=10)
        tk.Button(root, text="Resumir", command=self.abrir_resumo,
                  state=tk.NORMAL if api_available else tk.DISABLED).pack(pady=10)
        tk.Button(root, text="OCR", command=self.abrir_ocr, state=tk.NORMAL if api_available else tk.DISABLED).pack(
            pady=10)
        tk.Button(root, text="Editar", command=self.abrir_edicao, state=tk.NORMAL).pack(
            pady=10)
        tk.Button(root, text="Leia-me", command=self.abrir_leiame_html, state=tk.NORMAL if api_available else tk.DISABLED).pack(
            pady=10)

        credit_label = tk.Label(root, text=f"Desenvolvido por Pedro Duarte Blanco", fg="blue", cursor="hand2",
                                font=("Arial", 14))
        credit_label.pack(pady=2)
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
        leiame_path = "src/leiame.html"
        webbrowser.open(f'{leiame_path}')








if __name__ == "__main__":
    root = tk.Tk()
    app = MainGUI(root)
    root.mainloop()