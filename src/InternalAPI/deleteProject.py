from flask import request, jsonify
import os
import json

from API.services.helpers import get_db_connection

def deleteProject_routes():
    # Handle preflight request
    if request.method == 'OPTIONS':
        return ''

    token = request.json.get('token')
    if token != os.getenv("InternalAPIKey"):
        return jsonify({"error": "Invalid token"}), 401

    projectID = request.json.get('projectID')
    if projectID is None:
        return jsonify({"error": "Missing required information"}), 400

    db_connection = get_db_connection("projects")
    cursor = db_connection.cursor(dictionary=True)
    # Step 2: Delete the project from the database
    query = """
    DELETE FROM projects
    WHERE projectID = %s
    """
    cursor.execute(query, (projectID,))
    db_connection.commit()
    cursor.close()
    db_connection.close()
    
    # Step 3: Delete the project file from the filesystem
    path = os.path.join('storage/projectData/projectData/', f'{projectID}.json')

    # Read as JSON
    if not os.path.exists(path):
        return json.dumps({"status": "false", "error": "Failed to delete project (-0)"})

    try:
        with open(path, 'r') as f:
            data = json.load(f)
    except json.JSONDecodeError:
        return json.dumps({"status": "false", "error": "Failed to delete project (0)"})
    except Exception as e:
        return json.dumps({"status": "false", "error": f"Failed to read or decode JSON: {str(e)}"}) # More descriptive error

    # Delete file
    if os.path.exists(path):
        try:
            os.unlink(path)
        except OSError as e:
            return json.dumps({"status": "false", "error": f"Failed to delete project file: {str(e)}"}) # more descriptive error
    else:
        return json.dumps({"status": "false", "error": "Failed to delete project (-1)"})

    try: # wrap the whole asset deletion in a try-except to prevent incomplete deletions
        if 'targets' in data:
            data = data['targets']
            fonts = data.get('customFonts', [])  # Handle missing customFonts key

            for sprite in data:
                if 'costumes' in sprite:
                    for costume in sprite['costumes']:
                        costume_md5ext = costume['md5ext']
                        asset_path = os.path.join('storage/projectData/projectAssets/', costume_md5ext)
                        if costume_md5ext not in ('592bae6f8bb9c8d88401b54ac431f7b6.svg', 'cd21514d0531fdffb22204e0ec5ed84a.svg'):
                            if os.path.exists(asset_path):
                                try:
                                    os.unlink(asset_path)
                                except OSError as e:
                                    print(f"Error deleting costume asset {asset_path}: {e}") # Print error but don't stop.  Could also log.
                                    #  Original PHP code commented out the exit, so this maintains that behavior.
                            else:
                                print(f"Costume asset not found: {asset_path}")  #Log or print missing asset

                if 'sounds' in sprite:
                    for sound in sprite['sounds']:
                        sound_md5ext = sound['md5ext']
                        asset_path = os.path.join('storage/projectData/projectAssets/', sound_md5ext)
                        if os.path.exists(asset_path):
                            try:
                                os.unlink(asset_path)
                            except OSError as e:
                                print(f"Error deleting sound asset {asset_path}: {e}") # Print error, continue
                        else:
                            print(f"Sound asset not found: {asset_path}")


            if fonts:
                for font in fonts:
                    if isinstance(font, dict) and 'md5ext' in font: # locally called fonts don't have md5ext
                        font_md5ext = font['md5ext']
                        asset_path = os.path.join('storage/projectData/projectAssets/', font_md5ext)
                        if os.path.exists(asset_path):
                            try:
                                os.unlink(asset_path)
                            except OSError as e:
                                print(f"Error deleting font asset {asset_path}: {e}")  # Print error, continue
                        else:
                            print(f"Font asset not found: {asset_path}")



        else:
            assets_to_delete = []
            if 'sounds' in data:
                for sound in data['sounds']:
                    sound_md5 = sound['md5']
                    assets_to_delete.append(sound_md5)

            if 'costumes' in data:
                for costume in data['costumes']:
                    costume_md5 = costume['baseLayerMD5']
                    assets_to_delete.append(costume_md5)

            if 'children' in data:
                for element in data['children']:
                    if 'costumes' in element:
                        for costume in element['costumes']:
                            costume_md5 = costume['baseLayerMD5']
                            assets_to_delete.append(costume_md5)
                    if 'sounds' in element:
                        for sound in element['sounds']:
                            sound_md5 = sound['md5']
                            assets_to_delete.append(sound_md5)

            for asset in assets_to_delete:
                asset_path = os.path.join('storage/projectData/projectAssets/', asset)
                if os.path.exists(asset_path):
                    try:
                        os.unlink(asset_path)
                    except OSError as e:
                        print(f"Error deleting asset {asset_path}: {e}")
                else:
                    print(f"Asset not found: {asset_path}")

    except Exception as e:
        return json.dumps({"status": "false", "error": f"Error during asset deletion: {str(e)}"})


    return json.dumps({"status": "true"})

