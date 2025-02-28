import mysql.connector 

def get_mysql_connection():
    conn = mysql.connector.connect(
        host = "localhost",
        user = "user",
        password = "******",
        database = "billing_db"
    )
    return conn
#if __name__ == "__main__":
