import tkinter as tk
from tkinter import messagebox
import time


class DroneApp:

    def __init__(self, root):
        self.root = root
        self.root.title("Cистема проверки")
        self.root.geometry("400x500")
        self.root.configure(bg="#2b2b2b")
        # Константы
        self.is_system_checked = False  # Пройдена ли предполётная проверка
        self.is_armed = False  # Запущены ли двигатели (Arm)
        self.current_altitude = 0  # Текущая высота
        # Данные с датчиков (имитация): одна ячейка просела ниже 3.5V!
        self.battery_cells = [4.2, 4.2, 4.0, 4.2]
        # Интерфейс
        # Статусная панель
        self.status_var = tk.StringVar(value="СТАТУС: ОЖИДАНИЕ")
        self.lbl_status = tk.Label(root, textvariable=self.status_var,
                                   font=("Consolas", 14, "bold"), bg="#2b2b2b", fg="white")
        self.lbl_status.pack(pady=20)
        # Лог событий
        self.log_list = tk.Listbox(
            root, height=10, width=40, bg="#3c3c3c", fg="white")
        self.log_list.pack(pady=10)
        # Кнопки
        # Проверка систем
        self.btn_check = tk.Button(root, text="1. ПРОВЕРКА СИСТЕМ", width=30,
                                   command=self.check_systems, bg="#505050", fg="white")
        self.btn_check.pack(pady=5)
        # Арминг
        self.btn_arm = tk.Button(root, text="2. ARM", width=30,
                                 command=self.arm_vehicle, bg="red", fg="white")
        self.btn_arm.pack(pady=5)
        # Взлет
        self.btn_takeoff = tk.Button(root, text="3. TAKEOFF", width=30,
                                     command=self.takeoff_vehicle, bg="#505050", fg="white")
        self.btn_takeoff.pack(pady=5)
        # ЗАДАНИЕ 4
        self.btn_land = tk.Button(root, text="4. LAND", width=30, command=self.land_vehicle,
                                  bg="#505050", fg="white")
        self.btn_land.pack(pady=20)
    # Логика

    def log(self, message):
        # Добавляет сообщение в список событий
        self.log_list.insert(tk.END, f">> {message}")
        self.log_list.yview(tk.END)

    def check_systems(self):
        # Прверка заряда батареи
        self.log("Начало проверки батареи...")
        # ЗАДАНИЕ 1
        check_result = True
        for voltage in self.battery_cells:
            if voltage < 3.5:
                check_result = False
                self.log(f"ОШИБКА: Ячейка {voltage}V разряжена!")
                break
            # Здесь не хватает команды, которая прервет проверку или пометит сбой
            else:
                self.log(f"Ячейка {voltage}V - Норма")
        # Финализация
        if check_result == True:
            self.is_system_checked = True
            self.status_var.set("СТАТУС: ГОТОВ")
            self.log("Система исправна.")
        else:
            self.is_system_checked = False
            self.status_var.set("СТАТУС: ОШИБКА ПИТАНИЯ")

    def arm_vehicle(self):
        # Запуск двигателе
        # ЗАДАНИЕ 2
        # (Напишите здесь код if/return)
        if self.is_system_checked == False:
            self.log("Ошибка. Сначала выполните проверку")
            return
        self.is_armed = True
        self.status_var.set("СТАТУС: ARMED")
        self.btn_arm.config(bg="green")  # Визуальная индикация
        self.log("Двигатели запущены!")

    def takeoff_vehicle(self):
        # Взлет
        # ЗАДАНИЕ
        # Добавьте проверку: если self.is_armed равно False, запретить взлет.
        # (Напишите здесь код проверки)
        if self.is_armed == False:
            self.log("Ошибка. Дрон не запущен")
            return
        self.current_altitude = 50
        self.status_var.set(f"СТАТУС: ПОЛЕТ (Высота {self.current_altitude}м)")
        self.log("Выполняется автоматический взлет...")

    def land_vehicle(self):
        # Посадка
        if self.current_altitude > 0:
            self.log("Начало снижения...")
            self.current_altitude = 0
            self.is_armed = False
            self.status_var.set("СТАТУС: DISARMED")
            self.btn_arm.config(bg="red")
            self.log("Посадка завершена.")
        else:
            self.log("Дрон уже на земле.")


# Запуск приложения
if __name__ == "__main__":
    root = tk.Tk()
    app = DroneApp(root)
    root.mainloop()
