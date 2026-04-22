import threading
import tkinter as tk
from tkinter import messagebox
import FlowReader
import time
import MakePredictByNN
is_running = False
monitoring_is_started = False

def stop_program():
    global is_running
    is_running = False
    root.destroy()

def RealTimeThread():
    global is_running
    is_running = True
    app = FlowReader.Reader()
    while(is_running):
        data, isNull = app.readRealTime()
        if (not isNull):
            MakePredictByNN.makePred(data, True)
        time.sleep(5)

def FileThread():
    global is_running
    is_running = True
    app = FlowReader.Reader()
    while(is_running):
        data, isNull = app.readRawData()
        if (not isNull):
            MakePredictByNN.makePred(data, False)
        time.sleep(5)

# Создание основного окна
root = tk.Tk()
root.title("Нейросеть для мониторинга")

# Надпись с названием программы
title_label = tk.Label(root, text="Нажмите для начала мониторинга", font=("Helvetica", 16))
title_label.pack(pady=20)

# Функция для вывода сообщения о нажатии кнопки
def RealTimeMonitoring():
    global monitoring_is_started
    if(not monitoring_is_started):
        monitoring_is_started = True
        messagebox.showinfo("Поехали", "Программа начала работу!")
        my_thread = threading.Thread(target=RealTimeThread)
        my_thread.start()
    else:
        messagebox.showinfo("Ошибка", "Мониторинг уже запущен!")

def FromFileMonitoring():
    global monitoring_is_started
    if(not monitoring_is_started):
        monitoring_is_started = True
        messagebox.showinfo("Поехали", "Программа начала работу!")
        my_thread = threading.Thread(target=FileThread)
        my_thread.start()
    else:
        messagebox.showinfo("Ошибка", "Мониторинг уже запущен!")

# Кнопки
button1 = tk.Button(root, text="Начать мониторинг сети", command=RealTimeMonitoring)
button1.pack(pady=10)

button2 = tk.Button(root, text="Мониторинг файла", command=FromFileMonitoring)
button2.pack(pady=10)

stop_button = tk.Button(root, text="Остановить программу", command=stop_program)
stop_button.pack(pady=10)

# Запуск главного цикла обработки событий
root.mainloop()

