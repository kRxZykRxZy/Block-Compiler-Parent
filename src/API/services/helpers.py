import mysql.connector
import os
from datetime import datetime
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import redis

redis_connection = redis.Redis(host='bc_redis', port=6379)
# Create a global limiter instance
limiter = Limiter(
    get_remote_address,
    default_limits=[],
    storage_uri="redis://bc_redis:6379",
)

def get_db_connection(database="projects"):
    """
    Establishes and returns a MySQL database connection.
    """
    try:
        return mysql.connector.connect(
            host="bc_mysql",
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
