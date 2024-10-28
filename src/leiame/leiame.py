import os
import webbrowser

def abrir_leiame_html() -> None:
    """Abre o arquivo LEIAME em um navegador web."""
    leiame_path = os.path.join(os.getcwd(), 'leiame.html')
    if os.path.exists(leiame_path):
        webbrowser.open(f"file://{leiame_path}")
    else:
        print("Arquivo LEIAME não encontrado.")
