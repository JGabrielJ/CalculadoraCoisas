import threading
import tkinter as tk
from typing import Any
from tkinter import PhotoImage
from thing.datecalc import DateCalc
from thing.converter import Converter
from thing.calculator import Calculator
from thing import ICON_FILE, _fetch_currency_rates


class App(tk.Tk):
    def __init__(self, *args, **kwargs) -> None:
        """Janela principal da Calculadora de Coisas."""
        super().__init__(*args, **kwargs)

        # Configuração da Janela Principal
        self.title('Calculadora de Coisas')
        self.config(bg='#FFFFFF')

        icon_img = PhotoImage(file=ICON_FILE)
        self.iconphoto(False, icon_img)

        self.resizable(False, False)

        # Layout Principal com Barra Lateral
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Barra Lateral (Sidebar)
        sidebar_frame = tk.Frame(self, width=150, bg='#F0F0F0')
        sidebar_frame.grid(row=0, column=0, sticky='nsw')
        sidebar_frame.grid_rowconfigure(4, weight=1)

        # Botões de navegação na barra lateral
        menu_title = tk.Label(sidebar_frame, text='Menu', bg='#F0F0F0',
                              font=('Bahnschrift', 16, 'bold'))
        menu_title.grid(row=0, column=0, sticky='ew', pady=(5, 5))

        calc_button = tk.Button(sidebar_frame, text='Calculadora', font=('Bahnschrift', 12),
                                command=lambda: self.show_frame(Calculator))
        calc_button.grid(row=1, column=0, sticky='ew', padx=10, pady=7)

        conv_button = tk.Button(sidebar_frame, text='Conversor', font=('Bahnschrift', 12),
                                command=lambda: self.show_frame(Converter))
        conv_button.grid(row=2, column=0, sticky='ew', padx=10, pady=7)

        date_button = tk.Button(sidebar_frame, text='Cálculo de Data', font=('Bahnschrift', 12),
                                command=lambda: self.show_frame(DateCalc))
        date_button.grid(row=3, column=0, sticky='ew', padx=10, pady=7)

        # Container para as telas principais
        container = tk.Frame(self, bg='#FFFFFF')
        container.grid(row=0, column=1, sticky='nsew')
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # Dicionário para guardar os frames
        self.frames = {}

        # Criação e adição de cada frame ao dicionário
        for F in (Calculator, Converter, DateCalc):
            frame = F(container, self); self.frames[F] = frame
            frame.grid(row=0, column=0, sticky='nsew')

        # Exibição da tela inicial (Calculadora)
        self.show_frame(Calculator); self._center_window()

        # Pré-carrega as cotações de moeda em segundo plano para evitar travamentos
        threading.Thread(target=_fetch_currency_rates, daemon=True).start()

    def show_frame(self, cont: Any) -> None:
        """Mostra a tela (frame) na janela do app.

        Args:
            cont (Any): A classe da tela que será mostrada.
        """

        frame = self.frames[cont]; frame.tkraise()

    def _center_window(self) -> None:
        """Centraliza a janela na tela do computador."""

        self.update_idletasks() # Obtém largura e altura da janela
        width = self.winfo_width(); height = self.winfo_height()

        # Calcula a posição para centralizar a janela
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)

        self.geometry(f'{width}x{height}+{x}+{y}')
