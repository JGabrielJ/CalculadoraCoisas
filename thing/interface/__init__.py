import tkinter as tk
from thing import ICON_PATH


class Interface:
    def __init__(self, window: tk.Tk) -> None:
        self.WINDOW = window
        self.WINDOW.title('Calculadora de Coisas')
        self.WINDOW.iconbitmap(ICON_PATH)
        self.WINDOW.resizable(False, False)
        self.WINDOW.config(background='#FFFFFF')
