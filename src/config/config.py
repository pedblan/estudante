import os
import tkinter as tk
import webbrowser
from tkinter import messagebox, BooleanVar

from dotenv import load_dotenv
from src.requisitos import verificar_api_key
api_disponivel: bool = verificar_api_key()


class ConfigurarGUI:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Configurar Programa")
        self.root.geometry("400x300")

        if not api_disponivel:
            self.configurar_api_key_button = tk.Button(root, text="Configurar OpenAI API KEY", command=self.configurar_api_key)
            self.configurar_api_key_button.pack(pady=10)

        self.usar_api_ocr_var = BooleanVar()
        if api_disponivel:
            self.usar_api_ocr_checkbox = tk.Checkbutton(root, text="Usar API para ajustar OCR", variable=self.usar_api_ocr_var)
            self.usar_api_ocr_checkbox.pack(pady=10)

        self.aplicar_button = tk.Button(root, text="Aplicar", command=self.aplicar)
        self.aplicar_button.pack(side=tk.LEFT, padx=10, pady=10)

        self.cancelar_button = tk.Button(root, text="Cancelar", command=self.cancelar)
        self.cancelar_button.pack(side=tk.LEFT, padx=10, pady=10)

        self.ok_button = tk.Button(root, text="OK", command=self.ok)
        self.ok_button.pack(side=tk.LEFT, padx=10, pady=10)

    def configurar_api_key(self):
        key_prompt_window = tk.Toplevel(self.root)
        key_prompt_window.title("Inserir OpenAI API Key")
        key_prompt_window.geometry("400x250")

        label = tk.Label(key_prompt_window, text="Por favor, insira sua OpenAI API Key:")
        label.pack(padx=20, pady=5)

        api_key_entry = tk.Entry(key_prompt_window, width=50, show='*')
        api_key_entry.pack(padx=20, pady=5)

        save_key_var = BooleanVar()
        save_key_checkbox = tk.Checkbutton(key_prompt_window, text="Salvar minha API Key", variable=save_key_var)
        save_key_checkbox.pack(pady=5)

        def save_api_key():
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

    def aplicar(self):
        if api_disponivel:
            usar_api_ocr = self.usar_api_ocr_var.get()
            with open(".env", "a") as f:
                f.write(f"USAR_API_OCR={usar_api_ocr}\n")
            load_dotenv()
            messagebox.showinfo("Sucesso", "Configurações aplicadas com sucesso!")

    def cancelar(self):
        self.root.destroy()

    def ok(self):
        self.aplicar()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = ConfigurarGUI(root)
    root.mainloop()
