import tkinter as tk
from tkinter import scrolledtext
from src.transcricao.transcricao import TranscricaoGUI
from src.resumo.resumo import ResumoGUI
from src.pdf.pdf import PDFGUI
from src.edicao.edicao import EdicaoGUI
from PIL import Image, ImageTk
from src.requisitos import verificar_api_key, definir_permissoes, verificar_ffmpeg_instalado, verificar_tesseract_instalado
import webbrowser
from src.utils_gui import show_api_key_prompt

api_disponivel: bool = verificar_api_key()


class MainGUI:
    def __init__(self, root: tk.Tk) -> None:
        """Inicializa a GUI principal.

        Args:
            root (tk.Tk): A instância raiz do Tkinter.
        """
        self.root = root
        self.root.title("Estudante v1.1")
        self.root.iconbitmap("src/icone.ico")

        if not api_disponivel:
            show_api_key_prompt(root)

        self.criar_frame_botoes()
        self.criar_botoes()
        self.criar_label_creditos()

    def criar_frame_botoes(self) -> None:
        """Cria um frame para organizar os botões horizontalmente."""
        self.frame_botoes = tk.Frame(self.root)
        self.frame_botoes.pack(pady=10)

    def criar_botoes(self) -> None:
        """Cria os botões principais com ícones."""
        botoes = [
            ("src/transcricao/transcrever.png", "Transcrever", self.abrir_transcricao),
            ("src/resumo/resumir.png", "Resumir", self.abrir_resumo, tk.NORMAL if api_disponivel else tk.DISABLED),
            ("src/pdf/pdf.png", "PDF", self.abrir_, tk.NORMAL if api_disponivel else tk.DISABLED),
            ("src/edicao/editar.png", "Revisar", self.abrir_edicao),
            ("src/leiame/leia_me.png", "Leia-me", self.abrir_leiame_html)
        ]

        for caminho_imagem, texto, comando, *estado in botoes:
            self.criar_botao_icone(self.frame_botoes, caminho_imagem, texto, comando, estado[0] if estado else tk.NORMAL)

    def criar_botao_icone(self, frame: tk.Frame, caminho_imagem: str, texto: str, comando: callable, estado: str = tk.NORMAL) -> None:
        """Cria um botão com ícone e texto.

        Args:
            frame (tk.Frame): O frame onde o botão será adicionado.
            caminho_imagem (str): O caminho para a imagem do ícone.
            texto (str): O texto a ser exibido no botão.
            comando (callable): A função a ser chamada quando o botão for clicado.
            estado (str, optional): O estado inicial do botão. Padrão é tk.NORMAL.
        """
        imagem = Image.open(caminho_imagem)
        imagem = imagem.resize((50, 50), Image.LANCZOS)
        icone = ImageTk.PhotoImage(imagem)
        botao = tk.Button(frame, image=icone, text=texto, compound="top", command=comando, state=estado)
        botao.image = icone
        botao.pack(side="left", padx=10)

    def criar_label_creditos(self) -> None:
        """Cria um label para créditos."""
        label_creditos = tk.Label(self.root, text="Desenvolvido por Pedro Duarte Blanco", fg="blue", cursor="hand2", font=("Arial", 14))
        label_creditos.pack(pady=(2, 15))
        label_creditos.bind("<Button-1>", lambda e: webbrowser.open("http://pedblan.wordpress.com"))

    def abrir_transcricao(self) -> None:
        """Abre a janela de transcrição."""
        nova_janela = tk.Toplevel(self.root)
        TranscricaoGUI(nova_janela)

    def abrir_resumo(self) -> None:
        """Abre a janela de resumo."""
        nova_janela = tk.Toplevel(self.root)
        ResumoGUI(nova_janela)

    def abrir_(self) -> None:
        """Abre a janela de ."""
        nova_janela = tk.Toplevel(self.root)
        PDFGUI(nova_janela)

    def abrir_edicao(self) -> None:
        """Abre a janela de edição."""
        nova_janela = tk.Toplevel(self.root)
        EdicaoGUI(nova_janela)

    def abrir_leiame_html(self) -> None:
        """Abre o conteúdo do README em uma nova janela."""
        caminho_leiame = "src/leiame/leiame.html"
        with open(caminho_leiame, "r", encoding="utf-8") as arquivo:
            conteudo = arquivo.read()

        janela_leiame = tk.Toplevel(self.root)
        janela_leiame.title("Leia-me")
        area_texto = scrolledtext.ScrolledText(janela_leiame, wrap=tk.WORD, width=80, height=30, font=("Arial", 12))
        area_texto.insert(tk.INSERT, conteudo)
        area_texto.configure(state='disabled')
        area_texto.pack(pady=10, padx=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = MainGUI(root)
    root.mainloop()