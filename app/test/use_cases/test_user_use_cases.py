import pytest
from passlib.context import CryptContext
from app.schemas.user import User
from fastapi.exceptions import HTTPException
from app.db.models import User as UserModel
from app.use_cases.user import UserUseCases

cryptContext = CryptContext(schemes=['sha256_crypt'])

def test_register_user(db_session):
    user = User(
        username='David',
        password='pass#'
    )

    uc = UserUseCases(db_session)
    uc.register_user(user=user)

    user_on_db = db_session.query(UserModel).first()

    assert user_on_db is not None
    assert user_on_db.username == user.username
    assert cryptContext.verify(user.password, user_on_db.password)

    db_session.delete(user_on_db)
    db_session.commit()

def test_register_user_username_already_exists(db_session):
    user_on_db = UserModel(
        username='David',
        password=cryptContext.hash('pass#')
    )

    db_session.add(user_on_db)
    db_session.commit()

    uc = UserUseCases(db_session)

    user = User(
        username='David',
        password=cryptContext.hash('pass#')
    )

    with pytest.raises(HTTPException):
        uc.register_user(user=user)

    db_session.delete(user_on_db)
    db_session.commit()