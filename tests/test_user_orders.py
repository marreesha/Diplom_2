import allure
from src import constants, generate_string
from conftest import create_new_user, api_order, create_new_order


@allure.feature('Получение заказов пользователя')
class TestUserOrders:

    @allure.story('Получение заказов авторизованного пользователя')
    def test_get_user_orders_success(self, create_new_user, api_order, create_new_order):
        access_token = create_new_user

        # Создание заказа
        order_number = create_new_order(access_token)

        headers = {'Authorization': access_token}
        response = api_order.get_user_order(headers=headers)

        with allure.step('Данные теста'):
            allure.attach(str(response.status_code), name='status_code')
            allure.attach(str(response.json()), name='text')

        assert response.status_code == constants.OK
        assert response.json()['success'] is True
        assert response.json()['orders'][0]['number'] == order_number


    @allure.story('Получение заказов неавторизованного пользователя')
    def test_get_user_orders_wo_authorization(self, api_order):
        headers = {'Authorization': generate_string()}
        response = api_order.get_user_order(headers=headers)

        with allure.step('Данные теста'):
            allure.attach(str(response.status_code), name='status_code')
            allure.attach(str(response.json()), name='text')

        assert response.status_code == constants.UNAUTHORIZED
        assert response.json()['success'] is False
        assert response.json()['message'] == 'You should be authorised'
