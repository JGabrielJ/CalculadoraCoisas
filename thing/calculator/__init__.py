import math
import tkinter as tk
from thing.interface import Interface


class Calculator(Interface):
    def __init__(self, window: tk.Tk) -> None:
        super().__init__(window)
        self.equation: str = '0'

        self.title = tk.Label(window, text='Calculadora', font=('Bahnschrift', 18), background='#FFFFFF')
        self.title.grid(row=0, column=0, columnspan=5, pady=8)

        self.display = tk.Label(window, text='0', width=21, anchor='e', font=('System', 36), background='#C3EBEB')
        self.display.grid(row=1, column=0, columnspan=5, padx=8)

        buttons: list[tuple[str, int]] = [
            ('C', 2, 0), ('sin()', 2, 1), ('cos()', 2, 2), ('tan()', 2, 3), ('⌫', 2, 4),
            ('π', 3, 0), ('(', 3, 1), (')', 3, 2), ('%', 3, 3), ('/', 3, 4),
            ('√', 4, 0), ('7', 4, 1), ('8', 4, 2), ('9', 4, 3), ('*', 4, 4),
            ('^', 5, 0), ('4', 5, 1), ('5', 5, 2), ('6', 5, 3), ('-', 5, 4),
            ('10ⁿ', 6, 0), ('1', 6, 1), ('2', 6, 2), ('3', 6, 3), ('+', 6, 4),
            ('n!', 7, 0), ('|x|', 7, 1), ('0', 7, 2), ('.', 7, 3), ('=', 7, 4)
        ]

        for (txt, r, c) in buttons:
            button = tk.Button(window, text=txt, width=7, height=2, font=('Terminal', 12),
                               relief='raised', borderwidth=3, command=lambda t=txt: self.__button_click(t))
            button.grid(row=r, column=c, padx=5, pady=5)

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

    def __funct(self, val: str) -> None:
        parc_result: int | float | str
        final_result: int | float | str

        try:
            parc_result = eval(self.equation.replace('^', '**'))
        except SyntaxError:
            parc_result = 'Error'

        if parc_result != 'Error':
            match val:
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
                    try:
                        final_result = math.factorial(parc_result)
                    except (TypeError, ValueError):
                        final_result = 'Error'
                    self.equation = str(final_result)
                case '|x|':
                    final_result = abs(parc_result)
                    self.equation = str(final_result)
        else:
            self.equation = parc_result

    def __scien(self) -> None:
        exp: int = 0
        num: int | float

        try:
            num = int(eval(self.equation))
        except SyntaxError:
            self.equation = 'Error'
        else:
            while num >= 10:
                num /= 10
                exp += 1

            num = math.ceil(num * 100) / 100
            self.equation = f'{num}*10^{exp}'

    def __perc(self) -> None:
        result: float = 0
        values = self.__format_perc()

        num: float = float(values[0])
        if len(values) > 1:
            dif: float = float(values[1])
            opr: str = values[2]
            inc: float = (num * dif / 100)

            match opr:
                case '+':
                    result = num + inc
                case '-':
                    result = num - inc
                case '*':
                    result = num * inc
                case '/':
                    result = num / inc
        else:
            result = num / 100

        self.equation = str(result)

    def __format_perc(self) -> list[str]:
        v: list[str] = ['0']
        o: list[str] | str = ['+', '-', '*', '/']
        self.equation = self.equation.replace('(', '').replace(')', '').replace('^', '**')

        for t in self.equation:
            if t in o:
                o = t
                break

        if len(o) != 1 or '**' in self.equation or self.equation[0] == '-':
            try:
                n = str(eval(self.equation))
            except SyntaxError:
                self.equation = 'Error'
            else:
                v = [n]
        else:
            n = self.equation.split(o)
            v = [n[0], n[1], o]

        return v

    def __update_display(self) -> None:
        self.display['text'] = self.equation
