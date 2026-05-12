import tkinter as tk
from typing import Any
from tkinter import ttk
from thing.widgets import DateSelector
from dateutil.relativedelta import relativedelta


class DateCalc(ttk.Frame):
    def __init__(self, parent: tk.Widget, controller: Any) -> None:
        """Inicializa o frame da calculadora de datas.

        Args:
            parent (tk.Widget): O container da classe App.
            controller (App): A instância principal da aplicação.
        """
        super().__init__(parent)

        # Configuração do grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(3, weight=1)

        # Título do frame (cálculo de data)
        ttk.Label(
            self, text="Cálculo de Datas", style="TTL.TLabel", anchor="center"
        ).grid(row=0, column=0, sticky="nsew", pady=15)

        # Seleção de modo (radio buttons)
        mode_frame = ttk.Frame(self)
        mode_frame.grid(row=1, column=0, sticky="ns", pady=(5, 15))
        self.mode_var = tk.StringVar(value="diff")

        ttk.Radiobutton(
            mode_frame,
            text="Diferença entre Datas",
            variable=self.mode_var,
            style="CDC.TRadiobutton",
            value="diff",
            command=self.__update_layout,
        ).grid(row=0, column=0, padx=10, sticky="w")

        ttk.Radiobutton(
            mode_frame,
            text="Adicionar/Subtrair Data",
            variable=self.mode_var,
            style="CDC.TRadiobutton",
            value="adsb",
            command=self.__update_layout,
        ).grid(row=0, column=1, padx=10, sticky="e")

        # Frame 1: diferença entre datas
        self.diff_frame = ttk.LabelFrame(
            self, text=" Calcular a Diferença ", labelanchor="nw", padding=(5, 10)
        )
        self.diff_frame.grid_columnconfigure(1, weight=1)

        # Widgets da opção de cálculo 1
        ttk.Label(self.diff_frame, text="Data Inicial:", style="PRG.TLabel").grid(
            row=0, column=0, padx=5, pady=5, sticky="e"
        )

        self.start_date_entry = DateSelector(
            self.diff_frame,
            controller,
            width=12,
            date_pattern="dd/mm/yyyy",
            background="darkblue",
            foreground="white",
            selectbackground="blue",
            selectforeground="white",
            headersbackground="gray",
            headersforeground="white",
        )
        self.start_date_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(self.diff_frame, text="Data Final:", style="PRG.TLabel").grid(
            row=1, column=0, padx=5, pady=5, sticky="e"
        )

        self.end_date_entry = DateSelector(
            self.diff_frame,
            controller,
            width=12,
            date_pattern="dd/mm/yyyy",
            background="darkblue",
            foreground="white",
            selectbackground="blue",
            selectforeground="white",
            headersbackground="gray",
            headersforeground="white",
        )
        self.end_date_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        ttk.Button(
            self.diff_frame,
            text="Calcular Diferença",
            style="CDC.TButton",
            command=self.__calculate_difference,
        ).grid(row=2, column=0, columnspan=2, pady=10)

        self.diff_result_var = tk.StringVar(value="Diferença: ")
        ttk.Label(
            self.diff_frame, textvariable=self.diff_result_var, style="PRG.TLabel"
        ).grid(row=3, column=0, columnspan=2, pady=5)

        # Frame 2: adicionar/subtrair data
        self.add_frame = ttk.LabelFrame(
            self,
            text=" Adicionar ou Subtrair de uma Data ",
            labelanchor="nw",
            padding=(5, 10),
        )
        self.add_frame.grid_columnconfigure(1, weight=1)

        # Widgets da opção de cálculo 2
        ttk.Label(self.add_frame, text="Data de Partida:", style="PRG.TLabel").grid(
            row=0, column=0, padx=5, pady=5, sticky="e"
        )

        self.base_date_entry = DateSelector(
            self.add_frame,
            controller,
            width=12,
            date_pattern="dd/mm/yyyy",
            background="darkblue",
            foreground="white",
            selectbackground="blue",
            selectforeground="white",
            headersbackground="gray",
            headersforeground="white",
        )
        self.base_date_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        # Inputs para dias, meses e anos (respectivamente)
        time_units_frame = ttk.Frame(self.add_frame)
        time_units_frame.grid(row=1, column=0, columnspan=2, pady=5)
        time_units_frame.grid_columnconfigure((0, 1, 2, 3, 4, 5), weight=1)

        ttk.Label(time_units_frame, text="Dias:", style="PRG.TLabel").grid(
            row=0, column=0, sticky="e"
        )
        self.days_spinbox = ttk.Spinbox(time_units_frame, from_=0, to=100, width=5)
        self.days_spinbox.grid(row=0, column=1, padx=(7, 15), sticky="w")
        self.days_spinbox.set(0)

        ttk.Label(time_units_frame, text="Meses:", style="PRG.TLabel").grid(
            row=0, column=2, sticky="e"
        )
        self.months_spinbox = ttk.Spinbox(time_units_frame, from_=0, to=100, width=5)
        self.months_spinbox.grid(row=0, column=3, padx=(7, 15), sticky="w")
        self.months_spinbox.set(0)

        ttk.Label(time_units_frame, text="Anos:", style="PRG.TLabel").grid(
            row=0, column=4, sticky="e"
        )
        self.years_spinbox = ttk.Spinbox(time_units_frame, from_=0, to=100, width=5)
        self.years_spinbox.grid(row=0, column=5, padx=(7, 15), sticky="w")
        self.years_spinbox.set(0)

        # Botões de ação
        buttons_frame = ttk.Frame(self.add_frame)
        buttons_frame.grid(row=2, column=0, columnspan=2, pady=10)
        buttons_frame.grid_columnconfigure((0, 1), weight=1)

        ttk.Button(
            buttons_frame,
            text="Adicionar",
            style="CDC.TButton",
            command=lambda: self.__add_subtract_date(add=True),
        ).grid(row=0, column=0, padx=10, sticky="e")

        ttk.Button(
            buttons_frame,
            text="Subtrair",
            style="CDC.TButton",
            command=lambda: self.__add_subtract_date(add=False),
        ).grid(row=0, column=1, padx=10, sticky="w")

        self.add_result_var = tk.StringVar(value="Nova data: ")
        ttk.Label(
            self.add_frame, textvariable=self.add_result_var, style="PRG.TLabel"
        ).grid(row=3, column=0, columnspan=2, pady=5)

        # Exibe o layout inicial
        self.__update_layout()

    def __update_layout(self) -> None:
        """Mostra ou esconde os frames de acordo com o modo selecionado."""
        mode = self.mode_var.get()

        if mode == "diff":
            # Exibe o painel de diferença entre datas
            self.add_frame.grid_forget()
            self.diff_frame.grid(row=2, column=0, padx=20, pady=10, sticky="ew")
        elif mode == "adsb":
            # Exibe o painel de adição/subtração de datas
            self.diff_frame.grid_forget()
            self.add_frame.grid(row=2, column=0, padx=20, pady=10, sticky="ew")

    def __calculate_difference(self) -> None:
        """Calcula e exibe a diferença entre as datas inicial e final."""
        try:
            start_date = self.start_date_entry.get_date()
            end_date = self.end_date_entry.get_date()

            if start_date and end_date:
                # Calcula a diferença entre as duas datas utilizando `relativedelta`
                delta = relativedelta(end_date, start_date)
                result_str = f"Diferença: {delta.years} anos, {delta.months} meses e {delta.days} dias."
                self.diff_result_var.set(result_str)
            else:
                self.diff_result_var.set(
                    "Erro! Ambas as datas devem ser selecionadas!!!"
                )

        except Exception:
            self.diff_result_var.set("Erro! Verifique os valores!!!")

    def __add_subtract_date(self, add: bool) -> None:
        """Adiciona ou subtrai dias/meses/anos a
        partir de uma data fornecida pelo usuário.

        Args:
            add (bool): Indica se é adição ou subtração.
        """
        try:
            base_date = self.base_date_entry.get_date()
            days = int(self.days_spinbox.get())
            months = int(self.months_spinbox.get())
            years = int(self.years_spinbox.get())

            if base_date:  # Garante que a data base foi selecionada
                # Cria um deslocamento de tempo e aplica ao valor base
                delta = relativedelta(days=days, months=months, years=years)
                new_date = base_date + delta if add else base_date - delta
                self.add_result_var.set(f"Nova data: {new_date.strftime('%d/%m/%Y')}")
            else:
                self.add_result_var.set("Erro! Selecione uma data de partida!!!")

        except (ValueError, TypeError):
            self.add_result_var.set("Erro! Verifique os valores!!!")
