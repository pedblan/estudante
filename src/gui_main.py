import tkinter as tk
from gui_transcricao import TranscricaoGUI
from gui_resumo import ResumoGUI
from gui_ocr import OCRGUI


class MainGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Estudante - Escolha a Função")

        # Botões principais para escolher a funcionalidade
        tk.Button(root, text="Transcrever", command=self.abrir_transcricao).pack(pady=10)
        tk.Button(root, text="Resumir", command=self.abrir_resumo).pack(pady=10)
        tk.Button(root, text="OCR", command=self.abrir_ocr).pack(pady=10)

    def abrir_transcricao(self):
        self.nova_janela(TranscricaoGUI)

    def abrir_resumo(self):
        self.nova_janela(ResumoGUI)

    def abrir_ocr(self):
        self.nova_janela(OCRGUI)

    def nova_janela(self, GUIClass):
        # Fecha a janela atual e abre a nova janela
        self.root.destroy()
        nova_root = tk.Tk()
        GUIClass(nova_root)
        nova_root.mainloop()


if __name__ == "__main__":
    root = tk.Tk()
    app = MainGUI(root)
    root.mainloop()