import tkinter as tk
from tkinter import filedialog
import threading
from dotenv import load_dotenv
from src.tarefas_principais import audio, youtube
import os

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Verificar se a API_KEY está configurada
api_key = os.getenv('OPENAI_API_KEY')
api_available = api_key is not None


class TranscricaoGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Transcrever")

        # Variáveis de controle
        self.media_type_var = tk.StringVar(value="audio")
        self.idioma_var = tk.StringVar(value="pt")
        self.metodo_var = tk.StringVar(value="api")
        self.timestamp_var = tk.BooleanVar(value=False)

        # Botões de rádio para selecionar o tipo de mídia
        tk.Label(root, text="Escolha o tipo de mídia:").pack(pady=5)
        tk.Radiobutton(root, text="Arquivo de Áudio", variable=self.media_type_var, value="audio",
                       command=self.toggle_input).pack()
        tk.Radiobutton(root, text="Vídeo do YouTube", variable=self.media_type_var, value="youtube",
                       command=self.toggle_input).pack()

        # Frame para upload de áudio
        self.audio_frame = tk.Frame(root)
        tk.Label(self.audio_frame, text="Escolha o arquivo de áudio:").pack()
        tk.Button(self.audio_frame, text="Selecionar arquivo de áudio", command=self.processar_audio).pack()

        # Frame para URL do YouTube (inicialmente escondido)
        self.youtube_frame = tk.Frame(root)
        tk.Label(self.youtube_frame, text="Insira o link do YouTube:").pack()
        self.youtube_url_entry = tk.Entry(self.youtube_frame, width=50)
        self.youtube_url_entry.pack()
        self.youtube_frame.pack_forget()

        # Frame para escolha do idioma
        self.idioma_frame = tk.Frame(root)
        tk.Label(self.idioma_frame, text="Escolha o idioma:").pack()
        idioma_options = ["pt", "en", "es", "fr", "it"]
        self.idioma_menu = tk.OptionMenu(self.idioma_frame, self.idioma_var, *idioma_options)
        self.idioma_menu.pack()
        self.idioma_frame.pack(pady=5)

        # Frame para escolha do método de transcrição
        self.whisper_model_var = tk.StringVar(value="base")

        # Frame para escolha do modelo Whisper (aparece apenas quando Whisper Local é selecionado)
        self.whisper_model_frame = tk.Frame(root)
        tk.Label(self.whisper_model_frame, text="Escolha o modelo Whisper local:").pack()
        whisper_model_options = ["tiny", "base", "small", "medium", "large"]
        self.whisper_model_menu = tk.OptionMenu(self.whisper_model_frame, self.whisper_model_var,
                                                *whisper_model_options)
        self.whisper_model_menu.pack()

        self.metodo_var.trace_add('write', self.toggle_whisper_model_frame)
        self.metodo_frame = tk.Frame(root)
        tk.Label(self.metodo_frame, text="Escolha o método de transcrição:").pack()
        tk.Radiobutton(self.metodo_frame, text="Usar API da OpenAI", variable=self.metodo_var, value="api",
                       state=tk.NORMAL if api_available else tk.DISABLED).pack()
        tk.Radiobutton(self.metodo_frame, text="Usar Whisper Local", variable=self.metodo_var, value="local").pack()

        # Checkbox para timestamp
        self.timestamp_frame = tk.Frame(root)
        self.timestamp_checkbox = tk.Checkbutton(self.timestamp_frame, text="Com timestamp",
                                                 variable=self.timestamp_var)
        self.timestamp_checkbox.pack()

        # Botão Enviar
        self.send_button = tk.Button(root, text="Enviar", command=self.enviar)
        self.send_button.pack(pady=10)

        # Inicialmente, mostrar apenas a seleção de áudio
        self.toggle_input()
        self.metodo_frame.pack(pady=5)
        self.whisper_model_frame.pack_forget()
        self.timestamp_frame.pack(pady=5)

    def toggle_input(self):
        media_type = self.media_type_var.get()
        if media_type == 'audio':
            self.audio_frame.pack(pady=5)
            self.youtube_frame.pack_forget()
        elif media_type == 'youtube':
            self.youtube_frame.pack(pady=5)
            self.audio_frame.pack_forget()


    def toggle_whisper_model_frame(self, *args):
        if self.metodo_var.get() == 'local':
            self.whisper_model_frame.pack(pady=5)
        else:
            self.whisper_model_frame.pack_forget()

    def processar_audio(self):
        self.file_path = filedialog.askopenfilename(filetypes=[("Arquivos de áudio", "*.mp3 *.wav *.aac *.ogg")])

    def enviar(self):
        media_type = self.media_type_var.get()
        if media_type == "audio" and hasattr(self, 'file_path'):
            self.run_in_thread(audio, self.file_path, self.idioma_var.get(), self.metodo_var.get() == 'api', self.timestamp_var.get(), self.whisper_model_var.get() if self.metodo_var.get() == 'local' else None)
        elif media_type == "youtube" and self.youtube_url_entry.get():
            youtube_url = self.youtube_url_entry.get()
            self.run_in_thread(youtube, youtube_url, self.idioma_var.get(), self.metodo_var.get() == 'api', self.timestamp_var.get(), self.whisper_model_var.get() if self.metodo_var.get() == 'local' else None)
    def run_in_thread(self, func, *args):
        thread = threading.Thread(target=func, args=args)
        thread.start()


if __name__ == "__main__":
    root = tk.Tk()
    app = TranscricaoGUI(root)
    root.mainloop()
