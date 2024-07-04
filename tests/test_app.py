from http import HTTPStatus


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


def test_read_users(client):
    response = client.get('/users/')

    assert response.status_code == HTTPStatus.OK

    assert response.json() == {
        'users': [
            {'id': 1, 'username': 'testusername', 'email': 'test@test.com'}
        ]
    }


def test_read_user(client):
    response = client.get('/users/1')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': 1,
        'username': 'testusername',
        'email': 'test@test.com',
    }


def test_read_user_not_found(client):
    response = client.get('/users/2')

    assert response.status_code == HTTPStatus.NOT_FOUND

    assert response.json() == {'detail': 'User not found'}


def test_update_user(client):
    response = client.put(
        '/users/1',
        json={
            'id': 1,
            'username': 'testusername2',
            'email': 'test2@test.com',
            'password': 'secret2',
        },
    )

    assert response.status_code == HTTPStatus.OK

    assert response.json() == {
        'id': 1,
        'username': 'testusername2',
        'email': 'test2@test.com',
    }


def test_update_user_not_found(client):
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


def test_delete_user(client):
    response = client.delete('/users/1')

    assert response.json() == {'message': 'User deleted'}


def test_delete_user_not_found(client):
    response = client.delete('/users/2')

    assert response.status_code == HTTPStatus.NOT_FOUND

    assert response.json() == {'detail': 'User not found'}
