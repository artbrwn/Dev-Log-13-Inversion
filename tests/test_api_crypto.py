import inversion_app.models.api_crypto as api_cripto
import pytest
import unittest.mock as mock
from inversion_app.models.api_crypto import ApiCrypto
from requests import RequestException, HTTPError


@mock.patch("inversion_app.models.api_crypto.requests.get")
def test_get_good_conversion_price(mock_get):
    data = {"status": {
                        "timestamp": "2025-10-24T10:27:48.051Z",
                        "error_code": 0,
                        "error_message": None,
                        "elapsed": 12,
                        "credit_count": 1,
                        "notice": None
                    },
                    "data": {
                        "id": 1,
                        "symbol": "BTC",
                        "name": "Bitcoin",
                        "amount": 1,
                        "last_updated": "2025-10-24T10:25:00.000Z",
                        "quote": {
                            "2790": {
                                "price": 95680.67636668718,
                                "last_updated": "2025-10-24T10:26:02.000Z"
                            }
                        }
                    }
                }
    mock_response = mock.Mock()
    mock_response.json.return_value = data
    mock_get.return_value = mock_response
    api_control = api_cripto.ApiCrypto()
    conversion_price = api_control.get_conversion_price(1, 1, 2790)

    assert conversion_price == data["data"]["quote"]["2790"]["price"]

@mock.patch("inversion_app.models.api_crypto.requests.get")
def test_capture_http_exception(mock_get):
    mock_response = mock.Mock()
    mock_response.raise_for_status.side_effect = HTTPError()
    mock_get.return_value = mock_response

    api_control = ApiCrypto()
    with pytest.raises(api_cripto.ApiCryptoError) as e:
        api_control.get_conversion_price(1, -1, -2790)

    assert "API HTTP error" in str(e)

@mock.patch("inversion_app.models.api_crypto.requests.get")
def test_capture_requests_exception(mock_get):
    mock_response = mock.Mock()
    mock_response.raise_for_status.side_effect = RequestException()
    mock_get.return_value = mock_response

    api_control = ApiCrypto()
    with pytest.raises(api_cripto.ApiCryptoError) as e:
        api_control.get_conversion_price(1, 1, 2790)

    assert "Network error" in str(e) 