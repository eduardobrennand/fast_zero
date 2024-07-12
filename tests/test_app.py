from http import HTTPStatus

from fast_zero.schemas import UserPublic


def test_read_root_deve_retornar_ok_e_ola_mundo(client):
    response = client.get('/')  # Act (ação)

    assert response.status_code == HTTPStatus.OK  # Assert (garantir)
    assert response.json() == {'message': 'Olá Mundo!'}


def test_create_user(client):
    response = client.post(  # UserSchema
        '/users/',
        json={
            'username': 'testusername',
            'email': 'test@test.com',
            'password': 'secret',
        },
    )

    # Validando se retornou status code 201 (CREATED)
    assert response.status_code == HTTPStatus.CREATED

    # Validando se retornou o schema do UserPublic
    assert response.json() == {
        'id': 1,
        'username': 'testusername',
        'email': 'test@test.com',
    }


def test_create_user_already_registered(client, user):
    response = client.post(
        '/users/',
        json={
            'username': 'testuser',
            'email': 'user@test.com',
            'password': 'secretpassword',
        },
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Username already exists.'}


def test_create_email_already_registered(client, user):
    response = client.post(
        '/users/',
        json={
            'username': 'testuser2',
            'email': 'user@test.com',
            'password': 'secretpassword',
        },
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'E-mail already exists.'}


def test_read_users(client):
    response = client.get('/users/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': []}


def test_read_users_with_users(client, user):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get('/users/')
    assert response.json() == {'users': [user_schema]}


def test_read_user(client, user):
    response = client.get('/users/1')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': 1,
        'username': 'testuser',
        'email': 'user@test.com',
    }


def test_read_user_not_found(client, user):
    response = client.get('/users/2')

    assert response.status_code == HTTPStatus.NOT_FOUND

    assert response.json() == {'detail': 'User not found'}


def test_update_user(client, user, token):
    response = client.put(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'updatedusername',
            'email': 'updatedemail@test.com',
            'password': 'updatedsecretpassword',
        },
    )

    assert response.status_code == HTTPStatus.OK

    assert response.json() == {
        'id': user.id,
        'username': 'updatedusername',
        'email': 'updatedemail@test.com',
    }


def test_update_user_not_found(client, user):
    response = client.put(
        '/users/2',
        json={
            'id': 2,
            'username': 'testusername3',
            'email': 'test3@test.com',
            'password': 'secret3',
        },
    )

    assert response.status_code == HTTPStatus.NOT_FOUND

    assert response.json() == {'detail': 'User not found'}


def test_delete_user(client, user, token):
    response = client.delete(
        f'/users/{user.id}', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.json() == {'message': 'User deleted'}


def test_delete_user_not_found(client, user):
    response = client.delete('/users/2')

    assert response.status_code == HTTPStatus.NOT_FOUND

    assert response.json() == {'detail': 'User not found'}


def test_get_token(client, user):
    response = client.post(
        '/token',
        data={'username': user.email, 'password': user.clean_password},
    )
    token = response.json()

    assert response.status_code == HTTPStatus.OK
    assert token['token_type'] == 'Bearer'
    assert 'access_token' in token
