from src.utils import  requires_role
import pytest
from http import HTTPStatus


def test_requires_role_success(mocker):
    #given
    mock_user = mocker.Mock()
    mock_user.role.name = 'Admin'
    mocker.patch('src.utils.get_jwt_identity')
    mocker.patch('src.utils.db.get_or_404', return_value=mock_user)
    decorated_fuction = requires_role('Admin')(lambda: 'Success')

    #when
    result = decorated_fuction()

    #then
    assert result == 'Success'

def test_requires_role_fail(mocker):
    #given
    mock_user = mocker.Mock()
    mock_user.role.name = 'normal'

    mocker.patch('src.utils.get_jwt_identity')
    mocker.patch('src.utils.db.get_or_404', return_value=mock_user)

    decorated_fuction = requires_role('Admin')(lambda: 'Success')

    #when 
    result = decorated_fuction()

    #then
    assert result == ({"message": "user do not have acess"}, HTTPStatus.FORBIDDEN)

   