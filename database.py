import mysql.connector

def get_db_connection():
    conn = mysql.connector.connect(
        host="localhost",
        user="username",
        password="****",
        database="billing_db"
    )
    return conn
