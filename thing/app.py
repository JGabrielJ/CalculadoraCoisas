import threading
import tkinter as tk
from tkinter import ttk, PhotoImage
from thing.datecalc import DateCalc
from thing.converter import Converter
from thing.calculator import Calculator
from thing import ICON_FILE, _fetch_currency_rates


class App(tk.Tk):
    def __init__(self, *args, **kwargs) -> None:
        """Janela principal da Calculadora de Coisas."""
        super().__init__(*args, **kwargs)

        # Configuração da janela principal
        self.title("Calculadora de Coisas")
        self.config(background="#FFFFFF")

        # Define o ícone da aplicação a partir do arquivo especificado
        icon_img = PhotoImage(file=ICON_FILE)
        self.iconphoto(False, icon_img)

        # Configura a grade principal para que o notebook ocupe toda a janela
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Configuração de estilos do app (notebook)
        style = ttk.Style()
        style.theme_use("clam")

        style.configure("CDC.TNotebook", background="#FFFFFF")
        style.configure(
            "CDC.TNotebook.Tab", font=("Bahnschrift", 10), background="#D9D9D9"
        )

        style.map(
            "CDC.TNotebook.Tab",
            background=[
                ("selected", "#D9D9D9"),
                ("active", "!selected", "#C0C0C0"),
                ("!disabled", "!selected", "#E0E0E0"),
            ],
        )

        # Configuração dos botões
        style.configure(
            "CDC.TButton", font=("Helvetica", 10, "bold"), focuscolor="none"
        )
        style.configure(
            "EGG.TButton",
            relief="flat",
            focuscolor="none",
            font=("Helvetica", 10, "bold"),
        )
        style.configure("CDC.TRadiobutton", font=("Helvetica", 10), focuscolor="none")

        # Configuração dos labels
        style.configure("PRG.TLabel", font=("Bahnschrift", 12))
        style.configure("TTL.TLabel", font=("Bahnschrift", 24, "bold"))
        style.configure("NUM.TLabel", font=("Cambria_Math", 32))

        # Cria o notebook (abas) e o posiciona na janela principal
        notebook = ttk.Notebook(self, style="CDC.TNotebook")
        notebook.grid(row=0, column=0, columnspan=2, sticky="nsew", padx=10, pady=10)

        # Cria cada aba do aplicativo como um frame separado
        calculator_frame = Calculator(notebook, self)
        converter_frame = Converter(notebook, self)
        datecalc_frame = DateCalc(notebook, self)

        # Adiciona os frames ao notebook com seus rótulos de aba
        notebook.add(calculator_frame, text="Calculadora")
        notebook.add(converter_frame, text="Conversor")
        notebook.add(datecalc_frame, text="Cálculo de Data")

        # Centraliza a janela no meio da tela
        self.update_idletasks()

        width = self.winfo_width()
        height = self.winfo_height()

        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)

        self.geometry(f"{width}x{height}+{x}+{y}")

        # Pré-carrega as cotações de moeda em segundo plano para
        # evitar travamentos durante o uso do conversor de moeda
        threading.Thread(target=_fetch_currency_rates, daemon=True).start()
