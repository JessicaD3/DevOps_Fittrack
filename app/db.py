import os
import mysql.connector
from mysql.connector import Error


def get_conn():
    try:
        connection = mysql.connector.connect(
            host=os.getenv("DB_HOST", "127.0.0.1"),
            port=int(os.getenv("DB_PORT", 3306)),
            user=os.getenv("DB_USER", "root"),
            password=os.getenv("DB_PASSWORD", ""),
            database=os.getenv("DB_NAME", "fittrack"),
            connection_timeout=5,
        )

        return connection

    except Error as e:
        raise RuntimeError("Echec de connexion à la BDD") from e
