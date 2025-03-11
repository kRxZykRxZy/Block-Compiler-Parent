import os
import json
from flask import jsonify

from API.services.helpers import get_db_connection, verifyToken


def internalSaveProject(request, project_id):
    # check if project exists
    project_data = request.json
    if(project_data is None):
        return jsonify({"status": "error", "error": "no project data provided"}), 400
    project_file_path = f'app/storage/projectData/projectData/{project_id}.json'

    if not os.path.exists(project_file_path):
        return jsonify({"status": "error", "error": "project does not exist"}), 404
    try:
        # Save updated project data
        with open(project_file_path, 'w') as file:
            json.dump(project_data, file, indent=4)  # indent=4 for pretty printing
    except (IOError, json.JSONDecodeError) as e:
        return jsonify({"status": "error", "error": str(e)}), 500
    
    return jsonify({"status": "ok", "autosave-interval": "120"})


def saveProject(request, project_id):
    # (FUTURE) prevent user from uploading random JSON (validate JSON format)

    # Step 1: Establish DB connection
    try:
        token = request.args.get('token')
        if not token:
            return jsonify({
                "status": "error",
                "message": "Missing token"
            }), 400
        db_connection = get_db_connection()
        cursor = db_connection.cursor()

        # Step 2: Query the database for the project
        query = "SELECT Owner FROM projects WHERE projectID = %s"
        cursor.execute(query, (project_id,))
        project = cursor.fetchone()
        if not project:
            return jsonify({
                "status": "error",
                "message": "Invalid project ID"
            }), 404
        
        # Step 3: Verify the token
        if not verifyToken(token, project['Owner']):
            return jsonify({
                "status": "error",
                "message": "Invalid token"
            }), 403
        
        # Step 4: Update project timestamp
        query = "UPDATE projects SET EditTS = CURRENT_TIMESTAMP WHERE projectID = %s"
        cursor.execute(query, (project_id,))
        db_connection.commit()

        return internalSaveProject(request, project_id)
    
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500
    finally:
        cursor.close()
        db_connection.close()


