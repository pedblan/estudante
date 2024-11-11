import tkinter as tk
from tkinter import filedialog, messagebox
from src.leiturinha.leiturinha_utils import extrair_texto, centralizar_palavra


class LeiturinhaGUI:
    def __init__(self, root: tk.Tk) -> None:
        """Inicializa a GUI da Leiturinha."""
        self.root = root
        self.root.title("Leiturinha - leitura rápida visual")

        # Configurações da interface principal
        self.setup_interface()

        # Variáveis principais
        self.caminho_arquivo = None
        self.pausado = False
        self.percentual_posicao = 0

    def setup_interface(self):
        """Configura a interface de seleção e controle."""
        tk.Label(self.root, text="Escolha o arquivo de texto:").pack()
        tk.Button(self.root, text="Selecionar arquivo de texto", command=self.processar_texto).pack()

        # Configura controles de velocidade e fonte
        self.velocidade_var = tk.IntVar(value=200)
        self.slider_velocidade = tk.Scale(
            self.root, from_=100, to=600, orient="horizontal", variable=self.velocidade_var,
            label="Velocidade (palavras por minuto)"
        )
        self.slider_velocidade.pack(pady=5)

        self.tamanho_fonte_var = tk.IntVar(value=36)
        self.slider_fonte = tk.Scale(
            self.root, from_=24, to=100, orient="horizontal", variable=self.tamanho_fonte_var,
            label="Tamanho da Fonte"
        )
        self.slider_fonte.pack(pady=5)

        # Opções de tela cheia e negrito
        self.tela_cheia_var = tk.BooleanVar()
        tk.Checkbutton(self.root, text="Tela cheia", variable=self.tela_cheia_var).pack()

        self.negrito_var = tk.BooleanVar()
        tk.Checkbutton(self.root, text="Negritar as três primeiras letras", variable=self.negrito_var).pack()

        # Botão Iniciar
        tk.Button(self.root, text="Iniciar Leiturinha", command=self.abrir_janela_leiturinha).pack(pady=10)

    def processar_texto(self) -> None:
        """Abre um diálogo para selecionar um arquivo de texto."""
        self.caminho_arquivo = filedialog.askopenfilename(
            filetypes=[("Arquivos de texto", "*.txt *.pdf *.docx *.html")])
        if self.caminho_arquivo:
            tk.Label(self.root, text=f"Arquivo selecionado: {self.caminho_arquivo}").pack()

    def abrir_janela_leiturinha(self) -> None:
        """Abre a janela de exibição da Leiturinha."""
        if self.caminho_arquivo:
            self.leiturinha_window = tk.Toplevel(self.root)
            self.leiturinha_window.title("Leiturinha - visualização")
            if self.tela_cheia_var.get():
                self.leiturinha_window.attributes("-fullscreen", True)
            else:
                self.leiturinha_window.geometry("400x200")
                self.leiturinha_window.configure(bg="black")

            # Label para exibir a palavra atual
            self.label_palavra = tk.Label(self.leiturinha_window, font=("Arial", self.tamanho_fonte_var.get()))
            self.label_palavra.place(relx=0.5, rely=0.5, anchor="center")

            # Botão Pausar
            self.botao_pausar = tk.Button(self.leiturinha_window, text="Pausar", command=self.pausar_ou_retornar)
            self.botao_pausar.pack(side="left", padx=10)

            # Inicia a exibição das palavras
            self.exibir_palavras()

        else:
            messagebox.showwarning("Aviso", "Por favor, selecione um arquivo de texto primeiro.")

    def pausar_ou_retornar(self) -> None:
        """Alterna entre pausar e retornar a leitura."""
        self.pausado = not self.pausado
        self.botao_pausar.config(text="Retornar" if self.pausado else "Pausar")

    def exibir_palavras(self) -> None:
        """Lê e exibe as palavras da Leiturinha sem bloquear o loop principal."""
        conteudo = extrair_texto(self.caminho_arquivo)
        self.palavras = conteudo.split()
        self.total_palavras = len(self.palavras)
        self.posicao = int(self.percentual_posicao * self.total_palavras)
        self.exibir_proxima_palavra()  # Inicia a exibição das palavras

    def exibir_proxima_palavra(self) -> None:
        """Exibe a próxima palavra de forma assíncrona."""
        if self.posicao < self.total_palavras:
            if not self.pausado:
                centralizar_palavra(self.label_palavra, self.palavras[self.posicao], self.tamanho_fonte_var.get(),
                                    self.negrito_var.get())
                self.posicao += 1
                self.percentual_posicao = self.posicao / self.total_palavras
            delay = int(60000 / self.velocidade_var.get())
            self.root.after(delay, self.exibir_proxima_palavra)  # Chama a próxima palavra após o atraso configurado

