import tkinter as tk
from tkinter import ttk, messagebox
import json
import os


def main():
    root = tk.Tk()
    root.title("Список пользователей")
    root.geometry("500x500")

    main_frame = ttk.Frame(root, padding="20")
    main_frame.pack(fill=tk.BOTH, expand=True)

    label = ttk.Label(main_frame, text="Введите имя пользователя:")
    label.pack(pady=5)

    entry = ttk.Entry(main_frame)
    entry.pack(pady=5)
    entry.bind('<Return>', lambda event: add_user(entry, listbox))

    listbox = tk.Listbox(main_frame, height=8, selectmode=tk.SINGLE)
    listbox.pack(pady=10, fill=tk.BOTH, expand=True)

    scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=listbox.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    listbox.config(yscrollcommand=scrollbar.set)

    button_frame = ttk.Frame(main_frame)
    button_frame.pack(pady=10)

    add_button = ttk.Button(
        button_frame,
        text="Добавить пользователя",
        command=lambda: add_user(entry, listbox)
    )
    add_button.pack(side=tk.LEFT, padx=5)

    delete_button = ttk.Button(
        button_frame,
        text="Удалить выбранного",
        command=lambda: delete_user(listbox)
    )
    delete_button.pack(side=tk.LEFT, padx=5)

    clear_button = ttk.Button(
        button_frame,
        text="Очистить список",
        command=lambda: clear_users(listbox)
    )
    clear_button.pack(side=tk.LEFT, padx=5)

    context_menu = tk.Menu(root, tearoff=0)
    context_menu.add_command(label="Копировать", command=lambda: copy_user(listbox))
    context_menu.add_command(label="Удалить", command=lambda: delete_user(listbox))

    listbox.bind("<Button-3>", lambda event: show_context_menu(event, context_menu, listbox))
    listbox.bind("<Double-Button-1>", lambda event: edit_user_dialog(listbox, root))

    count_label = ttk.Label(main_frame, text="Всего пользователей: 0")
    count_label.pack(pady=5)

    load_users(listbox, count_label)

    root.mainloop()


def update_count(listbox, count_label):
    count = listbox.size()
    count_label.config(text=f"Всего пользователей: {count}")


def add_user(entry, listbox):
    name = entry.get()
    if name.strip() == "":
        messagebox.showwarning("Ошибка", "Введите имя!")
        return
    listbox.insert(tk.END, name)
    entry.delete(0, tk.END)
    save_users(listbox)
    update_count(listbox, count_label)


def delete_user(listbox):
    selected = listbox.curselection()
    if not selected:
        messagebox.showwarning("Ошибка", "Выберите пользователя для удаления!")
        return
    result = messagebox.askyesno("Подтверждение", f"Удалить пользователя '{listbox.get(selected[0])}'?")
    if result:
        listbox.delete(selected[0])
        save_users(listbox)
        update_count(listbox, count_label)


def clear_users(listbox):
    if listbox.size() == 0:
        return
    result = messagebox.askyesno("Подтверждение", "Очистить весь список пользователей?")
    if result:
        listbox.delete(0, tk.END)
        save_users(listbox)
        update_count(listbox, count_label)


def edit_user_dialog(listbox, parent):
    selected = listbox.curselection()
    if not selected:
        return

    old_name = listbox.get(selected[0])

    dialog = tk.Toplevel(parent)
    dialog.title("Редактировать пользователя")
    dialog.geometry("300x150")
    dialog.resizable(False, False)
    dialog.transient(parent)
    dialog.grab_set()

    ttk.Label(dialog, text="Введите новое имя:").pack(pady=10)
    entry = ttk.Entry(dialog, width=30)
    entry.insert(0, old_name)
    entry.pack(pady=5)
    entry.focus()
    entry.bind('<Return>', lambda event: save_edit())

    def save_edit():
        new_name = entry.get()
        if new_name.strip() == "":
            messagebox.showwarning("Ошибка", "Имя не может быть пустым!")
            return
        listbox.delete(selected[0])
        listbox.insert(selected[0], new_name)
        save_users(listbox)
        update_count(listbox, count_label)
        dialog.destroy()

    ttk.Button(dialog, text="Сохранить", command=save_edit).pack(pady=10)


def copy_user(listbox):
    selected = listbox.curselection()
    if selected:
        name = listbox.get(selected[0])
        root.clipboard_clear()
        root.clipboard_append(name)
        messagebox.showinfo("Информация", f"'{name}' скопирован в буфер обмена")


def show_context_menu(event, menu, listbox):
    index = listbox.nearest(event.y)
    listbox.selection_clear(0, tk.END)
    listbox.selection_set(index)
    menu.post(event.x_root, event.y_root)


def save_users(listbox):
    users = listbox.get(0, tk.END)
    with open('users.json', 'w', encoding='utf-8') as f:
        json.dump(list(users), f, ensure_ascii=False, indent=2)


def load_users(listbox, count_label):
    if os.path.exists('users.json'):
        try:
            with open('users.json', 'r', encoding='utf-8') as f:
                users = json.load(f)
                for user in users:
                    listbox.insert(tk.END, user)
                update_count(listbox, count_label)
        except:
            messagebox.showerror("Ошибка", "Не удалось загрузить данные")


if __name__ == "__main__":
    main()