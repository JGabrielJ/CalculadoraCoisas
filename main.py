import tkinter as tk
from thing.calculator import Calculator


if __name__ == '__main__':
    wind = tk.Tk()
    calc = Calculator(wind)
    wind.mainloop()
