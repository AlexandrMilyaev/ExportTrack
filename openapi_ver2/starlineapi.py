import argparse
import logging

import requests


def get_slnet_token(slid_token):
    """
    Авторизация пользователя по токену StarLineID. Токен авторизации предварительно необходимо получить на сервере StarLineID.
    :param slid_token: Токен StarLineID
    :return: Токен пользователя на StarLineAPI
    """
    url = 'https://developer.starline.ru/json/v2/auth.slid'
    logging.info('execute request: {}'.format(url))
    data = {
        'slid_token': slid_token
    }
    r = requests.post(url, json=data)
    response = r.json()
    logging.info('response info: {}'.format(r))
    logging.info('response data: {}'.format(response))
    slnet_token = r.cookies["slnet"]
    logging.info('slnet token: {}'.format(slnet_token))
    return slnet_token


def get_user_id(slid_token):
    """
    Возвращает user_id. Не злоупотребляйте методом /auth.slid, так как сервер может потребовать каптчу при частых
    обращениях. Желательно user_id кэшировать.
    :param slid_token: Токен StarLineID
    :return: Токен пользователя на StarLineAPI
    """
    url = 'https://developer.starline.ru/json/v2/auth.slid'
    logging.info('execute request: {}'.format(url))
    data = {
        'slid_token': slid_token
    }
    r = requests.post(url, json=data)
    response = r.json()
    logging.info('response info: {}'.format(r))
    logging.info('response data: {}'.format(response))
    user_id = response["user_id"]
    logging.info('user_id: {}'.format(user_id))
    return user_id


def get_user_info(user_id, slnet_token):
    """
    Получение списка устройств принадлежиших пользователю или устройств, доступ к которым предоставлен пользователю
     другими пользователями. Ответ содержит полное состояние устройств.
    :param user_id: user identifier
    :param slnet_token: StarLineAPI Token
    :return: Код, необходимый для получения токена приложения
    """
    url = "https://developer.starline.ru/json/v2/user/{}/user_info".format(user_id)
    logging.info('execute request: {}'.format(url))
    cookies = "slnet={}".format(slnet_token)

    r = requests.get(url, headers={"Cookie": "slnet=" + slnet_token})
    response = r.json()
    logging.info('cookies: {}'.format(cookies))
    logging.info('response info: {}'.format(response))
    return response


def get_ways(devise_id, slnet_token, begin_track, end_trak) -> list:
    '''
    :param devise_id: идентификатор устройства
    :param slnet_token: куки авторизации
    :param begin_track: unix-время начала запрашиваемого трека
    :param end_trak: unix-время конца запрашиваемого трека
    :return: возвращаем масив точек
    '''

    url = "https://developer.starline.ru/json/v1/device/{}/ways".format(devise_id)
    logging.info('execute request: {}'.format(url))
    cookies = "slnet={}".format(slnet_token)
    data = {}
    data["begin"] = begin_track
    data["end"] = end_trak

    r = requests.post(url, headers={"Cookie": "slnet=" + slnet_token}, json=data)
    response = r.json()
    r.close()
    #logging.info('payload : {}'.format(payload))
    logging.info('response info: {}'.format(r))
    logging.info('response data: {}'.format(response))

    return response


def get_args():
    parser = argparse.ArgumentParser()
    # для получения userId можно воспользоваться скриптом get_user_id.py
    parser.add_argument("-u", "--userId", dest="userId", help="user identifier", default="", required=True)
    parser.add_argument("-s", "--slnetToken", dest="slnetToken", help="StarLineAPI Token", default="", required=True)
    args = parser.parse_args()
    logging.info('userId {}, slnetToken: {}'.format(args.userId, args.slnetToken))
    return args


if __name__ == "__main__":
    pass
