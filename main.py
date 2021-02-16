# This is a sample Python script.
# noinspection PyUnresolvedReferences
import os.path
from typing import List, Union

from PySimpleGUI import Text, Button, Input

print(os.path)
import auth as slnet
import get_user_id
import get_user_info
import starlineapi as sl
import PySimpleGUI as gui
import tkinter as tk
import hashlib

from get_app_code import get_app_code
from get_app_token import get_app_token
from get_slid_user_token import get_slid_user_token
from get_slnet_token import get_slnet_token


# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
def gui_login_window() -> object:
    layout = [
        [gui.Text('Введите данные для авторизации:')],
        [gui.Text('Login:', size=(15, 1)), gui.InputText('Введите логин', key='-Login-')],
        [gui.Text('Password:', size=(15, 1)), gui.InputText('Введите пароль', key='-Password-')],
        [gui.Text('AppId:', size=(15, 1)), gui.InputText('Введите номер приложения', key='-AppId-')],
        [gui.Text('Secret:', size=(15, 1)), gui.InputText('Введите пароль приложения', key='-Secret-')],
        [gui.Text('Slid:', size=(15, 1)), gui.InputText('ef9d7318df61dba1b824ec36bb220ddc:1045837', key='-Slid-')],
        [gui.Button('Next'), gui.Cancel()]
    ]
    window = gui.Window('SLNetExportTrack', layout, size=(600, 300))
    return window


def gui_object_window(auto) -> object:
    layout = [
        [gui.Text('Выберете автомобиль с списка:')],
        [gui.Text('Список авто:', size=(15, 1)), gui.InputCombo(auto, key='-List auto-')],
        [gui.CalendarButton('Начало интервала'), gui.Text('Выберете дату')],
        [gui.CalendarButton('Конец интервала '), gui.Text('Выберете дату')],
        [gui.Button('Export'), gui.Cancel()]
    ]
    window = gui.Window('SLNetExportTrack', layout, size=(600, 300))
    return window


def gui_get_data(window):
    pass


def main():
    step = 'login', 'object selection', 'period selection'
    number_step = 0
    auto = list()
    slid_token = "ef9d7318df61dba1b824ec36bb220ddc:1045837"
    user = sl.get_user_id(slid_token)
    slnet_token = sl.get_slnet_token(slid_token)
    user_info = sl.get_user_info(user, slnet_token)
    if user_info.get('codestring') == 'OK':
        for devices in iter(user_info['devices']):
            print(devices)
        for shared_devices in iter(user_info['shared_devices']):
            print(shared_devices)
    else:
        print('data url error')

    window = gui_login_window()

    while True:
        event, values = window.read()
        if event == 'Next':
            try:
                user = sl.get_user_id(values['-Slid-'])
                slnet_token = sl.get_slnet_token(slid_token)
                user_info = sl.get_user_info(user, slnet_token)
                for devices in iter(user_info['devices']):
                    print(devices['alias'])
                    auto.append(devices['imei'])
                for shared_devices in iter(user_info['shared_devices']):
                    print(shared_devices['alias'])
                    auto.append(shared_devices['imei'])

                window.close()
                window = gui_object_window(auto)
            except KeyError:
                print("Нет такого ключа")
        elif event == gui.WIN_CLOSED or event == 'Cancel':
            print(event, values)
            window.close()
            break


# Press the green button in the gutter to run the script.
# if __name__ == '__main__':
main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
