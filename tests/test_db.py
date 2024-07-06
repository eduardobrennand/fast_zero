from sqlalchemy import select

from fast_zero.models import User


def test_create_user(session):
    user = User(
        username='test', email='test@email.com', password='secretpassword'
    )

    session.add(user)  # adiciona o usuario na sessao
    session.commit()  # junta todas as operações da sessão e persiste dentro do bd
    # session.refresh(user)  # sincroniza o obj User() com o obj em bd (adiciona id)
    # scalar = trazer infos do bd em fmt obj python
    result = session.scalar(select(User).where(User.email == 'test@email.com'))

    assert result.id == 1
