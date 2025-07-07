#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright (c) 2024 Pedro Duarte Blanco
#
# Este software é distribuído sob a Licença MIT.
# Consulte o arquivo LICENSE para obter mais informações.

from src.gui import MainGUI
import tkinter as tk
from src.requisitos import definir_permissoes

def main() -> None:
    """Função principal que verifica os requisitos do sistema e inicia a interface gráfica."""
    definir_permissoes()
    root = tk.Tk()
    MainGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
