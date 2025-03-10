import mysql.connector
import os
from datetime import datetime

def get_db_connection(database="projects"):
    """
    Establishes and returns a MySQL database connection.
    """
    try:
        return mysql.connector.connect(
            host="mysql",
            user="root",
            password=os.getenv("MYSQL_ROOT_PASSWORD"),
            database=database
        )
    except mysql.connector.Error as err:
        raise Exception(f"Error connecting to database: {err}")

def verifyToken(token,user_id): 
    """
    Verifies the provided token against the user's stored token in the database.
    """
    db_connection = get_db_connection("users")
    cursor = db_connection.cursor(dictionary=True)
    query = "SELECT AuthToken,AuthTokenExpiration FROM users WHERE Username = %s"
    cursor.execute(query, (user_id,))
    user = cursor.fetchone()
    if not user:
        return False
    cursor.close()
    db_connection.close()
    if user['AuthToken'] == token:
        # verify it hasn't expired (AuthTokenExpiration is a timestamp)
        if user['AuthTokenExpiration'] > datetime.now():
            return True
    else:
        return False
