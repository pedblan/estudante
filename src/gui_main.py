import tkinter as tk
import os
from src.gui_transcricao import TranscricaoGUI
from src.gui_resumo import ResumoGUI
from src.gui_ocr import OCRGUI
from dotenv import load_dotenv
from src.subtarefas import load_image

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Verificar se a API_KEY está configurada
api_key = os.getenv('OPENAI_API_KEY')
api_available = api_key is not None


class MainGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Estudante v1.1")

        image_tk = load_image("src/b.png", max_width=400, max_height=300)
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



    def abrir_transcricao(self):
        nova_janela = tk.Toplevel(self.root)
        TranscricaoGUI(nova_janela)

    def abrir_resumo(self):
        nova_janela = tk.Toplevel(self.root)
        ResumoGUI(nova_janela)

    def abrir_ocr(self):
        nova_janela = tk.Toplevel(self.root)
        OCRGUI(nova_janela)


if __name__ == "__main__":
    root = tk.Tk()
    app = MainGUI(root)
    root.mainloop()