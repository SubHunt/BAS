import tkinter as tk


def button_clicked():
    text = entry.get()
    label.config(text=f"Hello world{text}")


root = tk.Tk()
root.title("Первая программа с интерфейсом.")
root.geometry("300x200")

label = tk.Label(root, )
label.pack(pady=20)

entry = tk.Entry(root)
entry.pack(pady=30)

button = tk.Button(root, text="Нажми", command=button_clicked)
button.pack(pady=10)


root.mainloop()
