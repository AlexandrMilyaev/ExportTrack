# This is a sample Python script.
# noinspection PyUnresolvedReferences

import starlineapi as sl
from starlineapi import StarLine as SL
import PySimpleGUI as sg
import time as tm
import json
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
        [sg.InputCombo(auto, size=(29, 1), key='-List auto-', default_value='-select-')],
        [sg.Input(key='-start date-', size=(29, 1)), sg.CalendarButton('Дата от', size=(10, 1))],
        [sg.Input(key='-end date-', size=(29, 1)), sg.CalendarButton('Дата до', size=(10, 1))],
        [sg.Input(key='-user folders-', size=(29, 1)), sg.FolderBrowse(target='-user folders-', size=(10, 1))],
        [sg.Button('Export', size=(10, 1)), sg.Cancel(size=(10, 1)), sg.Button('Login', button_color=('black', 'red'), key='login', size=(10, 1))]
    ]
    window = sg.Window('SLNetExportTrack', layout)
    return window


def gui_error_window(code, data):
    layout = [
        [sg.Text('Error: {}'.format(str(code)))],
        [sg.Text(str(data))],
        [sg.Ok()]
    ]

    window = sg.Window('Oops...', layout)
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
    slnet = SL()
    auto = list()
    window = gui_object_window(auto)

    while True:
        tm.sleep(0.1)
        event, values = window.read()

        if event == 'login':
            window_login = gui_login_window()
            event_login, values_login = window_login.read()
            if event_login == 'login ok':
                auto.clear()
                slnet.slnet_init(values_login['-Slid-'])
                user_info = slnet.get_user_info(slnet.user_id)
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
            try:
                begin = time_to_unix(values['-start date-'])
                end = time_to_unix(values['-end date-'])
                device_id = int(values['-List auto-'])
                data = slnet.get_ways(device_id, begin, end)
                print(data)
                if data['code'] == 200:
                    print(str(values['-user folders-'])+'exportfile.wln')
                    if values['-user folders-']:
                        filename = '{}/track{}_{}_{}.wln'.format(values['-user folders-'],
                                                                 values['-List auto-'],
                                                                 values['-start date-'],
                                                                 values['-end date-'])
                    else:
                        filename = 'track{}_{}_{}.wln'.format(values['-List auto-'],
                                                              values['-start date-'],
                                                              values['-end date-'])
                    with open(filename, 'w') as f:
                        for key in iter(slnet.data_ways['way']):
                            if key['type'] == 'TRACK':
                                for point in iter(key['nodes']):
                                    f.write('REG;{};{};{};{};0;ALT:0.0,,;,,SATS:{},,,sat:{},;;;;\n'
                                            .format(str(point['t']), str(point['y']), str(point['x']), str(point['s']),
                                                    str(point['sat_qty']), str(point['sat_qty'])))
                else:
                    window_error = gui_error_window(data['code'], data['codestring'])
                    error_event, error_values = window_error.read()
                    if error_event == 'Ok' or error_event == sg.WIN_CLOSED:
                        window_error.close()

                data.clear()
            except Exception as e:
                if 'time data' in str(e.args):
                    window_error = gui_error_window('Нет даты', 'Выбирите дату')
                    error_event, error_values = window_error.read()
                    if error_event == 'Ok' or error_event == sg.WIN_CLOSED:
                        window_error.close()
                elif 'invalid literal' in str(e.args):
                    window_error = gui_error_window('Не выбран автомобиль',
                                                    'Выбирите автомобиль из всплывающего списка, по которому требуеться експортировать маршрут')
                    error_event, error_values = window_error.read()
                    if error_event == 'Ok' or error_event == sg.WIN_CLOSED:
                        window_error.close()
                else:
                    window_error = gui_error_window('Что то пошло не так!',
                                                    str(e.args))
                    error_event, error_values = window_error.read()
                    if error_event == 'Ok' or error_event == sg.WIN_CLOSED:
                        window_error.close()

        elif event == sg.WIN_CLOSED or event == 'Cancel':
            print(event, values)
            window.close()
            break
        # Обработка окна авторизации


# Press the green button in the gutter to run the script.
# if __name__ == '__main__':
main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
