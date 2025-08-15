# db.py
import pymysql
import pymysql.cursors

# Database connection configuration
DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = "your_password_here"
DB_NAME = "your_database_name_here"

def get_connection():
    """
    Creates and returns a connection to the MySQL database.
    """
    try:
        connection = pymysql.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME,
            cursorclass=pymysql.cursors.DictCursor
        )
        return connection
    except pymysql.MySQLError as e:
        print("Error connecting to MySQL:", e)
        return None
