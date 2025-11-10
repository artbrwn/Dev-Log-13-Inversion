import requests
from config import API_KEY
import time

class ApiCryptoError(Exception):
    """Exception for cryptocurrencies API queries errors"""
    pass

class ApiCrypto:
    BASE_URL = "https://pro-api.coinmarketcap.com/"
    HEADERS = {"X-CMC_PRO_API_KEY": API_KEY}

    def get_conversion_price(self, amount_from: float, currency_from: int, currency_to: int) -> float:
        """
        Receives a data_form with currency_from, amount_from, currency_to and returns conversion price. 
        Raises ApiCryptoError if anything goes wrong.
        """
        url = self.BASE_URL + "v2/tools/price-conversion"
        try:
            params = {
                "amount": amount_from,
                "id": currency_from,
                "convert_id": currency_to
            }
            response = requests.get(url, params=params, headers=self.HEADERS)
            response.raise_for_status()

            data = response.json()
            conversion_price = data["data"]["quote"][str(currency_to)]["price"]
            time.sleep(0.1)

            return conversion_price
        
        except requests.HTTPError as e:
            raise ApiCryptoError(f"API HTTP error: {e}")
        
        except requests.RequestException as e:
            raise ApiCryptoError(f"Network error: {e}")
          
        except (ValueError, KeyError) as e:
            raise ApiCryptoError(f"Invalid API response format: {e}")

        
        
    