import tkinter as tk
from typing import Any
from tkinter import ttk
from tkcalendar import Calendar
from datetime import datetime, date


class DateSelector(ttk.Frame):
    def __init__(self, parent: tk.Widget, controller: Any, **kwargs):
        """Frame personalizado para selecionar datas.

        Args:
            parent (tk.Widget): O container da classe App.
            controller (App): A instância principal da aplicação.
        """
        frame_style = kwargs.pop("style", None)
        super().__init__(parent, style=frame_style)

        # Armazena o controller para o Toplevel pai
        self.controller = controller

        # Variável para guardar a data
        self.data_var = tk.StringVar()

        # Configura a grade para o layout interno
        self.grid_columnconfigure(0, weight=1)

        # Extrai kwargs específicos para o campo de texto e para o widget Calendar
        entry_width = kwargs.pop("width", 12)
        self._date_pattern: str = kwargs.pop("date_pattern", "dd/mm/yyyy")
        self.calendar_kwargs = kwargs

        self.entry = ttk.Entry(self, textvariable=self.data_var, width=entry_width)
        self.entry.grid(row=0, column=0, sticky="ew", padx=(0, 5))
        self.entry.bind("<Button-1>", self.show_calendar)

        # Botão para abrir o calendário de seleção
        btn_cal = ttk.Button(
            self, text="▼", style="CDC.TButton", command=self.show_calendar
        )
        btn_cal.grid(row=0, column=1, sticky="e")
        self._app_toplevel = self.controller

    def get_date(self) -> date | None:
        """Retorna a data selecionada como um objeto `datetime.date`."""
        date_str = self.data_var.get()

        if date_str:
            try:
                # Converte o padrão de data do widget para o formato utilizado pelo `datetime`
                py_date_pattern = (
                    self._date_pattern.replace("dd", "%d")
                    .replace("mm", "%m")
                    .replace("yyyy", "%Y")
                )
                return datetime.strptime(date_str, py_date_pattern).date()
            except ValueError:
                return None

        return None

    def show_calendar(self, event=None) -> None:
        """Cria uma janela Toplevel, transiente para a janela principal do app.

        Args:
            event (tk.Event): O evento de clique do mouse.
        """
        top = tk.Toplevel(self._app_toplevel)
        top.title("Selecione uma Data:     ")
        top.transient(self._app_toplevel)

        # Centraliza a janela de seleção logo abaixo do campo de entrada
        x = self.entry.winfo_rootx()
        y = self.entry.winfo_rooty() + self.entry.winfo_height()
        top.geometry(f"+{x}+{y}")

        # Obtém o valor da data selecionada
        current_date = self.get_date()

        cal_kwargs = self.calendar_kwargs.copy()
        cal_kwargs["selectmode"] = "day"
        cal_kwargs["date_pattern"] = self._date_pattern

        if current_date:
            cal_kwargs["day"] = current_date.day
            cal_kwargs["month"] = current_date.month
            cal_kwargs["year"] = current_date.year

        cal = Calendar(top, **cal_kwargs)
        cal.pack(padx=10, pady=10)

        def set_date() -> None:
            """Define a data selecionada no campo e fecha a janela."""
            self.data_var.set(cal.get_date())
            top.destroy()

        btn_ok = ttk.Button(
            top, text="Confirmar", style="CDC.TButton", command=set_date
        )
        btn_ok.pack(pady=5)

        top.grab_set()
        top.focus_force()
        self._app_toplevel.wait_window(top)
