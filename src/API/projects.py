from flask import request, jsonify


import API.services as services
def projects_route(subpath=""):
    if request.method == 'POST':
        return services.createNewProject(request)

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
        return services.loadProject(project_id,request)
    else:
        return jsonify({"status": "error", "error": "method not implemented"}), 405
