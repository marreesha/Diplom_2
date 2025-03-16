import allure
from src import HttpMethods, URLS


class ApiUser:

    def __init__(self, api_client):
        self.client = api_client

    @allure.step('Запрос на создание нового пользователя')
    def create_user(self, data, **kwargs):
        return self.client.send_request(HttpMethods.POST, URLS.REGISTRATION_ENDPOINT, json=data, **kwargs)

    @allure.step('Запрос на удаление пользователя')
    def delete_user(self, **kwargs):
        return self.client.send_request(HttpMethods.DELETE, URLS.DELETE_ENDPOINT, **kwargs)

    @allure.step('Запрос на логин пользователя')
    def login_user(self, data, **kwargs):
        return self.client.send_request(HttpMethods.POST, URLS.LOGIN_ENDPOINT, json=data, **kwargs)

    @allure.step('Запрос на обновление данных пользователя')
    def update_userdata(self, data, **kwargs):
        return self.client.send_request(HttpMethods.PATCH, URLS.USER_ENDPOINT, json=data, **kwargs)
