from flask import request, jsonify
import os
import json

import API.services as services
def projects_route(subpath=""):
    if request.method == 'POST':
        return services.createNewProject()

    # OPTIONS requests
    if request.method == 'OPTIONS':
        return ""

    # PUT and GET requests

    if subpath == '':
        return jsonify({"status": "error", "error": "project path not provided"}), 400
    
    project_id = subpath.split("/")[0]
    #make sure it is a number
    if not project_id.isdigit():
            return jsonify({"status": "error", "error": "project id must be a number"}), 400    

    elif request.method == 'PUT':
        return services.saveProject(request, project_id)
    elif request.method == 'GET':
        # Logic to check if project is public or accessible (to be implemented)
        try:
            with open(f'app/storage/projectData/projectData/{project_id}.json', 'r') as file:
                data = json.load(file)
        except FileNotFoundError:
            return jsonify({"status": "error", "error": "torch does not exist"}), 404

        return jsonify(data)

    else:
        return jsonify({"status": "error", "error": "method not implemented"}), 405
