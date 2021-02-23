import argparse
import logging

import requests


class StarLine(object):
    slnet_token = None
    slid_token = None
    user_id = None
    data_ways = None

    def slnet_init(self, slid_token):
        self.slid_token = slid_token
        self.slnet_token = self.get_slnet_token()
        self.user_id = self.get_user_id()

    def get_slnet_token(self):
        """
        Авторизация пользователя по токену StarLineID. Токен авторизации предварительно необходимо получить на сервере StarLineID.
        :param slid_token: Токен StarLineID
        :return: Токен пользователя на StarLineAPI
        """
        url = 'https://developer.starline.ru/json/v2/auth.slid'
        logging.info('execute request: {}'.format(url))
        data = {
            'slid_token': self.slid_token
        }
        r = requests.post(url, json=data)
        response = r.json()
        logging.info('response info: {}'.format(r))
        logging.info('response data: {}'.format(response))
        slnet_token = r.cookies["slnet"]
        logging.info('slnet token: {}'.format(slnet_token))
        return slnet_token

    def get_user_id(self):
        """
        Возвращает user_id. Не злоупотребляйте методом /auth.slid, так как сервер может потребовать каптчу при частых
        обращениях. Желательно user_id кэшировать.
        :param slid_token: Токен StarLineID
        :return: Токен пользователя на StarLineAPI
        """
        url = 'https://developer.starline.ru/json/v2/auth.slid'
        logging.info('execute request: {}'.format(url))
        data = {
            'slid_token': self.slid_token
        }
        r = requests.post(url, json=data)
        response = r.json()
        logging.info('response info: {}'.format(r))
        logging.info('response data: {}'.format(response))
        user_id = response["user_id"]
        logging.info('user_id: {}'.format(user_id))
        return user_id

    def get_user_info(self, user_id):
        """
        Получение списка устройств принадлежиших пользователю или устройств, доступ к которым предоставлен пользователю
         другими пользователями. Ответ содержит полное состояние устройств.
        :param user_id: user identifier
        :param slnet_token: StarLineAPI Token
        :return: Код, необходимый для получения токена приложения
        """
        url = "https://developer.starline.ru/json/v2/user/{}/user_info".format(user_id)
        logging.info('execute request: {}'.format(url))
        cookies = "slnet={}".format(self.slnet_token)

        r = requests.get(url, headers={"Cookie": "slnet=" + self.slnet_token})
        response = r.json()
        logging.info('cookies: {}'.format(cookies))
        logging.info('response info: {}'.format(response))
        return response

    def get_ways(self, devise_id: int, begin_track, end_trak) -> dict:
        '''
        :param self: 
        :param devise_id: идентификатор устройства
        :param slnet_token: куки авторизации
        :param begin_track: unix-время начала запрашиваемого трека
        :param end_trak: unix-время конца запрашиваемого трека
        :return: возвращаем масив точек
        '''

        url = "https://developer.starline.ru/json/v1/device/{}/ways".format(devise_id)
        logging.info('execute request: {}'.format(url))
        cookies = "slnet={}".format(self.slnet_token)
        data = {"begin": begin_track, "end": end_trak}

        r = requests.post(url, headers={"Cookie": "slnet=" + self.slnet_token}, json=data)
        response = r.json()
        r.close()
        # logging.info('payload : {}'.format(payload))
        logging.info('response info: {}'.format(r))
        logging.info('response data: {}'.format(response))
        self.data_ways = response
        return response


if __name__ == "__main__":
    pass
