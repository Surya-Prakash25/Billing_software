import mysql.connector 

def get_mysql_connection():
    conn = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "Surya@2003",
        database = "billing_db"
    )
    return conn
#if __name__ == "__main__":
