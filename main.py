import tkinter as tk
from thing.calculator import Calculator


if __name__ == '__main__':
    window = tk.Tk()
    Calculator(window)
    window.mainloop()
