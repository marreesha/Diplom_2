import pytest
import allure
from src import generate_password, generate_email, generate_name, constants
from conftest import api_user, create_new_user

FIELD_AND_VALUE = [
    ('name', generate_name()),
    ('email', generate_email()),
    ('password', generate_password())
]


@allure.feature('Изменение данных пользователя')
class TestUserUpdate:

    @allure.story('Изменение данных с авторизацией')
    @allure.title('Тест для поля: {field}')
    @pytest.mark.parametrize('field, new_value', FIELD_AND_VALUE)
    def test_update_user_success(self, api_user, create_new_user, field, new_value):
        access_token = create_new_user

        headers = {'Authorization': access_token}
        update_payload = {field: new_value}
        # Запрос на обновление данных
        response = api_user.update_userdata(data=update_payload, headers=headers)

        with allure.step('Данные теста'):
            allure.attach(str(response.status_code), name='status_code')
            allure.attach(str(response.json()), name='text')

        assert response.status_code == constants.OK
        assert response.json()['success'] is True

    @allure.story('Изменение данных без авторизации')
    @allure.title('Тест для поля: {field}')
    @pytest.mark.parametrize('field, new_value', FIELD_AND_VALUE)
    def test_update_user_wo_authorization(self, api_user, field, new_value):
        headers = {'Authorization': ''}
        update_payload = {field: new_value}
        # Запрос на обновление данных
        response = api_user.update_userdata(data=update_payload, headers=headers)

        with allure.step('Данные теста'):
            allure.attach(str(response.status_code), name='status_code')
            allure.attach(str(response.json()), name='text')

        assert response.status_code == constants.UNAUTHORIZED
        assert response.json()['success'] is False
        assert response.json()['message'] == 'You should be authorised'
