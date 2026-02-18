# main.py

import tkinter as tk
from tkinter import ttk

def main():
    # Создаем главное окно
    root = tk.Tk()
    root.title("Пример проекта на Python с Tkinter")
    root.geometry("400x300")

    # Создаем основной фрейм
    main_frame = ttk.Frame(root, padding="20")
    main_frame.pack(fill=tk.BOTH, expand=True)

    # Создаем метку
    label = ttk.Label(main_frame, text="Это пример интерфейса")
    label.pack(pady=10)

    # Создаем кнопку
    button = ttk.Button(main_frame, text="Нажми меня", command=lambda: on_button_click(label))
    button.pack(pady=10)

    # Запускаем главный цикл
    root.mainloop()

def on_button_click(label):
    label.config(text="Кнопка нажата!")

if __name__ == "__main__":
    main()