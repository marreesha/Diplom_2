import pytest
from src import ApiClient, ApiUser, URLS, ApiOrder, get_ingredients, generate_email, generate_password, generate_name


@pytest.fixture
def api_user():
    client = ApiClient(URLS.BASE_URL)
    return ApiUser(client)


@pytest.fixture
def user_data():
    return {'email': generate_email(), 'password': generate_password(), 'name': generate_name()}


@pytest.fixture
def create_new_user(api_user, user_data):
    data = user_data

    response = api_user.create_user(data=data)
    token = response.json().get('accessToken', '')
    yield token

    headers = {'Authorization': token}
    api_user.delete_user(headers=headers)


@pytest.fixture
def api_order():
    client = ApiClient(URLS.BASE_URL)
    return ApiOrder(client)


@pytest.fixture
def create_new_order(api_order):
    def _wrapper(token):
        ingredients = {'ingredients': get_ingredients()}
        headers = {'Authorization': token}
        response = api_order.create_order(data=ingredients, headers=headers)

        return response.json().get('order', {}).get('number', '')

    return _wrapper
