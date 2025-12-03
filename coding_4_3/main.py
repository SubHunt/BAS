import tkinter as tk

root = tk.Tk()
root.title("UAS Control Module")
root.geometry("600x400")
root.configure(bg="#2b2b2b")


def check_systems():
    system_ok = True
    # Исправленная логика проверки
    log_listbox.insert(tk.END, f"Проверка батареи: {battery_cells}")
    for voltage in battery_cells:
        if voltage < 4.0:
            log_listbox.insert(tk.END, f"Low voltage: {voltage}")
            system_ok = False
            break
        else:
            log_listbox.insert(tk.END, "Cell OK")
    if system_ok:
        log_listbox.insert(tk.END, "Статус: ГОТОВ К АРМИНГУ")
        log_listbox.itemconfig(tk.END, fg="green")
    else:
        log_listbox.insert(tk.END, "Статус: ОШИБКА БАТАРЕИ")
        log_listbox.itemconfig(tk.END, fg="red")


# Фреймы
control_frame = tk.Frame(root, bg="#3c3c3c", width=240)  # 40% от 600px
# Исправлено: control_frame занимает 40% ширины слева
control_frame.pack(side="left", fill="both", expand=False, padx=(0, 5))
control_frame.pack_propagate(False)  # Предотвращает изменение размера фрейма
log_frame = tk.Frame(root, bg="#2b2b2b", width=360)  # 60% от 600px
# Исправлено: log_frame занимает 60% ширины справа
log_frame.pack(side="right", fill="both", expand=True, padx=(5, 0))
log_frame.pack_propagate(False)  # Предотвращает изменение размера фрейма

# Установка весов для колонок, чтобы сохранялись пропорции при расширении
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=2)  # control_frame - 40%
root.grid_columnconfigure(1, weight=3)  # log_frame - 60%
# Элементы управления
status_label = tk.Label(control_frame, text="Статус: DISARMED", font=("Arial", 14), fg="white",
                        bg="#3c3c3c")
# Исправлено: Добавлены отступы и выравнивание по центру
status_label.pack(pady=10, padx=10, anchor="center")
# Кнопка проверки
btn_check = tk.Button(
    control_frame, text="1. Проверка систем", bg="#505050", fg="white")
btn_check.pack(pady=5, fill="x")  # Исправлено: Кнопки выстроены вертикально
# Кнопка Арминга
btn_arm = tk.Button(control_frame, text="2. ARM", bg="red", fg="white")
btn_arm.pack(pady=5, fill="x")  # Исправлено: Кнопки выстроены вертикально
# Добавляем Listbox и Scrollbar в log_frame
log_listbox = tk.Listbox(log_frame, bg="#2b2b2b", fg="white")
log_scrollbar = tk.Scrollbar(
    log_frame, orient="vertical", command=log_listbox.yview)
log_listbox.config(yscrollcommand=log_scrollbar.set)

# Размещаем Listbox и Scrollbar в log_frame
log_listbox.pack(side="left", fill="both", expand=True)
log_scrollbar.pack(side="right", fill="y")

# Добавляем "рыбу" текста в listbox для демонстрации скролла
# for i in range(1, 51):
#     log_listbox.insert(
#         tk.END, f"Сообщение лога №{i}: Система работает нормально")

battery_cells = [4.15, 4.20, 4.50, 4.18]  # 3.50 - это сбойная ячейка

# Привязываем функцию к кнопке
btn_check.config(command=check_systems)


root.mainloop()
