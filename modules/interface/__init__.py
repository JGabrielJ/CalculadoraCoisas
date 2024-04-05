import tkinter as tk
from modules import icon_path


class Interface:
    def __init__(self, window: tk.Tk) -> None:
        self.window = window
        self.window.title('Calculadora de Coisas')
        self.window.iconbitmap(icon_path)
        self.window.config(background='#FFFFFF')
