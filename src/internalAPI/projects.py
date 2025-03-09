from flask import request, jsonify
import os
import json

def projects_route(subpath=""):
    if subpath == '':
        return jsonify({"status": "error", "error": "project path not provided"}), 400
    # Handle OPTIONS requests
    if request.method == 'OPTIONS':
        return ""

    elif request.method == 'PUT':
        # Save to server logic (authentication and saving JSON file)
        # Change project edit timestamp (logic to be implemented)
        return jsonify({"status": "ok", "autosave-interval": "120"})

    elif request.method == 'GET':
        # Logic to check if project is public or accessible (to be implemented)
        # Read JSON file from the server

        try:
            with open(f'app/internalAPI/projectData/projectData/1.json', 'r') as file:
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
