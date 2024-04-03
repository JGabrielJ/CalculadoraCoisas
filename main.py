import tkinter as tk
from math import pi, sin, cos, tan, sqrt, pow, factorial


def change_number():
    display.insert(0, '0')


# Instanciando a janela
calc = tk.Tk()

# Configurando a janela
calc.title('Calculadora de Coisas')
calc.iconbitmap('./files/icon.ico')
calc.config(background='#FFFFFF')

# Adicionando título e visor
title = tk.Label(calc, text='Calculadora', font=('Bahnschrift', 18), background='#FFFFFF')
title.grid(row=0, column=0, columnspan=5, pady=8)

display = tk.Entry(calc, cursor='xterm', width=21, font=('System', 36), justify='right', background='#C3EBEB')
display.grid(row=1, column=0, columnspan=5, padx=8)

# Adicionando os botões
clear = tk.Button(calc, text='C', width=7, height=2, font=('Terminal', 12),
                  relief='raised', borderwidth=3, command=change_number)
clear.grid(row=2, column=0, padx=5, pady=5)

seno = tk.Button(calc, text='sin()', width=7, height=2, font=('Terminal', 12),
                 relief='raised', borderwidth=3, command=change_number)
seno.grid(row=2, column=1, padx=5, pady=5)

coss = tk.Button(calc, text='cos()', width=7, height=2, font=('Terminal', 12),
                 relief='raised', borderwidth=3, command=change_number)
coss.grid(row=2, column=2, padx=5, pady=5)

tang = tk.Button(calc, text='tan()', width=7, height=2, font=('Terminal', 12),
                 relief='raised', borderwidth=3, command=change_number)
tang.grid(row=2, column=3, padx=5, pady=5)

porc = tk.Button(calc, text='%', width=7, height=2, font=('Terminal', 12),
                 relief='raised', borderwidth=3, command=change_number)
porc.grid(row=2, column=4, padx=5, pady=5)

square = tk.Button(calc, text='√', width=7, height=2, font=('Terminal', 12),
                   relief='raised', borderwidth=3, command=change_number)
square.grid(row=3, column=0, padx=5, pady=5)

open_par = tk.Button(calc, text='(', width=7, height=2, font=('Terminal', 12),
                     relief='raised', borderwidth=3, command=change_number)
open_par.grid(row=3, column=1, padx=5, pady=5)

close_par = tk.Button(calc, text=')', width=7, height=2, font=('Terminal', 12),
                      relief='raised', borderwidth=3, command=change_number)
close_par.grid(row=3, column=2, padx=5, pady=5)

pi_num = tk.Button(calc, text='π', width=7, height=2, font=('Terminal', 12),
                   relief='raised', borderwidth=3, command=change_number)
pi_num.grid(row=3, column=3, padx=5, pady=5)

divide = tk.Button(calc, text='/', width=7, height=2, font=('Terminal', 12),
                   relief='raised', borderwidth=3, command=change_number)
divide.grid(row=3, column=4, padx=5, pady=5)

power = tk.Button(calc, text='^', width=7, height=2, font=('Terminal', 12),
                  relief='raised', borderwidth=3, command=change_number)
power.grid(row=4, column=0, padx=5, pady=5)

seven = tk.Button(calc, text='7', width=7, height=2, font=('Terminal', 12),
                  relief='raised', borderwidth=3, command=change_number)
seven.grid(row=4, column=1, padx=5, pady=5)

eight = tk.Button(calc, text='8', width=7, height=2, font=('Terminal', 12),
                  relief='raised', borderwidth=3, command=change_number)
eight.grid(row=4, column=2, padx=5, pady=5)

nine = tk.Button(calc, text='9', width=7, height=2, font=('Terminal', 12),
                 relief='raised', borderwidth=3, command=change_number)
nine.grid(row=4, column=3, padx=5, pady=5)

times = tk.Button(calc, text='*', width=7, height=2, font=('Terminal', 12),
                  relief='raised', borderwidth=3, command=change_number)
times.grid(row=4, column=4, padx=5, pady=5)

ten_power = tk.Button(calc, text='10ⁿ', width=7, height=2, font=('Terminal', 12),
                      relief='raised', borderwidth=3, command=change_number)
ten_power.grid(row=5, column=0, padx=5, pady=5)

four = tk.Button(calc, text='4', width=7, height=2, font=('Terminal', 12),
                 relief='raised', borderwidth=3, command=change_number)
four.grid(row=5, column=1, padx=5, pady=5)

five = tk.Button(calc, text='5', width=7, height=2, font=('Terminal', 12),
                 relief='raised', borderwidth=3, command=change_number)
five.grid(row=5, column=2, padx=5, pady=5)

six = tk.Button(calc, text='6', width=7, height=2, font=('Terminal', 12),
                relief='raised', borderwidth=3, command=change_number)
six.grid(row=5, column=3, padx=5, pady=5)

minus = tk.Button(calc, text='-', width=7, height=2, font=('Terminal', 12),
                  relief='raised', borderwidth=3, command=change_number)
minus.grid(row=5, column=4, padx=5, pady=5)

fact = tk.Button(calc, text='n!', width=7, height=2, font=('Terminal', 12),
                 relief='raised', borderwidth=3, command=change_number)
fact.grid(row=6, column=0, padx=5, pady=5)

one = tk.Button(calc, text='1', width=7, height=2, font=('Terminal', 12),
                relief='raised', borderwidth=3, command=change_number)
one.grid(row=6, column=1, padx=5, pady=5)

two = tk.Button(calc, text='2', width=7, height=2, font=('Terminal', 12),
                relief='raised', borderwidth=3, command=change_number)
two.grid(row=6, column=2, padx=5, pady=5)

three = tk.Button(calc, text='3', width=7, height=2, font=('Terminal', 12),
                  relief='raised', borderwidth=3, command=change_number)
three.grid(row=6, column=3, padx=5, pady=5)

plus = tk.Button(calc, text='+', width=7, height=2, font=('Terminal', 12),
                 relief='raised', borderwidth=3, command=change_number)
plus.grid(row=6, column=4, padx=5, pady=5)

termial = tk.Button(calc, text='n?', width=7, height=2, font=('Terminal', 12),
                    relief='raised', borderwidth=3, command=change_number)
termial.grid(row=7, column=0, padx=5, pady=5)

module = tk.Button(calc, text='|x|', width=7, height=2, font=('Terminal', 12),
                   relief='raised', borderwidth=3, command=change_number)
module.grid(row=7, column=1, padx=5, pady=5)

zero = tk.Button(calc, text='0', width=7, height=2, font=('Terminal', 12),
                 relief='raised', borderwidth=3, command=change_number)
zero.grid(row=7, column=2, padx=5, pady=5)

dot = tk.Button(calc, text='.', width=7, height=2, font=('Terminal', 12),
                relief='raised', borderwidth=3, command=change_number)
dot.grid(row=7, column=3, padx=5, pady=5)

equal = tk.Button(calc, text='=', width=7, height=2, font=('Terminal', 12),
                  relief='raised', borderwidth=3, command=change_number)
equal.grid(row=7, column=4, padx=5, pady=5)

# Mantendo a janela aberta
calc.mainloop()
