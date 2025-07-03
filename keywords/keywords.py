import datetime
import os
import shutil
import pyautogui
import time
from pywinauto import Desktop

def press_keys(key1,key2):
    pyautogui.hotkey(key1, key2)

def switch_to_fj_frigo():
    """Tenta encontrar uma janela cujo título contenha 'FJ Frigo' e traz o foco para ela."""
    while True:
        windows = Desktop(backend="uia").windows()
        for win in windows:
            if "atualização" in win.window_text():
                win.set_focus()
                time.sleep(0.5)
                pyautogui.press("right")
                pyautogui.press("enter")
                continue
            if (
                "FJFrigo" in win.window_text()
                and "atualização" not in win.window_text()
            ):
                win.set_focus()
                return True
        break
    return False

def generate_filename_with_date(filename):
    datatime_now_formated = datetime.datetime.now().strftime('%Y%m%d_%H%M')
    return f'{filename}_{datatime_now_formated}'

def move(source,destination):
    if not os.path.exists(os.path.dirname(source)):
        print(f'File {source} does not exist.')
        return False
    print(f'Moving file from {source} to {destination}')
    shutil.move(source,destination)
    return True