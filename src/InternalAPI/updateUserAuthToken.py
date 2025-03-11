from flask import request, jsonify
import os

from API.services.helpers import get_db_connection, verifyToken


def UUAT_routes():
    # Handle preflight request
    if request.method == 'OPTIONS':
        return ''
    
    # Validate the token
    token = request.json.get('token')
    if token != os.getenv("InternalAPIKey"):
        return jsonify({"error": "Invalid token"}), 401
    
    # Extract data from request
    username = request.json.get('user_id')
    usertoken = request.json.get('usertoken')
    tokenExpiration = request.json.get('tokenExpiration')
    
    if not username or not usertoken or not tokenExpiration:
        return jsonify({"error": "Missing required information"}), 400
    
    # Step 1: Establish DB connection
    db_connection = get_db_connection("users")
    cursor = db_connection.cursor(dictionary=True)

    # Step 2: Insert or Update user's token in one query
    query = """
        INSERT INTO users (Username, AuthToken, AuthTokenExpiration) 
        VALUES (%s, %s, %s)
        ON DUPLICATE KEY UPDATE 
        AuthToken = VALUES(AuthToken), 
        AuthTokenExpiration = VALUES(AuthTokenExpiration)
    """
    cursor.execute(query, (username, usertoken, tokenExpiration))
    db_connection.commit()
    cursor.close()

    # Step 3: Return success response
    return jsonify({"status": "success", "info": "User created or updated"}), 200
