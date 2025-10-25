from inversion_app.models.connection import Connection
import sqlite3
import config

class TransactionError(Exception):
    """Exception for transaction operations"""
    pass

class Transaction:
    def __init__(self):
        self.db_path = config.ORIGIN_DATA

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

    def get_owned_currencies(self):
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
