import allure
from src import HttpMethods, URLS


class ApiOrder:

    def __init__(self, api_client):
        self.client = api_client

    @allure.step('Запрос на создание нового заказа')
    def create_order(self, data, **kwargs):
        return self.client.send_request(HttpMethods.POST, URLS.ORDER_ENDPOINT, json=data, **kwargs)

    @allure.step('Запрос на получение заказов пользователя')
    def get_user_order(self, **kwargs):
        return self.client.send_request(HttpMethods.GET, URLS.ORDER_ENDPOINT, **kwargs)
