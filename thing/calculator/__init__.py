import math
import tkinter as tk
from thing.interface import Interface


class Calculator(Interface):
    def __init__(self, window: tk.Tk) -> None:
        super().__init__(window)
        self.equation: str = '0'

        self.switch = tk.Button(window, text='Calculadora ⇄ Conversor', font=('Bahnschrift', 18), relief='flat',
                              background='#FFFFFF', command=lambda: self.__open_converter())
        self.switch.grid(row=0, column=0, columnspan=5, pady=8)

        self.display = tk.Label(window, text='0', width=21, anchor='e', font=('System', 36), background='#C3EBEB')
        self.display.grid(row=1, column=0, columnspan=5, padx=8)

        BUTTONS: list[tuple] = [
            ('C', 2, 0), ('sin()', 2, 1), ('cos()', 2, 2), ('tan()', 2, 3), ('⌫', 2, 4),
            ('π', 3, 0), ('(', 3, 1), (')', 3, 2), ('%', 3, 3), ('/', 3, 4),
            ('√', 4, 0), ('7', 4, 1), ('8', 4, 2), ('9', 4, 3), ('*', 4, 4),
            ('^', 5, 0), ('4', 5, 1), ('5', 5, 2), ('6', 5, 3), ('-', 5, 4),
            ('10ⁿ', 6, 0), ('1', 6, 1), ('2', 6, 2), ('3', 6, 3), ('+', 6, 4),
            ('n!', 7, 0), ('|x|', 7, 1), ('0', 7, 2), ('.', 7, 3), ('=', 7, 4)
        ]

        for (text, row, column) in BUTTONS:
            button = tk.Button(window, text=text, width=7, height=2, font=('Terminal', 12),
                               relief='raised', borderwidth=3, command=lambda t=text: self.__button_click(t))
            button.grid(row=row, column=column, padx=5, pady=5)


    def __button_click(self, value: str) -> None:
        if value == '^':
            value = '**'

        if value == '=':
            try:
                self.equation = str(eval(self.equation))
            except (SyntaxError, NameError, ZeroDivisionError):
                self.equation = 'Error'
        elif value == 'C':
            self.__clear()
        elif value == '⌫':
            self.__delete()
        elif value == 'π':
            self.equation = str(math.pi)
        elif value in ['sin()', 'cos()', 'tan()', '√', 'n!', '|x|']:
            self.__funct(value)
        elif value == '%':
            self.__perc()
        elif value == '10ⁿ':
            self.__scien()
        else:
            self.equation = self.equation + value if self.equation != '0' else value

        self.__update_display()


    def __clear(self) -> None:
        self.equation = '0'
        self.__update_display()


    def __delete(self) -> None:
        self.equation = self.equation[:-1] if len(self.equation) > 1 else '0'
        self.__update_display()


    def __funct(self, value: str) -> None:
        parc_result: int | float
        final_result: int | float | str

        try:
            parc_result = eval(self.equation.replace('^', '**'))

            match value:
                case 'sin()':
                    final_result = math.sin(parc_result)
                    self.equation = str(final_result)
                case 'cos()':
                    final_result = math.cos(parc_result)
                    self.equation = str(final_result)
                case 'tan()':
                    final_result = math.tan(parc_result)
                    self.equation = str(final_result)
                case '√':
                    try:
                        final_result = math.sqrt(parc_result)
                    except ValueError:
                        final_result = 'Error'
                    self.equation = str(final_result)
                case 'n!':
                    parc_result = int(parc_result)
                    try:
                        final_result = math.factorial(parc_result)
                    except ValueError:
                        final_result = 'Error'
                    self.equation = str(final_result)
                case '|x|':
                    final_result = abs(parc_result)
                    self.equation = str(final_result)
        except SyntaxError:
            self.equation = 'Error'


    def __scien(self) -> None:
        exponent: int = 0
        number: int | float

        try:
            number = int(eval(self.equation))
        except SyntaxError:
            self.equation = 'Error'
        else:
            while number >= 10:
                number /= 10
                exponent += 1

            number = math.ceil(number * 100) / 100
            self.equation = f'{number}*10^{exponent}'


    def __perc(self) -> None:
        result: float = 0
        VALUES = self.__format_perc()

        NUMBER: float = float(VALUES[0])
        if len(VALUES) > 1:
            DIFFERENCE: float = float(VALUES[1])
            OPERATION: str = VALUES[2]
            INCREMENT: float = (NUMBER * DIFFERENCE / 100)

            match OPERATION:
                case '+':
                    result = NUMBER + INCREMENT
                case '-':
                    result = NUMBER - INCREMENT
                case '*':
                    result = NUMBER * INCREMENT
                case '/':
                    result = NUMBER / INCREMENT
        else:
            result = NUMBER / 100

        self.equation = str(result)


    def __format_perc(self) -> list[str]:
        number: str | list[str]
        value: list[str] = ['0']
        operation: list[str] = ['+', '-', '*', '/']
        self.equation = self.equation.replace('(', '').replace(')', '').replace('^', '**')

        for digit in self.equation:
            if digit in operation:
                operation = [digit]
                break

        if len(operation) != 1 or '**' in self.equation or self.equation[0] == '-':
            try:
                number = str(eval(self.equation))
            except SyntaxError:
                self.equation = 'Error'
            else:
                value = [number]
        else:
            number = self.equation.split(operation[0])
            value = [number[0], number[1], operation[0]]

        return value


    def __update_display(self) -> None:
        self.display['text'] = self.equation


    def __open_converter(self) -> None:
        self.WINDOW.destroy()
        from thing.converter import Converter

        conv_window = tk.Tk()
        Converter(conv_window)
        conv_window.mainloop()
