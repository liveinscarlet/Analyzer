import tkinter as tk
from tkinter import ttk
import pyvisa
import tkinter_math as tkm
from analyzer import Pna

# Создание объектов класса
rm = pyvisa.ResourceManager()
PNA = Pna(rm, 'TCPIP0::169.254.25.7::inst0::INSTR')

# Дефолтные настройки
root = tk.Tk()                                  # Создаем корневой объект
root.title("PNA-X control panel")               # Название кода
root.geometry("800x500")                        # Размер окна

# Кнопошки
btn_reset = ttk.Button(text='Reset', command=Pna.Reset(PNA))    #Кнопошка для ресета
btn_reset.pack()

root.mainloop()

