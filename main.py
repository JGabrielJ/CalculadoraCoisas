import tkinter as tk
from thing.calculator import Calculator


if __name__ == '__main__':
    window = tk.Tk()
    calc = Calculator(window)
    window.mainloop()
