from PIL import Image, ImageTk
import tkinter as tk
from tkinter import filedialog, messagebox
from dotenv import load_dotenv
import os
import webbrowser

def load_image(image_path, max_width=None, max_height=None):
    try:
        # Abrir a imagem
        image = Image.open(image_path)

        # Definir as dimensões máximas, se especificadas
        if max_width and max_height:
            original_width, original_height = image.size
            ratio = min(max_width / original_width, max_height / original_height)

            # Se a imagem for maior que o tamanho máximo, redimensionar
            if ratio < 1:
                new_width = int(original_width * ratio)
                new_height = int(original_height * ratio)
                image = image.resize((new_width, new_height), Image.LANCZOS)

        # Converter para PhotoImage
        image_tk = ImageTk.PhotoImage(image)

        # Retornar a imagem configurada para ser usada no Label (o Label deve ser criado no script que usa tkinter)
        return image_tk

    except Exception as e:
        print(f"Erro ao carregar imagem: {str(e)}")
        return None


def configurar_log(root):
    """Configura um frame de log na janela root."""
    log_frame = tk.Frame(root)
    log_text = tk.Text(log_frame, height=15, width=80)
    log_text.pack(side=tk.LEFT, padx=5)
    log_scrollbar = tk.Scrollbar(log_frame, command=log_text.yview)
    log_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    log_text.config(yscrollcommand=log_scrollbar.set)

    # Função para adicionar mensagens ao log
    def append_log(message):
        log_text.insert(tk.END, f"{message}\n")
        log_text.see(tk.END)

    return log_frame, log_text, append_log

# Função para mostrar o prompt para inserir a OpenAI API Key com botão de ajuda
def show_api_key_prompt(app):
    """Abre um prompt para o usuário inserir a OpenAI API Key com a opção de ajuda."""
    key_prompt_window = tk.Toplevel(app)
    key_prompt_window.title("Inserir OpenAI API Key")
    key_prompt_window.geometry("400x250")  # Definindo um tamanho fixo

    # Instruções iniciais
    label = tk.Label(key_prompt_window, text="Por favor, insira sua OpenAI API Key:")
    label.pack(padx=20, pady=5)

    # Campo para entrada da API Key (com texto mascarado)
    api_key_entry = tk.Entry(key_prompt_window, width=50, show='*')
    api_key_entry.pack(padx=20, pady=5)

    # Checkbox para salvar a key
    save_key_var = tk.BooleanVar()
    save_key_checkbox = tk.Checkbutton(key_prompt_window, text="Salvar minha API Key", variable=save_key_var)
    save_key_checkbox.pack(pady=5)

    # Função para salvar a API Key
    def save_api_key():
        api_key = api_key_entry.get()
        if api_key:
            if save_key_var.get():
                # Salva a API Key no arquivo .env
                try:
                    with open(".env", "w") as f:
                        f.write(f"OPENAI_API_KEY={api_key}\n")
                    # Recarrega as variáveis de ambiente
                    load_dotenv()
                    messagebox.showinfo("Sucesso", "API Key salva com sucesso no arquivo .env!")
                except Exception as e:
                    messagebox.showerror("Erro", f"Erro ao salvar a API Key: {str(e)}")
            else:
                # Define a variável de ambiente para esta sessão
                os.environ['OPENAI_API_KEY'] = api_key
                messagebox.showinfo("Aviso", "API Key definida apenas para esta sessão.")
            key_prompt_window.destroy()
        else:
            messagebox.showerror("Erro", "Por favor, insira uma API Key válida.")

    # Botão para salvar a API Key
    tk.Button(key_prompt_window, text="Salvar Key", command=save_api_key).pack(pady=5)

    # Botão para cancelar
    tk.Button(key_prompt_window, text="Cancelar", command=key_prompt_window.destroy).pack(pady=5)

    # Função para abrir o link de criação de API Key
    def open_openai_key_link():
        webbrowser.open("https://platform.openai.com/account/api-keys")

    # Botão para abrir a página da OpenAI para criação de API Key
    tk.Button(key_prompt_window, text="Obter API Key", command=open_openai_key_link).pack(pady=5)


def mostrar_log(root):
    # Cria uma variável BooleanVar para o checkbox "Mostrar Log"
    mostrar_log_var = tk.BooleanVar(value=False)

    # Checkbox para controlar a exibição do log
    checkbox_mostrar_log = tk.Checkbutton(root, text="Mostrar Log", variable=mostrar_log_var)
    checkbox_mostrar_log.pack(pady=5)

    return mostrar_log_var

def abrir_janela_log(root):
    log_window = tk.Toplevel(root)
    log_window.title("Log")
    log_frame, log_text, append_log = configurar_log(log_window)
    log_frame.pack(pady=5)
    return log_frame, log_text, append_log

def enviar(mostrar_log_var, root, enviar_func):
    # Verifica se o checkbox "Mostrar Log" está marcado
    if mostrar_log_var.get():
        abrir_janela_log(root)



