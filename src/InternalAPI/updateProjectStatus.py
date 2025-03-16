from flask import request, jsonify
import os

from API.services.helpers import get_db_connection


def UPS_routes():
    # Handle preflight request
    if request.method == 'OPTIONS':
        return ''
    
    # Validate the token
    token = request.json.get('token')
    if token != os.getenv("InternalAPIKey"):
        return jsonify({"error": "Invalid token"}), 401
    
    # Extract data from request
    projectID = request.json.get('projectID')
    shared = request.json.get('shared')
    
    if projectID is None or shared is None:
        return jsonify({"error": "Missing required information"}), 400
    
    if not (shared == 0 or shared == 1):
        return jsonify({"error": "Invalid projectID"}), 400

    # Step 1: Establish DB connection
    db_connection = get_db_connection("projects")
    cursor = db_connection.cursor(dictionary=True)

    # Step 2: Insert or Update user's token in one query
    query = """
    UPDATE projects
    SET isShared = %s
    WHERE projectID = %s
    """
    cursor.execute(query, (shared, projectID))
    db_connection.commit()
    cursor.close()

    # Step 3: Return success response
    return jsonify({"status": "success", "info": "Project status updated"}), 200
