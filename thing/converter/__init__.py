import tkinter as tk
import math, requests
from thing.interface import Interface


class Converter(Interface):
    def __init__(self, window: tk.Tk) -> None:
        super().__init__(window)
        self.value: str = '0'
        self.option: str = 'Moeda'
        self.__change_menu(window)

        self.switch = tk.Button(window, text='Conversor ⇄ Calculadora', font=('Bahnschrift', 18), relief='flat',
                              background='#FFFFFF', command=lambda: self.__open_calculator())
        self.switch.grid(row=0, column=0, columnspan=3, pady=8)

        self.input = tk.Label(window, text='0', width=12, anchor='w', font=('System', 36), background='#FFFFFF')
        self.input.grid(row=1, column=0, columnspan=3, padx=8)

        self.input_menu.config(width=7, font=('Fixedsys', 10), relief='raised', borderwidth=3, anchor='w')
        self.input_menu.grid(row=2, column=0, columnspan=3, padx=8, sticky='w')

        self.output = tk.Label(window, text='0', width=12, anchor='w', font=('System', 36), background='#FFFFFF')
        self.output.grid(row=3, column=0, columnspan=3, padx=8)

        self.output_menu.config(width=7, font=('Fixedsys', 10), relief='raised', borderwidth=3, anchor='w')
        self.output_menu.grid(row=4, column=0, columnspan=3, padx=8, sticky='w')

        BUTTONS: list[tuple] = [
            ('7', 5, 0), ('8', 5, 1), ('9', 5, 2),
            ('4', 6, 0), ('5', 6, 1), ('6', 6, 2),
            ('1', 7, 0), ('2', 7, 1), ('3', 7, 2),
            ('⌫', 8, 0), ('0', 8, 1), ('.', 8, 2)
        ]

        for (text, row, column) in BUTTONS:
            button = tk.Button(window, text=text, width=7, height=2, font=('Terminal', 12),
                               relief='raised', borderwidth=3, command=lambda t=text: self.__button_click(t))
            button.grid(row=row, column=column, padx=5, pady=5)


    def __change_menu(self, window: tk.Tk) -> None:
        match self.option:
            case 'Moeda':
                self.input_menu = tk.OptionMenu(window, tk.StringVar(value='De'), 'Real', 'Dólar', 'Euro', 'Bitcoin')
                self.output_menu = tk.OptionMenu(window, tk.StringVar(value='Para'), 'Real', 'Dólar', 'Euro', 'Bitcoin')
            case 'Volume':
                self.input_menu = tk.OptionMenu(window, tk.StringVar(value='De'), 'Litro', 'Mililitro', 'Metro Cúbico', 'Centímetro Cúbico')
                self.output_menu = tk.OptionMenu(window, tk.StringVar(value='Para'), 'Litro', 'Mililitro', 'Metro Cúbico', 'Centímetro Cúbico')
            case 'Distância':
                self.input_menu = tk.OptionMenu(window, tk.StringVar(value='De'), 'Milímetro', 'Centímetro', 'Metro', 'Quilômetro')
                self.output_menu = tk.OptionMenu(window, tk.StringVar(value='Para'), 'Milímetro', 'Centímetro', 'Metro', 'Quilômetro')
            case 'Peso':
                self.input_menu = tk.OptionMenu(window, tk.StringVar(value='De'), 'Miligrama', 'Grama', 'Quilograma', 'Tonelada')
                self.output_menu = tk.OptionMenu(window, tk.StringVar(value='Para'), 'Miligrama', 'Grama', 'Quilograma', 'Tonelada')
            case 'Temperatura':
                self.input_menu = tk.OptionMenu(window, tk.StringVar(value='De'), 'Celsius', 'Fahrenheit', 'Kelvin')
                self.output_menu = tk.OptionMenu(window, tk.StringVar(value='Para'), 'Celsius', 'Fahrenheit', 'Kelvin')
            case 'Área':
                self.input_menu = tk.OptionMenu(window, tk.StringVar(value='De'), 'Metro Quadrado', 'Quilômetro Quadrado', 'Hectare')
                self.output_menu = tk.OptionMenu(window, tk.StringVar(value='Para'), 'Metro Quadrado', 'Quilômetro Quadrado', 'Hectare')
            case 'Velocidade':
                self.input_menu = tk.OptionMenu(window, tk.StringVar(value='De'), 'Metros por Segundo', 'Quilômetros por Hora', 'Milhas por Hora', 'Mach')
                self.output_menu = tk.OptionMenu(window, tk.StringVar(value='Para'), 'Metros por Segundo', 'Quilômetros por Hora', 'Milhas por Hora', 'Mach')
            case 'Tempo':
                self.input_menu = tk.OptionMenu(window, tk.StringVar(value='De'), 'Milissegundo', 'Segundo', 'Minuto', 'Hora', 'Dia', 'Semana', 'Mês', 'Ano', 'Década', 'Século', 'Milênio', 'Era')
                self.output_menu = tk.OptionMenu(window, tk.StringVar(value='Para'), 'Milissegundo', 'Segundo', 'Minuto', 'Hora', 'Dia', 'Semana', 'Mês', 'Ano', 'Década', 'Século', 'Milênio', 'Era')
            case 'Dados':
                self.input_menu = tk.OptionMenu(window, tk.StringVar(value='De'), 'Bit', 'Byte', 'Kilobyte', 'Megabyte', 'Gigabyte', 'Terabyte')
                self.output_menu = tk.OptionMenu(window, tk.StringVar(value='Para'), 'Bit', 'Byte', 'Kilobyte', 'Megabyte', 'Gigabyte', 'Terabyte')
            case 'Ângulo':
                self.input_menu = tk.OptionMenu(window, tk.StringVar(value='De'), 'Graus', 'Radianos', 'Gradianos')
                self.output_menu = tk.OptionMenu(window, tk.StringVar(value='Para'), 'Graus', 'Radianos', 'Gradianos')


    def __button_click(self, button: str) -> None:
        if button == '✓':
            pass # Fazer a conversão
        elif button == '⌫':
            self.__delete()
        else:
            self.__update_output(button)

        self.__update_input()


    def __delete(self) -> None:
        self.value = self.value[:-1] if len(self.value) > 1 else '0'
        self.__update_input()


    def __update_input(self) -> None:
        self.input['text'] = self.value
    

    def __update_output(self, number: str) -> None:
        self.value = self.value + number if self.value != '0' else number


    def __open_calculator(self) -> None:
        self.WINDOW.destroy()
        from thing.calculator import Calculator

        calc_window = tk.Tk()
        Calculator(calc_window)
        calc_window.mainloop()
