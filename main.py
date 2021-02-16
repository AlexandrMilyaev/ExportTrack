# This is a sample Python script.
# noinspection PyUnresolvedReferences
import os.path

print(os.path)
import auth as slnet
import get_user_id
import get_user_info
import starlineapi as sl
import PySimpleGUI as gui
import tkinter as tk

from get_app_code import get_app_code
from get_app_token import get_app_token
from get_slid_user_token import get_slid_user_token
from get_slnet_token import get_slnet_token


# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
def gui_init_window():
    layout = [
        [gui.Text('Введите данные для авторизации:')],
        [gui.Text('Login:', size=(15, 1)), gui.InputText('Введите логин')],
        [gui.Text('Password:', size=(15, 1)), gui.InputText('Введите пароль')],
        [gui.Text('AppId:', size=(15, 1)), gui.InputText('Введите номер приложения')],
        [gui.Text('Secret:', size=(15, 1)), gui.InputText('Введите пароль приложения')],
        [gui.Submit(), gui.Cancel()]
    ]
    window = gui.Window('SLNetExportTrack', layout)
    return window


def gui_get_data(window):
    pass


def main():
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

    window = gui_init_window()

    while True:
        event, values = window.read()
        if event == gui.WIN_CLOSED or event == 'Cancel':
            print(event, values)
            break


# Press the green button in the gutter to run the script.
# if __name__ == '__main__':
main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
