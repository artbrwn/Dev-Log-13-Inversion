from inversion_app.models.connection import Connection
import sqlite3

def get_all_transactions() -> list[dict]:
    try:
        query = "SELECT * FROM transactions"
        conn = Connection(query)
        result = conn.response.fetchall()
        transaction_list = [dict(row) for row in result]
        conn.connection.close()
        return transaction_list
    except sqlite3.Error as e:
        return f"No se han podido cargar los movimientos: {e}"

def insert_transaction(data_form):
    try:
        query = "INSERT INTO transactions (data, time, currency_from, amount_from, currency_to, amount_to) values (?, ?, ?, ?, ?, ?)"
        conn = Connection(query, data_form)
        conn.connection.commit()
        conn.connection.close()

    except sqlite3.Error as e:
        return f"No se ha podido guardar la transacción: {e}"
    
def get_owned_currencies():
    """
    Returns a dictionary with all coins with a positive balance in database as key and it's balance as value.
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

        owned_currencies = {currency: balance for currency, balance in balances.items() if balance > 0}

        return owned_currencies

    except sqlite3.Error as e:
        return f"No se ha podido obtener el balance: {e}"