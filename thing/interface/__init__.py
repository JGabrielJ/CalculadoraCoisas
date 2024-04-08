import tkinter as tk
from thing import icon_path


class Interface:
    def __init__(self, window: tk.Tk) -> None:
        self.window = window
        self.window.title('Calculadora de Coisas')
        self.window.iconbitmap(icon_path)
        self.window.resizable(False, False)
        self.window.config(background='#FFFFFF')
