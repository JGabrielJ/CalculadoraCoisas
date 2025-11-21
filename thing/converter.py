import pygame
import tkinter as tk
from typing import Any
from thing import BONK_FILE, CONVERSION_OPTIONS, convert


class Converter(tk.Frame):
    def __init__(self, parent: tk.Widget, controller: Any) -> None:
        """Inicializa o frame do conversor de medidas.

        Args:
            parent (tk.Widget): O container da classe App.
            controller (App): A instância principal da aplicação.
        """
        super().__init__(parent, bg='#FFFFFF')

        # Mixer de Áudio do PyGame
        try:
            pygame.mixer.init()
            print('Mixer de áudio inicializado com sucesso.')
        except pygame.error as e:
            print(f'Dispositivo de áudio não encontrado. O som será desativado. Erro: {e}')
            self.play_sound = False
        else:
            self.play_sound = True

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

        # Título do Frame (Conversor)
        title_label = tk.Label(self, text='Conversor de Coisas', font=('Bahnschrift', 24, 'bold'), bg='#FFFFFF')
        title_label.grid(row=0, column=0, columnspan=3, sticky='nsew', pady=(10, 15))

        # Menu de Seleção da Categoria de Conversão
        self.category_menu = tk.OptionMenu(self, self.option_var, *CONVERSION_OPTIONS.keys())
        self.category_menu.config(width=25, font=('Consolas', 10, 'bold'), relief='raised', borderwidth=2)
        self.category_menu.grid(row=1, column=0, columnspan=3, padx=8, pady=(0, 5))

        # Labels e Menus de Unidade (Entrada)
        self.input_value = tk.Label(self, textvariable=self.input_value_var,
                                    font=('Cambria_Math', 32), bg='#FFFFFF')
        self.input_value.grid(row=2, column=0, columnspan=3, padx=8, sticky='nsw')

        self.input_title = tk.Label(self, text='De:', font=('Bahnschrift', 12, 'bold'), bg='#FFFFFF')
        self.input_title.grid(row=3, column=0, padx=8, sticky='nsew')

        self.input_menu = tk.OptionMenu(self, self.input_unit_var, '')
        self.input_menu.config(font=('Consolas', 10, 'bold'), relief='raised', borderwidth=3)
        self.input_menu.grid(row=3, column=1, columnspan=2, padx=8, sticky='ew')

        # Labels e Menus de Unidade (Saída)
        self.output_value = tk.Label(self, textvariable=self.output_value_var,
                                     font=('Cambria_Math', 32), bg='#FFFFFF')
        self.output_value.grid(row=4, column=0, columnspan=3, padx=8, sticky='nsw')

        self.output_title = tk.Label(self, text='Para:', font=('Bahnschrift', 12, 'bold'), bg='#FFFFFF')
        self.output_title.grid(row=5, column=0, padx=8, pady=(0, 20), sticky='nsew')

        self.output_menu = tk.OptionMenu(self, self.output_unit_var, '')
        self.output_menu.config(font=('Consolas', 10, 'bold'), relief='raised', borderwidth=3)
        self.output_menu.grid(row=5, column=1, columnspan=2, padx=8, pady=(0, 20), sticky='ew')

        # Inicialização dos Menus de Unidade
        self.__change_menu(); self.option_var.trace_add('write', lambda *args: self.__change_menu())

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
                button = tk.Button(self, text=text, font='Terminal', width=12, height=2, relief='raised',
                                   borderwidth=3, command=lambda t=text: self.__button_click(t))
            else:
                button = tk.Button(self, text=text, font='Terminal', width=12, height=2, bg='#FFFFFF',
                                   relief='flat', borderwidth=3, command=lambda t=text: self.__button_click(t))
            button.grid(row=row, column=column, padx=5, pady=5)

    def __change_menu(self) -> None:
        """Atualiza as opções nos menus de unidade com base na categoria escolhida."""

        # Reseta os valores ao trocar de categoria
        self.__clear()

        # Obtém a categoria selecionada
        category = self.option_var.get()
        options = CONVERSION_OPTIONS.get(category, ())

        # Limpa os menus de unidade antes de atualizá-los
        self.input_menu['menu'].delete(0, 'end')
        self.output_menu['menu'].delete(0, 'end')

        if options:
            for option in options:
                self.input_menu['menu'].add_command(label=option, command=tk._setit(self.input_unit_var, option))
                self.output_menu['menu'].add_command(label=option, command=tk._setit(self.output_unit_var, option))

            # Define a primeira opção da lista como o valor padrão
            self.input_unit_var.set(options[0]); self.output_unit_var.set(options[0])

    def __button_click(self, button: str) -> None:
        """Define as ações de cada botão do conversor.

        Args:
            button (str): O caractere do botão pressionado.
        """
        if button == ',': button = '.'

        if button == '✓':
            result = convert(
                category=self.option_var.get(),
                to_unit=self.output_unit_var.get(),
                from_unit=self.input_unit_var.get(),
                value=float(self.__unformat_number(self.input_value_var.get()))
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
            try:
                if self.play_sound:
                    pygame.mixer.music.load(BONK_FILE)
                    pygame.mixer.music.play()
            except pygame.error as e:
                print(f"Erro ao tocar o som: {e}")
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
