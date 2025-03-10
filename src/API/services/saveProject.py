import os
import json
from flask import jsonify

def saveProject(request, project_id):
    # Save to server logic (authentication and saving JSON file)
    # Change project edit timestamp (logic to be implemented)
    # (FUTURE) prevent user from uploading random JSON (validate JSON format)
    
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
