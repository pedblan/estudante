import tkinter as tk
from typing import Optional, Tuple, Callable
from PIL import Image, ImageTk


def configurar_log(root: tk.Tk, mostrar_log_var: Optional[tk.BooleanVar] = None) -> Tuple[tk.Frame, tk.Text, Callable[[str], None]]:
    """Configura um frame de log na janela root."""
    log_frame = tk.Frame(root)
    log_text = tk.Text(log_frame, height=15, width=80)
    log_text.pack(side=tk.LEFT, padx=5)
    log_scrollbar = tk.Scrollbar(log_frame, command=log_text.yview)
    log_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    log_text.config(yscrollcommand=log_scrollbar.set)

    def append_log(message: str) -> None:
        if mostrar_log_var is None or mostrar_log_var.get():
            log_text.insert(tk.END, f"{message}\n")
            log_text.see(tk.END)

    return log_frame, log_text, append_log

def abrir_janela_log(root: tk.Tk, mostrar_log_var: Optional[tk.BooleanVar] = None) -> None:
    """Abre uma nova janela para exibir o log."""
    log_window = tk.Toplevel(root)
    log_window.title("Log")
    configurar_log(log_window, mostrar_log_var)
    log_window.mainloop()


def imagem_na_janela_secundaria(root, caminho_arquivo_imagem: str) -> None:
    # Imagem no topo da janela
    imagem = Image.open(caminho_arquivo_imagem)
    imagem = imagem.resize((100, 100), Image.LANCZOS)  # Redimensionar a imagem
    icone = ImageTk.PhotoImage(imagem)
    imagem_label = tk.Label(root, image=icone)
    imagem_label.image = icone  # Manter referência
    imagem_label.pack(pady=10)

def checkbox_mostrar_log_simplificado(root, self):
    checkbox_mostrar_log = tk.Checkbutton(root, text="Mostrar log simplificado", variable=self.mostrar_log_var)
    checkbox_mostrar_log.pack(pady=5)
