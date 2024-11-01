import tkinter as tk
from tkinter import filedialog
import threading
from typing import Union

from dotenv import load_dotenv
import os

from src.utils import download_yt, dividir_audio, transcrever_partes, gravar_documento, abrir_doc_produzido, limpar_temp, suprimir_avisos
from src.utils_gui import imagem_na_janela_secundaria, checkbox_mostrar_log_simplificado
# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Verificar se a API_KEY está configurada
api_key = os.getenv('OPENAI_API_KEY')
api_disponivel = api_key is not None

caminho_arquivo_imagem = "src/transcricao/transcrever.png"

class TranscricaoGUI:
    def __init__(self, root: tk.Tk) -> None:
        """Inicializa a GUI de transcrição.

        Args:
            root (tk.Tk): A instância raiz do Tkinter.
        """
        self.root = root
        self.root.title("Transcrever")

        imagem_na_janela_secundaria(self.root, caminho_arquivo_imagem)

        # Variáveis de controle
        self.tipo_midia_var = tk.StringVar(value="audio")
        self.idioma_var = tk.StringVar(value="pt")
        self.metodo_var = tk.StringVar(value="api")
        self.timestamp_var = tk.BooleanVar(value=False)
        self.mostrar_log_var = tk.BooleanVar(value=False)  # Variável de controle para o checkbox

        # Botões de rádio para selecionar o tipo de mídia
        tk.Label(root, text="Escolha o tipo de mídia:").pack(pady=5)
        tk.Radiobutton(root, text="Arquivo de Áudio", variable=self.tipo_midia_var, value="audio",
                       command=self.toggle_input).pack()
        tk.Radiobutton(root, text="Vídeo do YouTube", variable=self.tipo_midia_var, value="youtube",
                       command=self.toggle_input).pack()

        # Frame para upload de áudio
        self.frame_audio = tk.Frame(root)
        tk.Label(self.frame_audio, text="Escolha o arquivo de áudio:").pack()
        tk.Button(self.frame_audio, text="Selecionar arquivo de áudio", command=self.processar_audio).pack()

        # Frame para URL do YouTube (inicialmente escondido)
        self.frame_youtube = tk.Frame(root)
        tk.Label(self.frame_youtube, text="Insira o link do YouTube:").pack()
        self.youtube_url_entry = tk.Entry(self.frame_youtube, width=50)
        self.youtube_url_entry.pack()
        self.frame_youtube.pack_forget()

        # Frame para escolha do idioma
        self.frame_idioma = tk.Frame(root)
        tk.Label(self.frame_idioma, text="Escolha o idioma:").pack()
        opcoes_idioma = ["pt", "en", "es", "fr", "it"]
        self.menu_idioma = tk.OptionMenu(self.frame_idioma, self.idioma_var, *opcoes_idioma)
        self.menu_idioma.pack()
        self.frame_idioma.pack(pady=5)

        # Frame para escolha do método de transcrição
        self.whisper_model_var = tk.StringVar(value="base")

        # Frame para escolha do modelo Whisper (aparece apenas quando Whisper Local é selecionado)
        self.frame_whisper_model = tk.Frame(root)
        tk.Label(self.frame_whisper_model, text="Escolha o modelo Whisper local:").pack()
        opcoes_whisper_model = ["tiny", "base", "small", "medium", "large"]
        self.menu_whisper_model = tk.OptionMenu(self.frame_whisper_model, self.whisper_model_var,
                                                *opcoes_whisper_model)
        self.menu_whisper_model.pack()

        self.metodo_var.trace_add('write', self.toggle_whisper_model_frame)
        self.frame_metodo = tk.Frame(root)
        tk.Label(self.frame_metodo, text="Escolha o método de transcrição:").pack()
        tk.Radiobutton(self.frame_metodo, text="Usar API da OpenAI", variable=self.metodo_var, value="api",
                       state=tk.NORMAL if api_disponivel else tk.DISABLED).pack()
        tk.Radiobutton(self.frame_metodo, text="Usar Whisper Local", variable=self.metodo_var, value="local").pack()

        # Checkbox para timestamp
        self.frame_timestamp = tk.Frame(root)
        self.checkbox_timestamp = tk.Checkbutton(self.frame_timestamp, text="Com timestamp",
                                                 variable=self.timestamp_var)
        self.checkbox_timestamp.pack()

        # Botão Enviar
        self.botao_enviar = tk.Button(root, text="Enviar", command=self.enviar)
        self.botao_enviar.pack(pady=10)

        # Inicialmente, mostrar apenas a seleção de áudio
        self.toggle_input()
        self.frame_metodo.pack(pady=5)
        self.frame_whisper_model.pack_forget()
        self.frame_timestamp.pack(pady=5)



    def toggle_input(self) -> None:
        """Alterna a exibição dos frames de entrada de acordo com o tipo de mídia selecionado."""
        tipo_midia = self.tipo_midia_var.get()
        if tipo_midia == 'audio':
            self.frame_audio.pack(pady=5)
            self.frame_youtube.pack_forget()
        elif tipo_midia == 'youtube':
            self.frame_youtube.pack(pady=5)
            self.frame_audio.pack_forget()

    def toggle_whisper_model_frame(self, *args) -> None:
        """Alterna a exibição do frame de seleção do modelo Whisper."""
        if self.metodo_var.get() == 'local':
            self.frame_whisper_model.pack(pady=5)
        else:
            self.frame_whisper_model.pack_forget()

    def processar_audio(self) -> None:
        """Abre um diálogo para selecionar um arquivo de áudio."""
        self.caminho_arquivo = filedialog.askopenfilename(filetypes=[("Arquivos de áudio", "*.mp3 *.wav *.aac *.ogg")])

    def enviar(self) -> None:
        """Envia o arquivo de mídia para transcrição."""
        # Invocar a função suprimir_avisos com base no estado do checkbox
        suprimir_avisos(self.mostrar_log_var.get())

        tipo_midia = self.tipo_midia_var.get()
        if tipo_midia == "audio" and hasattr(self, 'caminho_arquivo'):
            self.run_in_thread(audio, self.caminho_arquivo, self.idioma_var.get(), self.metodo_var.get() == 'api', self.timestamp_var.get(), self.whisper_model_var.get() if self.metodo_var.get() == 'local' else None)
        elif tipo_midia == "youtube" and self.youtube_url_entry.get():
            youtube_url = self.youtube_url_entry.get()
            self.run_in_thread(youtube, youtube_url, self.idioma_var.get(), self.metodo_var.get() == 'api', self.timestamp_var.get(), self.whisper_model_var.get() if self.metodo_var.get() == 'local' else None)

    def run_in_thread(self, func: callable, *args) -> None:
        """Executa uma função em uma nova thread.

        Args:
            func (callable): A função a ser executada.
            *args: Argumentos para a função.
        """
        thread = threading.Thread(target=func, args=args)
        thread.start()

if __name__ == "__main__":
    root = tk.Tk()
    app = TranscricaoGUI(root)
    root.mainloop()


def youtube(youtube_url: str, idioma: str, api: bool, max_palavras: int, com_timestamp: bool) -> Union[bool, None]:
    """Processa a transcrição de um vídeo de streaming e salva o resultado em um documento Word.

    Args:
        youtube_url (str): URL do vídeo do YouTube.
        idioma (str): Idioma da transcrição.
        api (bool): Se True, usa a API da OpenAI; caso contrário, usa Whisper Local.
        max_palavras (int): Número máximo de palavras por parágrafo.
        com_timestamp (bool): Se True, adiciona timestamps.

    Returns:
        Union[bool, None]: True se o documento foi aberto com sucesso, None caso contrário.
    """
    try:
        titulo, caminho_audio_temp = download_yt(youtube_url)
        _, partes_temp, duracao_total = dividir_audio(caminho_audio_temp)
        doc = transcrever_partes(partes_temp, idioma, api, duracao_total, max_palavras, com_timestamp)
        caminho_arquivo_salvo = gravar_documento(titulo, doc)
        return abrir_doc_produzido(caminho_arquivo_salvo)
    except Exception as e:
        print(f"Erro ao processar vídeo de streaming: {str(e)}")
        return False
    finally:
        limpar_temp()


def audio(caminho_arquivo: str, idioma: str, api: bool, max_palavras: int, com_timestamp: bool) -> Union[bool, None]:
    """Processa a transcrição de um arquivo de áudio e salva o resultado em um documento Word.

    Args:
        caminho_arquivo (str): Caminho do arquivo de áudio.
        idioma (str): Idioma da transcrição.
        api (bool): Se True, usa a API da OpenAI; caso contrário, usa Whisper Local.
        max_palavras (int): Número máximo de palavras por parágrafo.
        com_timestamp (bool): Se True, adiciona timestamps.

    Returns:
        Union[bool, None]: True se o documento foi aberto com sucesso, None caso contrário.
    """
    try:
        titulo, partes_temp, duracao_total = dividir_audio(caminho_arquivo)
        doc = transcrever_partes(partes_temp, idioma, api, duracao_total, max_palavras, com_timestamp)
        caminho_arquivo_salvo = gravar_documento(titulo, doc)
        return abrir_doc_produzido(caminho_arquivo_salvo)
    except Exception as e:
        print(f"Erro ao processar áudio: {str(e)}")
        return False
    finally:
        limpar_temp()


