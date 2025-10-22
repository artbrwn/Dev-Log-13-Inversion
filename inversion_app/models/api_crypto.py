import requests
from config import API_KEY

class ApiCrypto:
    BASE_URL = "https://pro-api.coinmarketcap.com/"
    HEADERS = {"X-CMC_PRO_API_KEY": API_KEY}

    """
    def get_latest(self):
        url = self.BASE_URL+"v1/cryptocurrency/listings/latest"
        result = requests.get(url, headers=self.HEADERS)
        print(result)
    """

    def get_conversion_price(self, data_form):
        """
        Recieves a data_form with currency_from, amount_from, currency_to and returns conversion price. 
        """
        url = self.BASE_URL + "v2/tools/price-conversion"
        params = {
            "amount": data_form.amount_from,
            "id": data_form.currency_from_id,
            "convert_id": data_form.currency_to_id
        }
        response = requests.get(url, params=params)
        if not response["status"]["error_code"]:
            conversion_price = response["data"]["quote"][str(data_form.currency_to_id)]

        else:
            return response["status"]["error_message"]
        
        return conversion_price
    