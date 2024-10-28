import tkinter as tk
from tkinter import messagebox
from typing import Optional, Tuple, Callable
from dotenv import load_dotenv
import os
from PIL import Image, ImageTk
import webbrowser


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


def show_api_key_prompt(app: tk.Tk) -> None:
    """Abre um prompt para o usuário inserir a OpenAI API Key com a opção de ajuda.

    Args:
        app (tk.Tk): Instância raiz do Tkinter.
    """
    key_prompt_window = tk.Toplevel(app)
    key_prompt_window.title("Inserir OpenAI API Key")
    key_prompt_window.geometry("400x250")

    label = tk.Label(key_prompt_window, text="Por favor, insira sua OpenAI API Key:")
    label.pack(padx=20, pady=5)

    api_key_entry = tk.Entry(key_prompt_window, width=50, show='*')
    api_key_entry.pack(padx=20, pady=5)

    save_key_var = tk.BooleanVar()
    save_key_checkbox = tk.Checkbutton(key_prompt_window, text="Salvar minha API Key", variable=save_key_var)
    save_key_checkbox.pack(pady=5)

    def save_api_key() -> None:
        api_key = api_key_entry.get()
        if api_key:
            if save_key_var.get():
                try:
                    with open(".env", "w") as f:
                        f.write(f"OPENAI_API_KEY={api_key}\n")
                    load_dotenv()
                    messagebox.showinfo("Sucesso", "API Key salva com sucesso no arquivo .env!")
                except Exception as e:
                    messagebox.showerror("Erro", f"Erro ao salvar a API Key: {str(e)}")
            else:
                os.environ['OPENAI_API_KEY'] = api_key
                messagebox.showinfo("Aviso", "API Key definida apenas para esta sessão.")
            key_prompt_window.destroy()
        else:
            messagebox.showerror("Erro", "Por favor, insira uma API Key válida.")

    tk.Button(key_prompt_window, text="Salvar Key", command=save_api_key).pack(pady=5)
    tk.Button(key_prompt_window, text="Cancelar", command=key_prompt_window.destroy).pack(pady=5)

    def open_openai_key_link() -> None:
        webbrowser.open("https://platform.openai.com/account/api-keys")

    tk.Button(key_prompt_window, text="Obter API Key", command=open_openai_key_link).pack(pady=5)




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