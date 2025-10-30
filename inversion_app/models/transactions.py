from inversion_app.models.connection import Connection
import sqlite3
import config
from inversion_app.models.api_crypto import ApiCrypto, ApiCryptoError

class TransactionError(Exception):
    """Exception for transaction operations"""
    pass

class Transaction:
    def __init__(self):
        self.db_path = config.ORIGIN_DATA
        self.eur_id = config.CURRENCIES["EUR"]

    def get_all(self):
        try:
            query = "SELECT * FROM transactions ORDER BY date DESC, time DESC"
            conn = Connection(query)
            result = conn.response.fetchall()
            conn.connection.close()
            return [dict(row) for row in result]
        except sqlite3.Error as e:
            raise TransactionError(f"Unable to get transactions: {e}")

    def insert(self, data_form):
        try:
            query = "INSERT INTO transactions (date, time, currency_from, amount_from, currency_to, amount_to) VALUES (?, ?, ?, ?, ?, ?)"
            conn = Connection(query, data_form)
            conn.connection.commit()
            conn.connection.close()
        except sqlite3.Error as e:
            raise TransactionError(f"Unable to save the transaction: {e}")

    def get_owned_currencies(self) -> dict:
        """
        Returns a dictionary with the ID of the owned currencies as key and its balance as value.
        """
        try:
            query = "SELECT currency_from, amount_from, currency_to, amount_to FROM transactions"
            conn = Connection(query)
            rows = conn.response.fetchall()
            conn.connection.close()

            balances = {}
            for row in rows:
                balances[row["currency_from"]] = balances.get(row["currency_from"], 0) - row["amount_from"]
                balances[row["currency_to"]] = balances.get(row["currency_to"], 0) + row["amount_to"]

            # Euros always available
            owned = {currency: balance for currency, balance in balances.items() if balance > 0}
            owned[config.CURRENCIES["EUR"]] = float("inf")

            return owned

        except sqlite3.Error as e:
            raise TransactionError(f"Unable to get the currencies: {e}")
        
    def get_total_investment(self) -> float:
        """
        Returns the sum of amount_from where currency_from equals EUR 
        """
        try:
            query = "SELECT SUM(amount_from) FROM transactions WHERE currency_from = ?;"
            conn = Connection(query, (self.eur_id,)) 
            result = conn.response.fetchone()
            conn.connection.close()
            return result[0] if result and result[0] != None else 0
        
        except sqlite3.Error as e:
            raise TransactionError(f"Unable to get invested EUR in database: {e}")
        
    def get_total_recovered(self) -> float:
        """
        Returns de sum of amount_to where currency_to equals EUR.
        """
        try:
            query = "SELECT SUM(amount_to) FROM transactions WHERE currency_to = ?;"
            conn = Connection(query, (self.eur_id,)) 
            result = conn.response.fetchone()
            conn.connection.close()

            return result[0] if result and result[0] != None else 0
        
        except sqlite3.Error as e:
            raise TransactionError(f"Unable to get recovered EUR in database: {e}")
        
    def calculate_actual_value(self) -> float:
        """
        Returns the sum of all owned currencies in EUR.
        """
        actual_value = 0
        owned = self.get_owned_currencies()
        if not owned:
            return 0.0

        request = ApiCrypto()
        for coin, balance in owned.items():
            if coin != self.eur_id:
                try:
                    conversion_price = request.get_conversion_price(balance, coin, self.eur_id)
                    actual_value += conversion_price
                except ApiCryptoError as e:
                    raise TransactionError("Unable to get equivalences for all currencies.")    

        return actual_value

