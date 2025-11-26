import tkinter as tk
from typing import Any
from tkinter import ttk
from thing import CONVERSION_OPTIONS, convert


class Converter(ttk.Frame):
    def __init__(self, parent: tk.Widget, controller: Any) -> None:
        """Inicializa o frame do conversor de medidas.

        Args:
            parent (tk.Widget): O container da classe App.
            controller (App): A instância principal da aplicação.
        """
        super().__init__(parent)

        # Configuração do Grid
        for c in range(3):
            self.grid_columnconfigure(c, weight=1)
        for r in range(11):
            self.grid_rowconfigure(r, weight=1)

        # Variáveis de Estado
        self.max_digits: int = 16
        self.input_unit_var = tk.StringVar()
        self.output_unit_var = tk.StringVar()
        self.input_value_var = tk.StringVar(value='0')
        self.output_value_var = tk.StringVar(value='0')
        self.option_var = tk.StringVar(value='Contagem')

        # Configuração das Listas de Seleção
        self.option_add('*TCombobox*font', ('Consolas', 10))
        self.option_add('*TCombobox*Listbox.font', ('Consolas', 10))

        # Título do Frame (Conversor)
        ttk.Label(self, text='Conversor de Coisas', style='TTL.TLabel', anchor='center')\
            .grid(row=0, column=0, columnspan=3, sticky='nsew', pady=15)

        self.category_menu = ttk.Combobox(self, textvariable=self.option_var, font=('Consolas', 10),
                                          values=list(CONVERSION_OPTIONS.keys()), state='readonly')
        self.category_menu.grid(row=1, column=0, columnspan=3, sticky='nsew', padx=100, pady=(0, 5))

        # Labels e Menus de Unidade (Entrada)
        ttk.Label(self, textvariable=self.input_value_var, anchor='w', style='NUM.TLabel')\
            .grid(row=2, column=0, columnspan=3, padx=8, sticky='nsew')

        ttk.Label(self, text='De:', anchor='center', style='PRG.TLabel')\
            .grid(row=3, column=0, padx=8, sticky='nsew')

        self.input_menu = ttk.Combobox(self, textvariable=self.input_unit_var,
                                       font=('Consolas', 10), state='readonly')
        self.input_menu.grid(row=3, column=1, columnspan=2, padx=8, sticky='nsew')

        # Labels e Menus de Unidade (Saída)
        ttk.Label(self, textvariable=self.output_value_var, anchor='w', style='NUM.TLabel')\
            .grid(row=4, column=0, columnspan=3, padx=8, sticky='nsew')

        ttk.Label(self, text='Para:', anchor='center', style='PRG.TLabel')\
            .grid(row=5, column=0, padx=8, pady=(0, 20), sticky='nsew')

        self.output_menu = ttk.Combobox(self, textvariable=self.output_unit_var,
                                        font=('Consolas', 10), state='readonly')
        self.output_menu.grid(row=5, column=1, columnspan=2, padx=8, pady=(0, 20), sticky='nsew')

        # Inicialização dos Menus de Unidade
        self.__change_menu(); self.category_menu.bind('<<ComboboxSelected>>', self.__change_menu)

        # Lista de Botões do Conversor
        buttons: list[tuple] = [
            ('', 6, 0), ('C', 6, 1), ('✓', 6, 2),
            ('7', 7, 0), ('8', 7, 1), ('9', 7, 2),
            ('4', 8, 0), ('5', 8, 1), ('6', 8, 2),
            ('1', 9, 0), ('2', 9, 1), ('3', 9, 2),
            ('⌫', 10, 0), ('0', 10, 1), (',', 10, 2)
        ]

        for (text, row, column) in buttons:
            if text:
                button = ttk.Button(self, text=text, style='CDC.TButton', command=lambda t=text: self.__button_click(t))
            else:
                button = ttk.Button(self, text=text, style='EGG.TButton', command=lambda t=text: self.__button_click(t))
            button.grid(row=row, column=column, padx=5, pady=5, sticky='nsew')

    def __change_menu(self, event=None) -> None:
        """Atualiza as opções nos menus de unidade com base na categoria escolhida."""

        # Reseta os valores ao trocar de categoria
        self.__clear()

        # Obtém a categoria selecionada
        category = self.option_var.get()
        options = CONVERSION_OPTIONS.get(category, ())

        # Atualiza os valores dos Comboboxes
        self.input_menu['values'] = options
        self.output_menu['values'] = options

        # Define a primeira opção da lista como o valor padrão
        if options:
            self.input_unit_var.set(options[0])
            self.output_unit_var.set(options[0])

    def __button_click(self, button: str) -> None:
        """Define as ações de cada botão do conversor.

        Args:
            button (str): O caractere do botão pressionado.
        """
        if button == ',': button = '.'

        if button == '✓':
            input_val = self.input_value_var.get()

            if input_val == '∞':
                self.output_value_var.set('∞'); return

            result = convert(
                category=self.option_var.get(),
                to_unit=self.output_unit_var.get(),
                from_unit=self.input_unit_var.get(),
                value=float(self.__unformat_number(input_val))
            )

            # Limita o resultado ao número máximo de dígitos
            if len(result) > self.max_digits:
                result = result[:self.max_digits]
            self.output_value_var.set(result)
        elif button == 'C':
            self.__clear()
        elif button == '⌫':
            self.__delete()
        elif not button:
            self.input_value_var.set('∞')
        elif button:
            self.__append_digit(button)

    def __format_number(self, number_str: str) -> str:
        """Formata uma string numérica para o padrão brasileiro.
        
        Args:
            number_str (str): A string numérica a ser formatada.

        Returns:
            str: A string formatada.
        """
        if 'e' in number_str.lower() or number_str in ("Erro", "N/A"):
            return number_str.replace('.', ',')

        parts = number_str.split('.'); integer_part = parts[0]
        decimal_part = parts[1] if len(parts) > 1 else None

        integer_part_formatted = f'{int(integer_part):,}'.replace(',', '.')

        if decimal_part is not None:
            return f'{integer_part_formatted},{decimal_part}'
        return integer_part_formatted

    def __unformat_number(self, formatted_str: str) -> str:
        """Converte uma string no padrão brasileiro de volta para o padrão do Python.

        Args:
            formatted_str (str): A string formatada.

        Returns:
            str: A string no padrão do Python.
        """
        return formatted_str.replace('.', '').replace(',', '.')

    def __clear(self) -> None:
        """Reseta o conversor para o estado inicial."""
        self.input_value_var.set('0'); self.output_value_var.set('0')

    def __delete(self) -> None:
        """Remove o último dígito inserido no input."""
        current = self.__unformat_number(self.input_value_var.get())

        if len(current) == 1:
            self.input_value_var.set('0')
        else:
            self.input_value_var.set(self.__format_number(current[:-1]))

    def __append_digit(self, number: str) -> None:
        """Adiciona um algarismo no input.

        Args:
            number (str): O dígito ou `.` a ser inserido.
        """
        current = self.__unformat_number(self.input_value_var.get())

        # Adiciona um dígito apenas se o limite não foi atingido
        if len(current) < self.max_digits:
            if current == '0' and number != '.':
                self.input_value_var.set(self.__format_number(number))
            else:
                # Evita adicionar múltiplos pontos decimais
                if number == '.' and '.' in current: return
                self.input_value_var.set(self.__format_number(current + number))
