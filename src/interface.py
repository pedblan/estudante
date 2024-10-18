#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright (c) 2024 Pedro Duarte Blanco
#
# Este software é distribuído sob a Licença MIT.
# Consulte o arquivo LICENSE para obter mais informações.

"""Este script contém a interface gráfica do aplicativo."""

import os
import sys
import threading
import tkinter as tk
from tkinter import filedialog, messagebox
from dotenv import load_dotenv
import webbrowser
from PIL import Image, ImageTk
from src.tarefas_principais import youtube, audio, pdf_docx, abrir_leiame_html  # Importando funções do tarefas_principais.py

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()
# Variável fixa para o nome do aplicativo
APP_NAME = "estudante v. 1.0"  # Modifique esta variável conforme necessário
# Declara botão de envio
send_button = None

def rodar():
    def reset_app():
        # Redefinir variáveis de controle para seus valores iniciais
        media_type_var.set("audio")
        metodo_var.set("api")
        idioma_var.set("pt")
        whisper_model_var.set("base")
        modo_var.set("geral")
        timestamp_var.set(False)

        # Limpar campos de entrada
        youtube_url_entry.delete(0, tk.END)
        instrucao_personalizada_text.delete("1.0", tk.END)

        # Resetar caminho do arquivo PDF/DOCX
        global pdf_file_path
        pdf_file_path = None

        # Esconder botões e frames que podem estar visíveis
        send_button.pack_forget()
        log_frame.pack_forget()
        instrucao_personalizada_frame.pack_forget()
        whisper_model_frame.pack_forget()
        audio_frame.pack_forget()
        youtube_frame.pack_forget()
        pdf_frame.pack_forget()
        modo_frame.pack_forget()
        idioma_frame.pack_forget()
        metodo_frame.pack_forget()
        timestamp_frame.pack_forget()

        # Mostrar os frames iniciais
        toggle_input()
        toggle_whisper_options()
        toggle_personalizado()

    # Função para abrir o link da OpenAI para obter a API key
    def open_openai_link():
        webbrowser.open("https://platform.openai.com/signup")

    # Função para mostrar o prompt para inserir a OpenAI API Key com botão de ajuda
    def show_api_key_prompt():
        """Abre um prompt para o usuário inserir a OpenAI API Key com a opção de ajuda."""
        key_prompt_window = tk.Toplevel(app)
        key_prompt_window.title("Inserir OpenAI API Key")

        # Instruções iniciais
        label = tk.Label(key_prompt_window, text="Por favor, insira sua OpenAI API Key:")
        label.pack(padx=20, pady=5)

        # Campo para entrada da API Key
        api_key_entry = tk.Entry(key_prompt_window, width=50)
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
                    with open(".env", "w") as f:
                        f.write(f"OPENAI_API_KEY={api_key}\n")
                    # Recarrega as variáveis de ambiente
                    load_dotenv()
                    messagebox.showinfo("Sucesso", "API Key salva com sucesso no arquivo .env!")
                else:
                    # Define a variável de ambiente para esta sessão
                    os.environ['OPENAI_API_KEY'] = api_key
                    messagebox.showinfo("Aviso", "API Key definida apenas para esta sessão.")
                key_prompt_window.destroy()
            else:
                messagebox.showerror("Erro", "Por favor, insira uma API Key válida.")

        # Botão para salvar a API Key
        tk.Button(key_prompt_window, text="Salvar Key", command=save_api_key).pack(pady=5)


        # Botão de ajuda
        def show_api_key_info():
            """Abre uma janela com uma explicação sobre a OpenAI API Key."""
            key_info_window = tk.Toplevel(key_prompt_window)
            key_info_window.title("Informações sobre a API Key")

            label = tk.Label(key_info_window, text="A OpenAI API Key é necessária para utilizar os recursos da API da "
                                                   "da OpenAI, incluindo resumo e transcrição eficiente.\n\n"
                                                   "1. Você pode obter uma API Key criando uma conta no site da OpenAI.\n"
                                                   "2. Após criar sua conta, acesse o painel de controle para gerar uma chave.\n"
                                                   "3. Cole sua chave no campo apropriado ao utilizar o app.\n\n"
                                                   "Nota: Se você não salvar a chave, será necessário inseri-la a cada uso.")
            label.pack(padx=20, pady=20)

            close_button = tk.Button(key_info_window, text="Fechar", command=key_info_window.destroy)
            close_button.pack(pady=10)

        # Botão para exibir a explicação da API Key
        tk.Button(key_prompt_window, text="O que é a OpenAI API Key?", command=show_api_key_info).pack(pady=5)

        # Botão para fechar o prompt sem salvar
        close_button = tk.Button(key_prompt_window, text="Fechar", command=key_prompt_window.destroy)
        close_button.pack(pady=5)

    # Função para rodar as tarefas longas em uma thread separada
    def run_in_thread(func, *args):
        thread = threading.Thread(target=func, args=args)
        thread.start()

    # Funções para processar o áudio, YouTube e PDF/DOCX

    def process_audio():
        # ... código existente ...
        file_path = filedialog.askopenfilename(filetypes=[
            ("Arquivos de áudio",
             "*.mp3 *.wav *.aac *.ogg *.flac *.m4a *.wma *.aiff *.ac3 *.opus *.alac *.amr *.caf *.dsd *.dts *.pcm *.mp4 *.mkv *.mov *.avi")
        ])
        if file_path:
            idioma = idioma_var.get()
            api = metodo_var.get() == "api"
            com_timestamp = timestamp_var.get()

            # Função que será executada em uma thread separada
            def task():
                audio(file_path, idioma, api, 80, com_timestamp)
                # Após a conclusão, redefinir o aplicativo
                app.after(0, reset_app)

            run_in_thread(task)

    # Função para processar o YouTube
    def process_youtube():
        youtube_url = youtube_url_entry.get()
        if youtube_url:
            idioma = idioma_var.get()
            api = metodo_var.get() == "api"
            com_timestamp = timestamp_var.get()

            # Função que será executada em uma thread separada
            def task():
                youtube(youtube_url, idioma, api, 80, com_timestamp)
                # Após a conclusão, redefinir o aplicativo
                app.after(0, reset_app)

            run_in_thread(task)

    # Variável para armazenar o caminho do arquivo selecionado
    pdf_file_path = None

    # Função para selecionar o arquivo PDF/DOCX
    def select_pdf_file():
        nonlocal pdf_file_path
        file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf"), ("Word Files", "*.docx")])
        if file_path:
            pdf_file_path = file_path
            update_send_button_visibility()
        else:
            pdf_file_path = None
            update_send_button_visibility()

    # Função para processar PDF/DOCX (quando o usuário clica em "Enviar")
    def process_pdf():
        if pdf_file_path:
            modo_resumo = modo_var.get()
            instrucao_personalizada = instrucao_personalizada_text.get("1.0",
                                                                       tk.END).strip() if modo_resumo == "personalizado" else None

            # Função que será executada em uma thread separada
            def task():
                pdf_docx(pdf_file_path, modo_resumo, instrucao_personalizada)
                # Após a conclusão, redefinir o aplicativo
                app.after(0, reset_app)

            run_in_thread(task)

    # Classe para redirecionar o stdout e capturar prints
    class PrintLogger:
        def __init__(self, text_widget):
            self.text_widget = text_widget
            self.text_widget.config(state=tk.NORMAL)

        def write(self, message):
            self.text_widget.insert(tk.END, message)
            self.text_widget.see(tk.END)
            self.text_widget.update()

        def flush(self):
            pass

    # Verificar se a API_KEY está configurada
    api_key = os.getenv('OPENAI_API_KEY')
    api_available = api_key is not None

    # Função para alternar a exibição de campos de entrada
    def toggle_input():
        #global send_button  # Adiciona a declaração global

        media_type = media_type_var.get()
        if media_type == 'audio' or media_type == 'youtube':
            audio_frame.pack(pady=5) if media_type == 'audio' else audio_frame.pack_forget()
            youtube_frame.pack(pady=5) if media_type == 'youtube' else youtube_frame.pack_forget()
            pdf_frame.pack_forget()
            idioma_frame.pack(pady=5)
            metodo_frame.pack(pady=5)
            timestamp_frame.pack(pady=5)
            modo_frame.pack_forget()
        elif media_type == 'pdf':
            audio_frame.pack_forget()
            youtube_frame.pack_forget()
            pdf_frame.pack(pady=5)
            idioma_frame.pack_forget()
            metodo_frame.pack_forget()
            timestamp_frame.pack_forget()
            modo_frame.pack(pady=5)
        update_send_button_visibility()

    def update_send_button_visibility():
        # Mostrar o botão Enviar apenas se um arquivo ou URL estiver selecionado
        if media_type_var.get() == "audio" and audio_frame.winfo_ismapped():
            send_button.pack_forget()  # Não mostrar o botão Enviar aqui
        elif media_type_var.get() == "youtube" and youtube_url_entry.get():
            send_button.pack(pady=10)
        elif media_type_var.get() == "pdf" and pdf_file_path:
            send_button.pack(pady=10)
        else:
            send_button.pack_forget()

    # Função para enviar a tarefa correta
    def send_task():
        media_type = media_type_var.get()
        if media_type == "audio":
            run_in_thread(process_audio)
        elif media_type == "youtube":
            run_in_thread(process_youtube)
        elif media_type == "pdf":
            process_pdf()

    def toggle_whisper_options():
        metodo = metodo_var.get()
        if metodo == 'local':
            whisper_model_frame.pack(pady=5)
        else:
            whisper_model_frame.pack_forget()

    def toggle_personalizado():
        modo = modo_var.get()
        if modo == 'personalizado':
            instrucao_personalizada_frame.pack(pady=5)
        else:
            instrucao_personalizada_frame.pack_forget()

    def show_log():
        if log_frame.winfo_viewable():
            log_frame.pack_forget()
        else:
            log_frame.pack(pady=5)

    def open_website(url):
        webbrowser.open(url)

    # Função para carregar e exibir a imagem
    def load_image():
        try:
            # Abrir a imagem
            image_path = recurso_caminho("src/b.png")
            image = Image.open(image_path)

            # Definir as dimensões máximas
            max_width = 400
            max_height = 300

            # Obter as dimensões originais
            original_width, original_height = image.size

            # Calcular a proporção de redimensionamento
            ratio = min(max_width / original_width, max_height / original_height)

            # Se a imagem for maior que o tamanho máximo, redimensionar
            if ratio < 1:
                new_width = int(original_width * ratio)
                new_height = int(original_height * ratio)
                image_resized = image.resize((new_width, new_height), Image.LANCZOS)
            else:
                # Manter o tamanho original
                image_resized = image

            # Converter para PhotoImage
            image_tk = ImageTk.PhotoImage(image_resized)

            # Atualizar o label da imagem
            image_label.config(image=image_tk)
            image_label.image = image_tk  # Manter referência

        except Exception as e:
            print(f"Erro ao carregar imagem: {str(e)}")

    # Configurando a janela principal
    app = tk.Tk()
    app.title(APP_NAME)
    icon_path = recurso_caminho("b.ico")
    app.iconbitmap(icon_path)

    # Variáveis de controle
    media_type_var = tk.StringVar(value="audio")
    metodo_var = tk.StringVar(value="api")
    idioma_var = tk.StringVar(value="pt")
    whisper_model_var = tk.StringVar(value="base")
    modo_var = tk.StringVar(value="geral")
    timestamp_var = tk.BooleanVar(value=False)

    # Variável para armazenar o caminho do arquivo PDF/DOCX selecionado
    pdf_file_path = None

    # Frame para imagem no topo
    image_label = tk.Label(app)
    image_label.pack(pady=10)
    load_image()

    # Adicionando o botão para obter a OpenAI Key caso não esteja configurada
    if not api_available:
        tk.Button(app, text="Obter OpenAI API Key", command=open_openai_link).pack(pady=5)
        tk.Button(app, text="Inserir OpenAI API Key", command=show_api_key_prompt).pack(pady=5)

    # Botões de rádio para selecionar o tipo de tarefa
    tk.Label(app, text="Escolha a tarefa:").pack(pady=5)
    tk.Radiobutton(app, text="Transcrever arquivo de áudio", variable=media_type_var, value="audio",
                   command=toggle_input).pack()
    tk.Radiobutton(app, text="Transcrever vídeo do YouTube", variable=media_type_var, value="youtube",
                   command=toggle_input).pack()
    tk.Radiobutton(app, text="Resumir PDF ou DOCX", variable=media_type_var, value="pdf", command=toggle_input,
                   state=tk.NORMAL if api_available else tk.DISABLED).pack()

    # Frame para upload de áudio
    audio_frame = tk.Frame(app)
    tk.Label(audio_frame, text="Escolha o arquivo de áudio:").pack()
    tk.Button(audio_frame, text="Selecionar arquivo de áudio", command=process_audio).pack()

    # Frame para URL do YouTube
    youtube_frame = tk.Frame(app)
    tk.Label(youtube_frame, text="Insira o link do YouTube:").pack()
    youtube_url_entry = tk.Entry(youtube_frame)
    youtube_url_entry.pack(fill=tk.X, expand=True)
    tk.Button(youtube_frame, text="Transcrever YouTube", command=process_youtube).pack()

    # Frame para upload de PDF/DOCX
    pdf_frame = tk.Frame(app)
    tk.Label(pdf_frame, text="Escolha o arquivo PDF ou DOCX:").pack()
    tk.Button(pdf_frame, text="Selecionar arquivo PDF/DOCX", command=select_pdf_file).pack()

    # Frame do botão Enviar (inicialmente oculto)
    send_button = tk.Button(app, text="Enviar", command=send_task)
    send_button.pack_forget()

    # Frame para escolha do idioma
    idioma_frame = tk.Frame(app)
    tk.Label(idioma_frame, text="Escolha o idioma:").pack()
    idioma_options = ["pt", "en", "es", "fr", "it"]
    idioma_menu = tk.OptionMenu(idioma_frame, idioma_var, *idioma_options)
    idioma_menu.pack()

    # Frame para escolha entre API da OpenAI ou Whisper Local
    metodo_frame = tk.Frame(app)
    tk.Label(metodo_frame, text="Escolha o método de transcrição:").pack()
    tk.Radiobutton(metodo_frame, text="Usar API da OpenAI", variable=metodo_var, value="api",
                   command=toggle_whisper_options, state=tk.NORMAL if api_available else tk.DISABLED).pack()
    tk.Radiobutton(metodo_frame, text="Usar Whisper Local", variable=metodo_var, value="local",
                   command=toggle_whisper_options).pack()

    # Checkbox para timestamp (ao lado da coluna principal)
    timestamp_frame = tk.Frame(app)
    timestamp_checkbox = tk.Checkbutton(timestamp_frame, text="Com timestamp", variable=timestamp_var)
    timestamp_checkbox.pack(side=tk.LEFT)

    # Frame para escolha do modelo Whisper (aparece apenas quando Whisper Local é selecionado)
    whisper_model_frame = tk.Frame(app)
    tk.Label(whisper_model_frame, text="Escolha o modelo Whisper local:").pack()
    whisper_model_menu = tk.OptionMenu(whisper_model_frame, whisper_model_var, "tiny", "base", "small", "medium", "large")
    whisper_model_menu.pack()

    # Frame para escolher o modo de resumo (para PDF/DOCX)
    modo_frame = tk.Frame(app)
    tk.Label(modo_frame, text="Escolha o modo de resumo:").pack()
    tk.Radiobutton(modo_frame, text="Modo Geral", variable=modo_var, value="geral", command=toggle_personalizado).pack()
    tk.Radiobutton(modo_frame, text="Modo Jurisprudência", variable=modo_var, value="jurisprudencia",
                   command=toggle_personalizado).pack()
    tk.Radiobutton(modo_frame, text="Modo Personalizado", variable=modo_var, value="personalizado",
                   command=toggle_personalizado).pack()

    # Frame para instrução personalizada (aparece apenas quando o modo "personalizado" é selecionado)
    instrucao_personalizada_frame = tk.Frame(app)
    tk.Label(instrucao_personalizada_frame, text="Escreva sua instrução personalizada:").pack()
    instrucao_personalizada_text = tk.Text(instrucao_personalizada_frame, height=4, width=50)
    instrucao_personalizada_text.pack()

    # Frame do log (escondido inicialmente)
    log_frame = tk.Frame(app)
    log_text = tk.Text(log_frame, height=15, width=80)
    log_text.pack(side=tk.LEFT, padx=5)
    log_scrollbar = tk.Scrollbar(log_frame, command=log_text.yview)
    log_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    log_text.config(yscrollcommand=log_scrollbar.set)

    # Redireciona os prints para a área de log
    sys.stdout = PrintLogger(log_text)

    # Botão para exibir o log
    tk.Button(app, text="Ver log", command=show_log).pack(pady=10)

    # Adicionando o link de créditos no rodapé
    footer_frame = tk.Frame(app)
    footer_frame.pack(side=tk.BOTTOM, pady=5)

    credit_label = tk.Label(footer_frame, text=f"Desenvolvido por Pedro Duarte Blanco", fg="blue", cursor="hand2",
                            font=("Arial", 14))
    credit_label.pack()
    credit_label.bind("<Button-1>", lambda e: open_website("http://pedblan.wordpress.com"))

    # Botão para abrir o arquivo LEIAME
    leiame_button_frame = tk.Frame(app)
    leiame_button_frame.pack(side=tk.BOTTOM, pady=5)

    tk.Button(leiame_button_frame, text="LEIAME", command=abrir_leiame_html).pack()

    # Inicialmente, mostrar apenas a seleção de áudio
    toggle_input()
    toggle_whisper_options()
    toggle_personalizado()

    # Executa a aplicação
    app.mainloop()

def recurso_caminho(caminho_relativo):
    """Obter o caminho para recurso, mesmo em ambiente empacotado."""
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, caminho_relativo)

def abrir_leiame_html():
    leiame_path = recurso_caminho("src/leiame.html")
    webbrowser.open(f'file://{leiame_path}')