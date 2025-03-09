from flask import request, jsonify
import os
import json

def projects_route(subpath=""):
    if subpath == '':
        return jsonify({"status": "error", "error": "project path not provided"}), 400
    
    if request.method == 'OPTIONS':
        return ""

    project_id = subpath.split("/")[0]
    #make sure it is a number
    if not project_id.isdigit():
            return jsonify({"status": "error", "error": "project id must be a number"}), 400
    # Handle OPTIONS requests
    

    elif request.method == 'PUT':
        # Save to server logic (authentication and saving JSON file)
        # Change project edit timestamp (logic to be implemented)
        # (FUTURE) prevent user from uploading random JSON (validate JSON format)
        
        # check if project exists
        project_data = request.json
        if(project_data is None):
            return jsonify({"status": "error", "error": "no project data provided"}), 400
        project_file_path = f'app/internalAPI/projectData/projectData/{project_id}.json'

        if not os.path.exists(project_file_path):
            return jsonify({"status": "error", "error": "project does not exist"}), 404
        try:
            # Save updated project data
            with open(project_file_path, 'w') as file:
                json.dump(project_data, file, indent=4)  # indent=4 for pretty printing
        except (IOError, json.JSONDecodeError) as e:
            return jsonify({"status": "error", "error": str(e)}), 500
        
        return jsonify({"status": "ok", "autosave-interval": "120"})

    elif request.method == 'GET':
        # Logic to check if project is public or accessible (to be implemented)
        try:
            with open(f'app/internalAPI/projectData/projectData/{project_id}.json', 'r') as file:
                data = json.load(file)
        except FileNotFoundError:
            return jsonify({"status": "error", "error": "torch does not exist"}), 404

        return jsonify(data)

    elif request.method == 'POST':
        # Logic to ensure the user is authorized to create a new project (to be implemented)
        # Logic to update DB & files for project creation (to be implemented)
        return jsonify({"status": "ok", "content-name": "1", "content-title": "untitled", "autosave-interval": "120"})

    else:
        return jsonify({"status": "error", "error": "method not implemented"}), 405
