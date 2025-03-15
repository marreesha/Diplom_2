import pytest
import allure
from src import get_ingredients, generate_string, constants
from conftest import create_new_user, api_order


@allure.feature('Создание заказа')
class TestOrderCreation:

    @allure.story('Создание заказа с авторизацией и корректными ингредиентами')
    @allure.title('Тест для числа ингредиентов: {ingredient_quantity}')
    @pytest.mark.parametrize('ingredient_quantity', (1, 3, 6, 10))
    def test_create_order_success(self, create_new_user, api_order, ingredient_quantity):
        access_token = create_new_user

        ingredients = {'ingredients': get_ingredients(ingredient_quantity)}
        headers = {'Authorization': access_token}
        # Создание заказа
        response = api_order.create_order(data=ingredients, headers=headers)

        with allure.step('Данные теста'):
            allure.attach(str(response.status_code), name='status_code')
            allure.attach(str(response.json()), name='text')

        assert response.status_code == constants.OK
        assert response.json()['success'] is True

    @allure.story('Создание заказа без авторизации')
    def test_create_order_wo_authorization(self, api_order):
        ingredients = {'ingredients': get_ingredients()}
        headers = {'Authorization': ''}
        # Создание заказа
        response = api_order.create_order(data=ingredients, headers=headers)

        with allure.step('Данные теста'):
            allure.attach(str(response.status_code), name='status_code')
            allure.attach(str(response.json()), name='text')

        assert response.status_code == constants.OK
        assert response.json()['success'] is True

    @allure.story('Создание заказа без ингредиентов')
    def test_create_order_wo_ingredients(self, api_order, create_new_user):
        access_token = create_new_user

        ingredients = {'ingredients': []}
        headers = {'Authorization': access_token}
        # Создание заказа
        response = api_order.create_order(data=ingredients, headers=headers)

        with allure.step('Данные теста'):
            allure.attach(str(response.status_code), name='status_code')
            allure.attach(str(response.json()), name='text')

        assert response.status_code == constants.BAD_REQUEST
        assert response.json()['success'] is False
        assert response.json()['message'] == 'Ingredient ids must be provided'

    @allure.story('Создание заказа с неверным хешем ингредиента')
    def test_create_order_with_invalid_ingredient(self, create_new_user, api_order):
        access_token = create_new_user

        ingredients = {'ingredients': [generate_string()]}
        headers = {'Authorization': access_token}
        # Создание заказа
        response = api_order.create_order(data=ingredients, headers=headers)

        with allure.step('Данные теста'):
            allure.attach(str(response.status_code), name='status_code')

        assert response.status_code == constants.INTERNAL_SERVER_ERROR
