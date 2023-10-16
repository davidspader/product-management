from datetime import datetime
import pytest
from app.schemas.user import User


def test_user_schema():
    user = User(username='David', password='pass#')
    assert user.dict() == {
        'username': 'David',
        'password': 'pass#'
    }

def test_user_schema_invalid_username():
    with pytest.raises(ValueError):
        user = User(username='João#', password='pass#')