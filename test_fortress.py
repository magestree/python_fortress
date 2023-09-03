import os

import pytest
import requests_mock

from python_fortress.fortress import Fortress, BASE_URL


@pytest.fixture
def fortress():
    return Fortress()


def test_load_fortress_credentials(fortress):
    def mock_dotenv_loader():
        return {
            "FORTRESS_API_KEY": "mock_api_key",
            "FORTRESS_ACCESS_TOKEN": "mock_access_token",
            "FORTRESS_MASTER_KEY": "mock_master_key",
            "FORTRESS_ENVFILE_NAME": "mock_envfile_name",
        }

    fortress.load_fortress_credentials(dotenv_loader=mock_dotenv_loader)

    assert fortress.api_key == "mock_api_key"
    assert fortress.access_token == "mock_access_token"
    assert fortress.master_key == "mock_master_key"
    assert fortress.envfile_name == "mock_envfile_name"


def test_build_url(fortress):
    endpoint = "sample-endpoint/"
    constructed_url = fortress._build_url(endpoint)
    assert constructed_url == f"{BASE_URL}{endpoint}"


def test_load_headers(fortress):
    fortress.access_token = "sample_token"
    fortress.load_headers()
    assert fortress.headers == {"Authorization": "Bearer sample_token"}


def test_get_envfile_success(fortress):
    with requests_mock.Mocker() as m:
        mock_response = {
            "success": True,
            "message": "OK",
            "envfile_data": {"value": "KEY=VALUE\nANOTHER_KEY=ANOTHER_VALUE\n"}
        }
        m.post(f'{BASE_URL}get-envfile/', json=mock_response)
        envfile_content = fortress.get_envfile()
        assert envfile_content == "KEY=VALUE\nANOTHER_KEY=ANOTHER_VALUE\n"


def test_get_envfile_failure(fortress):
    with requests_mock.Mocker() as m:
        mock_response = {
            "success": False,
            "message": "Unauthorized customer",
            "envfile_data": {}
        }
        m.post(f'{BASE_URL}get-envfile/', json=mock_response, status_code=401)
        envfile_content = fortress.get_envfile()
        assert envfile_content is None


def test_load_env(fortress):
    original_env = dict(os.environ)

    with requests_mock.Mocker() as m:
        mock_response = {
            "success": True,
            "message": "OK",
            "envfile_data": {"value": "KEY=VALUE\nANOTHER_KEY=ANOTHER_VALUE\n"}
        }
        m.post(f'{BASE_URL}get-envfile/', json=mock_response)
        result = fortress.load_env()

        assert result is True
        assert os.environ.get('KEY') == 'VALUE'
        assert os.environ.get('ANOTHER_KEY') == 'ANOTHER_VALUE'

    os.environ.clear()
    os.environ.update(original_env)
