import sys
sys.path.insert(0, 'lib')

import endpoints
from endpoints import message_types
import mock
import pytest

import main

def test_bicycle():
    api = main.EchoApi()
    request = main.EchoApi.echo.remote.request_type(content='Hello Merlin!')
    response = api.echo(request)
    assert 'Hello Merlin!' == response.content


def test_get_user_email():
    api = main.BicycleApi()

    with mock.patch('main.endpoints.get_current_user') as user_mock:
        user_mock.return_value = None
        with pytest.raises(endpoints.UnauthorizedException):
            api.get_user_email(message_types.VoidMessage())

        user_mock.return_value = mock.Mock()
        user_mock.return_value.email.return_value = 'user@example.com'
        response = api.get_user_email(message_types.VoidMessage())
        assert 'user@example.com' == response.content
