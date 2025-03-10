from flask import jsonify
import json

from API.services.helpers import get_db_connection, verifyToken

def loadProject(project_id,request):
    """
    Loads a project from a JSON file based on the project ID.
    Checks if the project is public or if the ID is valid.
    Returns the project data if found and accessible, otherwise returns an error.
    """
    # Step 1: Establish DB connection
    try:
        db_connection = get_db_connection()
        cursor = db_connection.cursor(dictionary=True)

        # Step 2: Query the database for the project
        query = "SELECT Owner, isShared FROM projects WHERE projectID = %s"
        cursor.execute(query, (project_id,))
        project = cursor.fetchone()

        if not project:
            return jsonify({
                "status": "error",
                "message": "Invalid project ID"
            }), 404

        # Step 3: Check if the project is public or if a valid token is provided
        if project['isShared'] == 0:
            if not request.args.get('token'):
                return jsonify({
                    "status": "error",
                    "message": "Project is not public"
                }), 403
            if not verifyToken(request.args.get('token'),project['Owner']):
                return jsonify({
                    "status": "error",
                    "message": "Invalid token"
                }), 403

        # Step 4: Load the project data from the file
        file_path = f'app/storage/projectData/projectData/{project_id}.json'
        try:
            with open(file_path, 'r') as file:
                data = json.load(file)

            # Return the loaded project data as a JSON response
            return jsonify(data)

        except FileNotFoundError:
            return jsonify({
                "status": "error",
                "message": "Project data file does not exist"
            }), 404

        except json.JSONDecodeError:
            return jsonify({
                "status": "error",
                "message": "Failed to parse project data"
            }), 500

    except Exception as err:
        # Handle any other unexpected errors
        return jsonify({
            "status": "error",
            "message": str(err)
        }), 500

    finally:
        cursor.close()
        db_connection.close()
