from datetime import datetime, time
import pyautogui
import keyboard

# Частота кликов в секунду
clicks_per_second = 100

# Основные координаты монитора
width, height = pyautogui.size()

def start_click():
        while True:
            pyautogui.tripleClick()
            if keyboard.is_pressed('-'):
                print("Скрипт остановлен по запросу пользователя.")
                break
            if keyboard.is_pressed('x'):
                print("Выход")
                break
def stop_is_clicked():
     while True:
          if keyboard.is_pressed('+'):
                start_click()
          if keyboard.is_pressed('x'):
                print("Выход")
                break
          
stop_is_clicked()
     