import allure
from src import generate_password, constants
from conftest import api_user, create_new_user, user_data


@allure.feature('Авторизация пользователя')
class TestUserLogin:

    @allure.story('Авторизация существующего пользователя')
    def test_login_user_success(self, user_data, api_user, create_new_user):
        # Авторизация
        response = api_user.login_user(user_data)

        with allure.step('Данные теста'):
            allure.attach(str(response.status_code), name='status_code')
            allure.attach(str(response.json()), name='text')

        assert response.status_code == constants.OK
        assert response.json()['success'] is True

    @allure.story('Авторизация с неверным логином и паролем')
    def test_login_user_incorrect_data(self, user_data, api_user):
        # Авторизация
        response = api_user.login_user(user_data)

        with allure.step('Данные теста'):
            allure.attach(str(response.status_code), name='status_code')
            allure.attach(str(response.json()), name='text')

        assert response.status_code == constants.UNAUTHORIZED
        assert response.json()['success'] is False
        assert response.json()['message'] == 'email or password are incorrect'

    @allure.story('Авторизация с неверным паролем')
    def test_login_user_incorrect_password(self, user_data, api_user, create_new_user):
        # Изменение данных пользователя
        user_data['password'] = generate_password()

        # Авторизация
        response = api_user.login_user(user_data)

        with allure.step('Данные теста'):
            allure.attach(str(response.status_code), name='status_code')
            allure.attach(str(response.json()), name='text')

        assert response.status_code == constants.UNAUTHORIZED
        assert response.json()['success'] is False
        assert response.json()['message'] == 'email or password are incorrect'
