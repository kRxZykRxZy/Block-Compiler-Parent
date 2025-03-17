from flask import request, jsonify

from API.services.helpers import get_db_connection, verifyToken

def get_username_by_token(token):
    query = "SELECT username FROM users WHERE AuthToken = %s"
    
    try:
        db_connection = get_db_connection("users")
        with db_connection.cursor(dictionary=True) as cursor:
            cursor.execute(query, (token,))
            user = cursor.fetchone() or {"username": ""}
        return user
    except Exception as err:
        return {"username": ""}
    finally:
        db_connection.close()


def projectsMETA_route():
    # Handle OPTIONS requests
    if request.method == 'OPTIONS':
        return ""
    
    elif request.method == 'GET':
        project_id = request.args.get('id')
        if not project_id:
            return jsonify({
                "status": "error",
                "message": "Missing project ID"
            }), 400
        # make sure project_id is an integer
        if not project_id.isdigit():
                return jsonify({
                    "status": "error",
                    "message": "Project ID must be a number"
                }), 400
        # Step 1: Establish DB connection
        try:
            db_connection = get_db_connection()
            cursor = db_connection.cursor(dictionary=True)

            # Step 2: Query the database for the project
            query = "SELECT Title, Owner, isShared FROM projects WHERE projectID = %s"
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
            # Step 4: Get the current user's username
            user = get_username_by_token(request.args.get('token'))['username']
            canRemix = "false"
            if user and user != project['Owner'] and project['isShared'] == 1:
                canRemix = "true"
            # Step 5: Return the project metadata
            metadata = {
                "id": project_id,
                "title": project['Title'],
                "visibility": "true" if project['isShared'] == 1 else "false",
                "author": {
                    "username": project['Owner'],
                    "history": {"joined": "1900-01-01T00:00:00.000Z"},
                },
                "username": user,
                "canSave": "true" if project['Owner'] == user else "false",
                "canRemix": canRemix
            }
            return jsonify(metadata)


        except Exception as err:
            # Handle any other unexpected errors
            return jsonify({
                "status": "error",
                "message": str(err)
            }), 500

        finally:
            cursor.close()
            db_connection.close()
    else:
        # Return error for unsupported methods
        return jsonify({"status": "error", "error": "method not implemented"}), 405
