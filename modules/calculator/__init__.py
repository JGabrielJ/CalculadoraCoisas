import tkinter as tk
from modules.interface import Interface
from math import pi, sin, cos, tan, sqrt, pow, factorial


class Calculator(Interface):
    def __init__(self, window: tk.Tk) -> None:
        super().__init__(window)
        self.equation = ''

        self.title = tk.Label(window, text='Calculadora', font=('Bahnschrift', 18), background='#FFFFFF')
        self.title.grid(row=0, column=0, columnspan=5, pady=8)

        self.display = tk.Entry(window, cursor='xterm', width=21, font=('System', 36),
                                justify='right', background='#C3EBEB')
        self.display.grid(row=1, column=0, columnspan=5, padx=8)

        buttons = [
            ('C', 2, 0, ''), ('sin()', 2, 1, ''), ('cos()', 2, 2, ''), ('tan()', 2, 3, ''), ('%', 2, 4, ''),
            ('√', 3, 0, ''), ('(', 3, 1, ''), (')', 3, 2, ''), ('π', 3, 3, ''), ('/', 3, 4, ''),
            ('^', 4, 0, ''), ('7', 4, 1, ''), ('8', 4, 2, ''), ('9', 4, 3, ''), ('*', 4, 4, ''),
            ('10ⁿ', 5, 0, ''), ('4', 5, 1, ''), ('5', 5, 2, ''), ('6', 5, 3, ''), ('-', 5, 4, ''),
            ('n!', 6, 0, ''), ('1', 6, 1, ''), ('2', 6, 2, ''), ('3', 6, 3, ''), ('+', 6, 4, ''),
            ('n?', 7, 0, ''), ('|x|', 7, 1, ''), ('0', 7, 2, ''), ('.', 7, 3, ''), ('=', 7, 4, '')
        ]

        for (txt, r, c, cmd) in buttons:
            button = tk.Button(window, text=txt, width=7, height=2, font=('Terminal', 12),
                               relief='raised', borderwidth=3, command=cmd)
            button.grid(row=r, column=c, padx=5, pady=5)
