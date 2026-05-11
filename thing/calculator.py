import math
import re
import tkinter as tk
from typing import Any
from tkinter import ttk
from thing.utils import format_number, unformat_number


class Calculator(ttk.Frame):
    def __init__(self, parent: tk.Widget, controller: Any) -> None:
        """Inicializa o frame da calculadora principal.

        Args:
            parent (tk.Widget): O container da classe App.
            controller (App): A instância principal da aplicação.
        """
        super().__init__(parent)

        # Configuração do Grid
        for c in range(5):
            self.grid_columnconfigure(c, weight=1)
        for r in range(8):
            self.grid_rowconfigure(r, weight=1)

        # Variáveis de Estado
        self.max_digits: int = 19
        self.is_result: bool = False
        self.equation_var = tk.StringVar(value="0")

        # Título do Frame (Calculadora)
        ttk.Label(
            self, text="Calculadora de Coisas", style="TTL.TLabel", anchor="center"
        ).grid(row=0, column=0, columnspan=5, sticky="nsew", pady=15)

        # Display das Equações e Resultados
        ttk.Label(
            self,
            textvariable=self.equation_var,
            anchor="e",
            style="NUM.TLabel",
            background="#C3EBEB",
        ).grid(row=1, column=0, columnspan=5, sticky="nsew", padx=8, pady=(0, 15))

        # Lista de Botões da Calculadora
        buttons: list[tuple] = [
            ("C", 2, 0),
            ("sin", 2, 1),
            ("cos", 2, 2),
            ("tan", 2, 3),
            ("⌫", 2, 4),
            ("π", 3, 0),
            ("(", 3, 1),
            (")", 3, 2),
            ("%", 3, 3),
            ("÷", 3, 4),
            ("sqrt", 4, 0),
            ("7", 4, 1),
            ("8", 4, 2),
            ("9", 4, 3),
            ("×", 4, 4),
            ("^", 5, 0),
            ("4", 5, 1),
            ("5", 5, 2),
            ("6", 5, 3),
            ("-", 5, 4),
            ("scien", 6, 0),
            ("1", 6, 1),
            ("2", 6, 2),
            ("3", 6, 3),
            ("+", 6, 4),
            ("fact", 7, 0),
            ("abs", 7, 1),
            ("0", 7, 2),
            (",", 7, 3),
            ("=", 7, 4),
        ]

        for text, row, column in buttons:
            ttk.Button(
                self,
                text=text,
                style="CDC.TButton",
                command=lambda t=text: self.__button_click(t),
            ).grid(row=row, column=column, pady=5, padx=5, sticky="nsew")

    def __button_click(self, value: str) -> None:
        """Define as ações de cada botão da calculadora.

        Args:
            value (str): O valor do botão pressionado.
        """
        if value == ",":
            value = "."

        if value == "=":
            self.__calculate()
        elif value == "C":
            self.__clear()
        elif value == "⌫":
            self.__delete()
        elif value == "%":
            self.__handle_percentage()
        elif value in ["sin", "cos", "tan", "sqrt", "fact", "abs", "scien"]:
            self.__apply_immediate_function(value)
        else:
            self.__update_display(value)

    def __clear(self) -> None:
        """Reseta a calculadora para o estado inicial."""
        self.equation_var.set("0")
        self.is_result = False

    def __delete(self) -> None:
        """Remove o último caractere da equação."""
        current = unformat_number(self.equation_var.get())

        # Se for um resultado ou um único dígito, limpa a tela
        if self.is_result or len(current) == 1:
            self.equation_var.set("0")
        else:
            self.__reformat_display(current[:-1])

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
            expression = unformat_number(self.equation_var.get()).replace(
                "π", "math.pi"
            )
            safe_env = {"math": math, "__builtins__": {}}
            current_value = eval(expression, safe_env)

            # Executa a função selecionada pelo usuário
            match func:
                case "sin":
                    result = math.sin(math.radians(current_value))
                case "cos":
                    result = math.cos(math.radians(current_value))
                case "tan":
                    if current_value % 180 == 90:
                        raise ValueError("Tangente indefinida!!!")
                    result = math.tan(math.radians(current_value))
                case "sqrt":
                    result = math.sqrt(current_value)
                case "fact":
                    result = math.factorial(int(current_value))
                case "abs":
                    result = abs(current_value)
                case "scien":
                    self.__scientific(current_value)
                    self.is_result = True
                    return

            # Mostra o resultado no visor, arredondado para 10 casas decimais
            self.equation_var.set(format_number(str(round(result, 10))))
            self.is_result = True

        except (ValueError, TypeError, SyntaxError):
            # Em caso de erro matemático ou de sintaxe, exibe uma mensagem de erro no visor
            self.equation_var.set("Erro")
            self.is_result = True

    def __calculate(self) -> None:
        """Avalia a expressão final quando `=` é pressionado."""

        try:
            expression = unformat_number(self.equation_var.get())

            # Remove operadores finais consecutivos para resolver expressões como "1+2+"
            expression = re.sub(r"[+\-×÷^]+$", "", expression)

            # Substitui os símbolos visuais por operadores/funções do Python
            expression = expression.replace("×", "*")
            expression = expression.replace("÷", "/")
            expression = expression.replace("^", "**")
            expression = expression.replace("π", "math.pi")

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
            if result == int(result):
                result = int(result)
            self.equation_var.set(format_number(str(result)))
            self.is_result = True

        except (SyntaxError, NameError, ZeroDivisionError, ValueError, TypeError):
            self.equation_var.set("Erro")
            self.is_result = True

    def __handle_percentage(self) -> None:
        """Lida com cálculos de porcentagem:
        - Se o formato for `número`, calcula `número / 100`;
        - Se o formato for `{base}{op}{perc}`, calcula o resultado contextual.
        """
        current_equation = unformat_number(self.equation_var.get())

        # Regex para encontrar um padrão como `100+10` no final da string
        match = re.search(r"(\d+\.?\d*)([+\-×÷])(\d+\.?\d*)$", current_equation)

        try:
            if match:
                # Cálculo contextual (ex.: 100 + 10%)
                base_num, operator, perc_num = match.groups()
                base_num, perc_num = float(base_num), float(perc_num)
                increment = base_num * (perc_num / 100)
                result: float = 0

                match operator:
                    case "+":
                        result = base_num + increment
                    case "-":
                        result = base_num - increment
                    case "×":
                        result = base_num * increment
                    case "÷":
                        result = base_num / increment

                self.equation_var.set(format_number(str(result)))
            else:
                # Conversão simples (ex.: 50% → 0.5)
                num = float(current_equation)
                self.equation_var.set(format_number(str(num / 100)))

            self.is_result = True

        except ValueError:
            self.equation_var.set("Erro")
            self.is_result = True

    def __scientific(self, value: float) -> None:
        """Converte um número para notação científica com uma formatação legível.

        Args:
            value (float): O número a ser convertido.
        """
        scien_value = f"{value:.2e}"
        mantissa, exponent = scien_value.split("e")
        self.equation_var.set(f"{mantissa.replace('.', ',')}×10^{int(exponent)}")

    def __reformat_display(self, equation: str) -> None:
        """Divide a equação em números e operadores, formata os números
        individualmente e junta tudo de volta para exibir no visor.

        Args:
            equation (str): A equação não formatada.
        """
        # Divide a expressão em partes e remove strings vazias
        parts = re.split(r"([+\-×÷^()π])", equation)
        parts = [p for p in parts if p]

        for i, part in enumerate(parts):
            # Se a parte for um número, ela é formatada
            if part and part not in ["+", "-", "×", "÷", "^", "(", ")", "π"]:
                parts[i] = format_number(part)

        self.equation_var.set("".join(parts))

    def __update_display(self, val: str) -> None:
        """Adiciona dígitos ao mostrador ou reseta se for o resultado final.

        Args:
            val (str): O caractere do botão pressionado.
        """
        current_equation = unformat_number(self.equation_var.get())

        if self.is_result:
            if val in ["+", "-", "×", "÷", "^"]:
                self.is_result = False
            else:
                current_equation = "0"
                self.is_result = False

        if len(current_equation) >= self.max_digits:
            return

        # Regex para separar a expressão em números e operadores
        parts = re.split(r"([+\-×÷^()])", current_equation)
        parts = [p for p in parts if p]
        last_part = parts[-1] if parts else ""

        if val == ".":
            # Permite ponto apenas se o último número não tiver um
            if "." not in last_part:
                current_equation += val
        elif current_equation == "0" and val != ".":
            current_equation = val
        else:
            current_equation += val

        # Re-formata a equação inteira para exibição
        self.__reformat_display(current_equation)
