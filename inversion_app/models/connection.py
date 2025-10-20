import sqlite3
from config import ORIGIN_DATA

class Connection:
    def __init__(self, query_sql, params=[]):
        self.connection = sqlite3.connect(ORIGIN_DATA)
        self.connection.row_factory = sqlite3.Row
        self.cursor = self.connection.cursor()
        self.response = self.cursor.execute(query_sql, params)