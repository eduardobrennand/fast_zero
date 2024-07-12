import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from fast_zero.app import app
from fast_zero.database import get_session
from fast_zero.models import User, table_registry
from fast_zero.security import get_password_hash


@pytest.fixture()
def client(session):
    def get_session_override():
        return session

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = get_session_override

        yield client

    app.dependency_overrides.clear()


@pytest.fixture()
def session():
    engine = create_engine(
        'sqlite:///:memory:',
        connect_args={'check_same_thread': False},
        poolclass=StaticPool,
    )  # bd em memoria p/ teste
    table_registry.metadata.create_all(engine)  # cria os metadados (tabelas)

    # gerenciamento de contexto
    with Session(engine) as session:
        yield session

    table_registry.metadata.drop_all(engine)  # teardown -> dropar a tabela


@pytest.fixture()
def user(session):
    pwd = 'secretpassword'

    user = User(
        username='testuser',
        password=get_password_hash(pwd),
        email='user@test.com',
    )

    session.add(user)
    session.commit()
    session.refresh(user)

    user.clean_password = pwd  # monkey patch

    return user


@pytest.fixture()
def token(client, user):
    response = client.post(
        '/token',
        data={'username': user.email, 'password': user.clean_password},
    )
    return response.json()['access_token']
