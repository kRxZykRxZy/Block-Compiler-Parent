from flask import jsonify

def createNewProject():
        # Logic to ensure the user is authorized to create a new project (to be implemented)
        # Logic to update DB & files for project creation (to be implemented)
        return jsonify({"status": "ok", "content-name": "1", "content-title": "untitled", "autosave-interval": "120"})


