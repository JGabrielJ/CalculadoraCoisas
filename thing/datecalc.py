import tkinter as tk
from typing import Any


class DateCalc(tk.Frame):
    def __init__(self, parent: tk.Widget, controller: Any) -> None:
        """Inicializa o frame da calculadora de datas.

        Args:
            parent (tk.Widget): O container da classe App.
            controller (App): A instância principal da aplicação.
        """
        super().__init__(parent, bg='#FFFFFF')
