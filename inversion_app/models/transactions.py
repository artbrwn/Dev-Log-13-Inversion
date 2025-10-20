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