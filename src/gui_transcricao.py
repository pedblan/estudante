import tkinter as tk
from tkinter import filedialog
import threading
from tarefas_principais import audio, youtube


class TranscricaoGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Transcrição de Áudio/Vídeo")

        # Componentes da GUI para transcrição
        tk.Button(root, text="Escolher Arquivo de Áudio", command=self.processar_audio).pack(pady=10)
        self.youtube_url_entry = tk.Entry(root, width=50)
        self.youtube_url_entry.pack(pady=5)
        tk.Button(root, text="Transcrever Vídeo do YouTube", command=self.processar_youtube).pack(pady=10)

        # Checkbox para timestamp
        self.timestamp_var = tk.BooleanVar(value=False)
        tk.Checkbutton(root, text="Com timestamp", variable=self.timestamp_var).pack(pady=5)

        # Botão Enviar
        tk.Button(root, text="Enviar", command=self.enviar).pack(pady=10)

    def processar_audio(self):
        self.file_path = filedialog.askopenfilename(filetypes=[("Arquivos de áudio", "*.mp3 *.wav *.aac *.ogg")])

    def processar_youtube(self):
        self.youtube_url = self.youtube_url_entry.get()

    def enviar(self):
        # Lógica para processar o áudio ou o vídeo
        if hasattr(self, 'file_path'):
            self.run_in_thread(audio, self.file_path, self.timestamp_var.get())
        elif hasattr(self, 'youtube_url') and self.youtube_url:
            self.run_in_thread(youtube, self.youtube_url, self.timestamp_var.get())

    def run_in_thread(self, func, *args):
        thread = threading.Thread(target=func, args=args)
        thread.start()