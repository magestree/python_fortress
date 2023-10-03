import os
import uuid

import pytest
import requests_mock

from python_fortress.fortress import Fortress, BASE_URL


@pytest.fixture
def fortress():
    return Fortress()


@pytest.fixture
def credentials():
    return {
        "api_key": "test_api_key",
        "access_token": "test_access_token",
        "master_key": "master_key",
    }


def test_configure(fortress, credentials):
    fortress.configure(**credentials)
    assert fortress.api_key == credentials["api_key"]
    assert fortress.access_token == credentials["access_token"]
    assert fortress.master_key == credentials["master_key"]


def test_build_url(fortress):
    endpoint = "sample-endpoint/"
    url = fortress._build_url(endpoint)
    assert url == f"{BASE_URL}{endpoint}"


def test_headers_without_configure(fortress):
    assert fortress.headers == {"Authorization": "Bearer None"}


def test_headers_with_configure(fortress, credentials):
    fortress.configure(**credentials)
    assert fortress.headers == {"Authorization": f"Bearer {fortress.access_token}"}


def test_get_envfile(fortress, credentials):
    fortress.configure(**credentials)
    envfile_id = uuid.uuid4().__str__()
    url = fortress._build_url(f"get-secret/{envfile_id}/")

    with requests_mock.Mocker() as m:
        mock_response = {
            "success": True,
            "secret_data": {
                "secret_type": "envfile",
                "uuid": envfile_id,
                "name": "test_envfile_name",
                "container": {},
                "value": "KEY=VALUE\nANOTHER_KEY=ANOTHER_VALUE\n",
                "notes": None,
            },
            "message": "envfile successfully retrieved.",
        }

        m.post(url=url, json=mock_response)
        envfile_content = fortress.get_envfile(envfile_id)
        assert envfile_content == "KEY=VALUE\nANOTHER_KEY=ANOTHER_VALUE\n"


def test_load_env(fortress, credentials):
    fortress.configure(**credentials)
    envfile_id = uuid.uuid4().__str__()
    url = fortress._build_url(f"get-secret/{envfile_id}/")

    original_env = dict(os.environ)
    assert os.environ.get('KEY') is None
    assert os.environ.get('ANOTHER_KEY') is None

    with requests_mock.Mocker() as m:
        mock_response = {
            "success": True,
            "secret_data": {
                "secret_type": "envfile",
                "uuid": envfile_id,
                "name": "test_envfile_name",
                "container": {},
                "value": "KEY=VALUE\nANOTHER_KEY=ANOTHER_VALUE\n",
                "notes": None,
            },
            "message": "envfile successfully retrieved.",
        }
        m.post(url=url, json=mock_response)
        result = fortress.load_env(envfile_id)

        assert result is True
        assert os.environ.get('KEY') == 'VALUE'
        assert os.environ.get('ANOTHER_KEY') == 'ANOTHER_VALUE'

    os.environ.clear()
    os.environ.update(original_env)
