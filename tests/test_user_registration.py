import allure
import pytest
from src import generate_password, generate_email, generate_name, constants
from conftest import api_user, create_new_user, user_data


@allure.feature('Регистрация пользователя')
class TestUserRegistration:

    @allure.story('Создание уникального пользователя')
    def test_create_user_success(self, api_user):
        data = {'email': generate_email(), 'password': generate_password(), 'name': generate_name()}

        # Запрос на создание нового клиента
        response = api_user.create_user(data=data)

        with allure.step('Данные теста'):
            allure.attach(str(response.status_code), name='status_code')
            allure.attach(str(response.json()), name='text')

        assert response.status_code == constants.OK
        assert response.json()['success'] is True
        assert 'accessToken' in response.json()

        # Удаление пользователя
        headers = {'Authorization': response.json().get('accessToken', '')}
        api_user.delete_user(headers=headers)

    @allure.story('Регистрация уже существующего пользователя')
    def test_create_existing_user(self, user_data, api_user, create_new_user):
        # Запрос на повторное создание клиента
        response = api_user.create_user(data=user_data)

        with allure.step('Данные теста'):
            allure.attach(str(response.status_code), name='status_code')
            allure.attach(str(response.json()), name='text')

        assert response.status_code == constants.FORBIDDEN
        assert response.json()['success'] is False
        assert response.json()['message'] == 'User already exists'

    @allure.story('Регистрация без обязательного поля')
    @allure.title('Тест для поля: {missing_field}')
    @pytest.mark.parametrize('missing_field', ['email', 'password', 'name'])
    def test_create_user_missing_field(self, user_data, api_user, missing_field):
        # Удаляем одно из обязательных полей
        user_data.pop(missing_field)

        # Запрос на создание нового клиента
        response = api_user.create_user(data=user_data)

        with allure.step('Данные теста'):
            allure.attach(str(response.status_code), name='status_code')
            allure.attach(str(response.json()), name='text')

        assert response.status_code == constants.FORBIDDEN
        assert response.json()['success'] is False
        assert response.json()['message'] == 'Email, password and name are required fields'
