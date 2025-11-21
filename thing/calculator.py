import math, re
import tkinter as tk
from typing import Any


class Calculator(tk.Frame):
    def __init__(self, parent: tk.Widget, controller: Any) -> None:
        """Inicializa o frame da calculadora principal.

        Args:
            parent (tk.Widget): O container da classe App.
            controller (App): A instância principal da aplicação.
        """
        super().__init__(parent, bg='#FFFFFF')

        # Configuração do Grid
        for c in range(5):
            self.grid_columnconfigure(c, weight=1)
        for r in range(8):
            self.grid_rowconfigure(r, weight=1)

        # Variáveis de Estado
        self.max_digits: int = 16
        self.is_result: bool = False
        self.equation_var = tk.StringVar(value='0')

        # Título do Frame (Calculadora)
        title_label = tk.Label(self, text='Calculadora de Coisas', font=('Bahnschrift', 24, 'bold'), bg='#FFFFFF')
        title_label.grid(row=0, column=0, columnspan=5, sticky='nsew', pady=(10, 15))

        # Display das Equações e Resultados
        self.display = tk.Label(self, textvariable=self.equation_var, anchor='e',
                                font=('Cambria_Math', 32), bg='#C3EBEB')
        self.display.grid(row=1, column=0, columnspan=5, sticky='nsew', padx=8, pady=(0, 15))

        # Lista de Botões da Calculadora
        buttons: list[tuple] = [
            ('C', 2, 0), ('sin', 2, 1), ('cos', 2, 2), ('tan', 2, 3), ('⌫', 2, 4),
            ('π', 3, 0), ('(', 3, 1), (')', 3, 2), ('%', 3, 3), ('÷', 3, 4),
            ('sqrt', 4, 0), ('7', 4, 1), ('8', 4, 2), ('9', 4, 3), ('×', 4, 4),
            ('^', 5, 0), ('4', 5, 1), ('5', 5, 2), ('6', 5, 3), ('-', 5, 4),
            ('scien', 6, 0), ('1', 6, 1), ('2', 6, 2), ('3', 6, 3), ('+', 6, 4),
            ('fact', 7, 0), ('abs', 7, 1), ('0', 7, 2), (',', 7, 3), ('=', 7, 4)
        ]

        for (text, row, column) in buttons:
            button = tk.Button(self, text=text, font='Terminal', width=6, height=3, relief='raised',
                               borderwidth=3, command=lambda t=text: self.__button_click(t))
            button.grid(row=row, column=column, pady=5)

    def __button_click(self, value: str) -> None:
        """Define as ações de cada botão da calculadora.

        Args:
            value (str): O valor do botão pressionado.
        """
        if value == ',': value = '.'

        if value == '=':
            self.__calculate()
        elif value == 'C':
            self.__clear()
        elif value == '⌫':
            self.__delete()
        elif value == '%':
            self.__handle_percentage()
        elif value in ['sin', 'cos', 'tan', 'sqrt', 'fact', 'abs', 'scien']:
            self.__apply_immediate_function(value)
        else:
            self.__update_display(value)

    def __format_number(self, number_str: str) -> str:
        """Formata uma string numérica para o padrão brasileiro.
        
        Args:
            number_str (str): A string numérica a ser formatada.

        Returns:
            str: A string formatada.
        """
        if 'e' in number_str.lower():
            return number_str.replace('.', ',')

        parts = number_str.split('.'); integer_part = parts[0]
        decimal_part = parts[1] if len(parts) > 1 else None

        # Adiciona separadores de milhar
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
        """Reseta a calculadora para o estado inicial."""
        self.equation_var.set('0'); self.is_result = False

    def __delete(self) -> None:
        """Remove o último caractere da equação."""
        current = self.__unformat_number(self.equation_var.get())

        # Se for um resultado ou um único dígito, limpa a tela.
        if self.is_result or len(current) == 1:
            self.equation_var.set('0')
        else:
            self.equation_var.set(self.__format_number(current[:-1]))

        self.is_result = False

    def __apply_immediate_function(self, func: str) -> None:
        """Aplica uma função matemática ao número que está
        aparecendo no visor, exibindo o resultado imediatamente.

        Args:
            func (str): O nome da função a ser executada.
        """
        try:
            result: float = 0
            # Avalia a expressão atual para obter um número e
            # substitui `π` pelo valor de `math.pi` para o cálculo
            current_value = eval(self.__unformat_number(self.equation_var.get()).replace('π', 'math.pi'))

            # Executa a função selecionada pelo usuário
            match func:
                case 'sin':
                    result = math.sin(math.radians(current_value))
                case 'cos':
                    result = math.cos(math.radians(current_value))
                case 'tan':
                    if current_value % 180 == 90:
                        raise ValueError("Tangente indefinida!!!")
                    result = math.tan(math.radians(current_value))
                case 'sqrt':
                    result = math.sqrt(current_value)
                case 'fact':
                    result = math.factorial(int(current_value))
                case 'abs':
                    result = abs(current_value)
                case 'scien':
                    self.__scientific(current_value)
                    self.is_result = True; return

            # Mostra o resultado no visor, arredondado para 10 casas decimais
            self.equation_var.set(self.__format_number(str(round(result, 10)))); self.is_result = True

        except (ValueError, TypeError, SyntaxError):
            # Em caso de erro matemático ou de sintaxe, exibe uma mensagem de erro no visor
            self.equation_var.set("Erro"); self.is_result = True

    def __calculate(self) -> None:
        """Avalia a expressão final quando `=` é pressionado."""

        try:
            expression = self.__unformat_number(self.equation_var.get())

            # Substitui os símbolos visuais por operadores/funções do Python
            expression = expression.replace('×', '*')
            expression = expression.replace('÷', '/')
            expression = expression.replace('^', '**')
            expression = expression.replace('π', 'math.pi')

            # Adiciona multiplicação implícita para π
            expression = re.sub(r"(\d+)(math\.pi)", r"\1*\2", expression)
            expression = re.sub(r"(math\.pi)(\d+)", r"\1*\2", expression)

            # Adiciona multiplicação implícita para parênteses
            expression = re.sub(r"(\d+|\))\(", r"\1*(", expression)

            # Filtro de segurança que garante que a expressão contenha apenas caracteres permitidos
            if not re.match(r"^[0-9+\-*/().\s,a-z_]+$", expression):
                raise ValueError("Caracteres inválidos na expressão!!!")

            # Executa `eval()` em um ambiente seguro para prevenir a execução de código malicioso
            safe_env = {"math": math, "abs": abs, "__builtins__": {}}
            result = eval(expression, safe_env)

            # Formata o resultado para remover `.0` de números inteiros
            if result == int(result): result = int(result)
            self.equation_var.set(self.__format_number(str(result))); self.is_result = True

        except (SyntaxError, NameError, ZeroDivisionError, ValueError, TypeError):
            self.equation_var.set("Erro"); self.is_result = True

    def __handle_percentage(self) -> None:
        """Lida com cálculos de porcentagem:
        - Se o formato for `número`, calcula `número / 100`;
        - Se o formato for `{base}{op}{perc}`, calcula o resultado contextual.
        """
        current_equation = self.__unformat_number(self.equation_var.get())

        # Regex para encontrar um padrão como `100+10` no final da string
        match = re.search(r"(\d+\.?\d*)([+\-×÷])(\d+\.?\d*)$", current_equation)

        try:
            if match:
                # Cálculo contextual (ex.: 100 + 10%)
                base_num, operator, perc_num = match.groups()
                base_num, perc_num = float(base_num), float(perc_num)
                increment = base_num * (perc_num / 100); result: float = 0

                match operator:
                    case '+': result = base_num + increment
                    case '-': result = base_num - increment
                    case '×': result = base_num * increment
                    case '÷': result = base_num / increment

                self.equation_var.set(self.__format_number(str(result)))
            else:
                # Conversão simples (ex.: 50% → 0.5)
                num = float(current_equation)
                self.equation_var.set(self.__format_number(str(num / 100)))

            self.is_result = True

        except ValueError:
            self.equation_var.set("Erro"); self.is_result = True
    
    def __scientific(self, value: float) -> None:
        """Converte um número para notação científica com uma formatação legível.

        Args:
            value (float): O número a ser convertido.
        """
        scien_value = f'{value:.2e}'; mantissa, exponent = scien_value.split('e')
        self.equation_var.set(f'{mantissa.replace('.', ',')}×10^{int(exponent)}')

    def __update_display(self, val: str) -> None:
        """Adiciona dígitos ao mostrador ou reseta se for o resultado final.

        Args:
            val (str): O caractere do botão pressionado.
        """
        current_equation = self.__unformat_number(self.equation_var.get())

        if self.is_result:
            if val in ['+', '-', '×', '÷', '^']:
                self.is_result = False
            else:
                current_equation = '0'
                self.is_result = False

        if len(self.__unformat_number(self.equation_var.get())) >= self.max_digits: return

        # Regex para separar a expressão em números e operadores
        parts = re.split(r"([+\-×÷^()])", current_equation)
        parts = [p for p in parts if p]; last_part = parts[-1] if parts else ''

        if val == '.':
            # Permite ponto apenas se o último número não tiver um
            if '.' not in last_part:
                current_equation += val
        elif current_equation == '0' and val != '.':
            current_equation = val
        else:
            current_equation += val

        # Reformata a expressão, formatando cada parte que não seja um operador ou símbolo
        new_parts = re.split(r"([+\-×÷^()π])", current_equation)
        new_parts = [p for p in new_parts if p] # Remove strings vazias

        for i, part in enumerate(new_parts):
            # Se a parte não for um operador ou símbolo e não estiver vazia, formata como número
            if part and part not in ['+', '-', '×', '÷', '^', '(', ')', 'π']:
                new_parts[i] = self.__format_number(part)

        self.equation_var.set(''.join(new_parts))
