import argparse
import logging
import hashlib
import requests


class StarLine(object):
    slnet_token = None
    slid_token = None
    user_id = None

    def __init__(self, app_id, app_secret):
        self.app_id = app_id
        self.app_secret = app_secret

    def auth(self, login, password):
        app_code = self.get_app_code()
        app_token = self.get_app_token(app_code)
        self.slid_token = self.get_slid_user_token(app_token, login, password)
        self.slnet_token = self.get_slnet_token()
        self.user_id = self.get_user_id()

    def get_app_code(self):
        """
        Получение кода приложения для дальнейшего получения токена.
        Идентификатор приложения и пароль выдаются контактным лицом СтарЛайн.
        Срок годности кода приложения 1 час.
        :param app_id: Идентификатор приложения
        :param app_secret: Пароль приложения
        :return: Код, необходимый для получения токена приложения
        """
        url = 'https://id.starline.ru/apiV3/application/getCode/'
        logging.info('execute request: {}'.format(url))

        payload = {
            'appId': self.app_id,
            'secret': hashlib.md5(self.app_secret.encode('utf-8')).hexdigest()
        }
        r = requests.get(url, params=payload)
        response = r.json()
        logging.info('payload : {}'.format(payload))
        logging.info('response info: {}'.format(r))
        logging.info('response data: {}'.format(response))
        if int(response['state']) == 1:
            app_code = response['desc']['code']
            logging.info('Application code: {}'.format(app_code))
            return app_code
        raise Exception(response)

    def get_app_token(self, app_code):
        """
        Получение токена приложения для дальнейшей авторизации.
        Время жизни токена приложения - 4 часа.
        Идентификатор приложения и пароль можно получить на my.starline.ru.
        :param app_id: Идентификатор приложения
        :param app_secret: Пароль приложения
        :param app_code: Код приложения
        :return: Токен приложения
        """
        url = 'https://id.starline.ru/apiV3/application/getToken/'
        logging.info('execute request: {}'.format(url))
        payload = {
            'appId': self.app_id,
            'secret': hashlib.md5((self.app_secret + app_code).encode('utf-8')).hexdigest()
        }
        r = requests.get(url, params=payload)
        response = r.json()
        logging.info('payload: {}'.format(payload))
        logging.info('response info: {}'.format(r))
        logging.info('response data: {}'.format(response))
        if int(response['state']) == 1:
            app_token = response['desc']['token']
            logging.info('Application token: {}'.format(app_token))
            return app_token
        raise Exception(response)

    def get_slid_user_token(self, app_token, user_login, user_password):
        """
         Аутентификация пользователя по логину и паролю.
         Неверные данные авторизации или слишком частое выполнение запроса авторизации с одного
         ip-адреса может привести к запросу капчи.
         Для того, чтобы сервер SLID корректно обрабатывал клиентский IP,
         необходимо проксировать его в параметре user_ip.
         В противном случае все запросы авторизации будут фиксироваться для IP-адреса сервера приложения, что приведет к частому требованию капчи.
        :param sid_url: URL StarLineID сервера
        :param app_token: Токен приложения
        :param user_login: Логин пользователя
        :param user_password: Пароль пользователя
        :return: Токен, необходимый для работы с данными пользователя. Данный токен потребуется для авторизации на StarLine API сервере.
        """
        url = 'https://id.starline.ru/apiV3/user/login/'
        logging.info('execute request: {}'.format(url))
        payload = {
            'token': app_token
        }
        data = {"login": user_login, "pass": hashlib.sha1(user_password.encode('utf-8')).hexdigest()}
        r = requests.post(url, params=payload, data=data)
        response = r.json()
        logging.info('payload : {}'.format(payload))
        logging.info('response info: {}'.format(r))
        logging.info('response data: {}'.format(response))
        if int(response['state']) == 1:
            slid_token = response['desc']['user_token']
            logging.info('SLID token: {}'.format(slid_token))
            return slid_token
        raise Exception(response)

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

    def get_user_info(self):
        """
        Получение списка устройств принадлежиших пользователю или устройств, доступ к которым предоставлен пользователю
         другими пользователями. Ответ содержит полное состояние устройств.
        :param user_id: user identifier
        :param slnet_token: StarLineAPI Token
        :return: Код, необходимый для получения токена приложения
        """
        url = "https://developer.starline.ru/json/v2/user/{}/user_info".format(self.user_id)
        logging.info('execute request: {}'.format(url))
        cookies = "slnet={}".format(self.slnet_token)

        r = requests.get(url, headers={"Cookie": "slnet=" + self.slnet_token})
        response = r.json()
        logging.info('cookies: {}'.format(cookies))
        logging.info('response info: {}'.format(response))
        return response

    def get_ways(self, devise_id: int, begin_track: int, end_track: int) -> dict:
        '''
        :param self: 
        :param devise_id: идентификатор устройства
        :param begin_track: unix-время начала запрашиваемого трека
        :param end_track: unix-время конца запрашиваемого трека
        :return: возвращаем масив точек
        '''

        url = "https://developer.starline.ru/json/v1/device/{}/ways".format(devise_id)
        logging.info('execute request: {}'.format(url))
        cookies = "slnet={}".format(self.slnet_token)
        data = {"begin": begin_track, "end": end_track}

        r = requests.post(url, headers={"Cookie": cookies}, json=data)
        response = r.json()
        r.close()
        # logging.info('payload : {}'.format(payload))
        logging.info('response info: {}'.format(r))
        logging.info('response data: {}'.format(response))
        return response


if __name__ == "__main__":
    pass
