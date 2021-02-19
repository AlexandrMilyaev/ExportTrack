# This is a sample Python script.
# noinspection PyUnresolvedReferences

import starlineapi as sl
import PySimpleGUI as sg
import time as tm
import datetime as dt


# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
def gui_login_window() -> object:
    layout = [
        [sg.Text('Введите данные для авторизации:')],
        [sg.Text('Login:', size=(15, 1)), sg.InputText('Введите логин', key='-Login-')],
        [sg.Text('Password:', size=(15, 1)), sg.InputText('Введите пароль', key='-Password-')],
        [sg.Text('AppId:', size=(15, 1)), sg.InputText('Введите номер приложения', key='-AppId-')],
        [sg.Text('Secret:', size=(15, 1)), sg.InputText('Введите пароль приложения', key='-Secret-')],
        [sg.Text('Slid:', size=(15, 1)), sg.InputText('ef9d7318df61dba1b824ec36bb220ddc:1045837', key='-Slid-')],
        [sg.Button('login', key='login ok'), sg.Cancel(key='login cansel')]
    ]
    window = sg.Window('SLNetExportTrack', layout)
    return window


def gui_object_window(auto) -> object:
    layout = [
        [sg.Text('Выберете автомобиль с списка:')],
        [sg.Text('Список авто:', size=(15, 1)), sg.InputCombo(auto, size=(15, 1), key='-List auto-')],
        [sg.Input(key='-start date-', size=(20, 1)), sg.CalendarButton('Дата от')],
        [sg.Input(key='-end date-', size=(20, 1)), sg.CalendarButton('Дата до')],
        [sg.Button('Export'), sg.Cancel(), sg.Button('Login', button_color=('black', 'red'), key='login')]
    ]
    window = sg.Window('SLNetExportTrack', layout)
    return window


def time_to_unix(time: str, time_format="%Y-%m-%d %H:%M:%S") -> int:
    '''
    :param time: время в формате строки. Например, '2021-02-18 16:37:58'
    :param time_format: формат времени, котрый принимаем. Например, "%Y-%m-%d %H:%M:%S"
    :return: unix-время
    '''

    data = time
    data = tm.strptime(data, time_format)
    data = tm.mktime(data)
    data = int(data)
    return data


def main():
    '''
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
    '''
    slnet_token = ''
    auto = list()
    window = gui_object_window(auto)

    while True:
        tm.sleep(0.1)
        event, values = window.read()
        if event == 'Next':
            pass
        elif event == 'login':
            window_login = gui_login_window()
            event_login, values_login = window_login.read()
            if event_login == 'login ok':
                auto.clear()
                user = sl.get_user_id(values_login['-Slid-'])
                slnet_token = sl.get_slnet_token(values_login['-Slid-'])
                user_info = sl.get_user_info(user, slnet_token)
                for devices in iter(user_info['devices']):
                    auto.append(devices['imei'])
                for shared_devices in iter(user_info['shared_devices']):
                    auto.append(shared_devices['imei'])
                window['-List auto-'].update(values=auto)
                window['login'].update(button_color=('black', 'green'))
                del event_login, values_login
                window_login.close()
            elif event_login == "login cansel" or event_login == sg.WIN_CLOSED:
                window_login.close()
                del event_login, values_login
        elif event == 'Export':
            begin = time_to_unix(values['-start date-'])
            end = time_to_unix(values['-end date-'])
            device_id = int(values['-List auto-'])
            data = sl.get_ways(devise_id=device_id, slnet_token=slnet_token, begin_track=begin, end_trak=end)
            print(data)
            data.clear()
        elif event == sg.WIN_CLOSED or event == 'Cancel':
            print(event, values)
            window.close()
            break
        # Обработка окна авторизации


# Press the green button in the gutter to run the script.
# if __name__ == '__main__':
main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
