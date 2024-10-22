#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright (c) 2024 Pedro Duarte Blanco
#
# Este software é distribuído sob a Licença MIT.
# Consulte o arquivo LICENSE para obter mais informações.

from src.tarefas_principais import verificar_requisitos_sistema
from src.gui_main import MainGUI


def main():
    if verificar_requisitos_sistema():
        import tkinter as tk
        root = tk.Tk()
        app = MainGUI(root)
        root.mainloop()
          # Chama a função de iniciar a interface, que agora está em outro arquivo

if __name__ == "__main__":
    main()
