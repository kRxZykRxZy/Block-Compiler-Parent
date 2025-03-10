from flask import request, jsonify
import os
import json
import re

def projectsMETA_route():
    # Handle OPTIONS requests
    if request.method == 'OPTIONS':
        return ""
    
    elif request.method == 'GET':
        # Respond with static metadata
        metadata = {
            "id": "32",
            "title": "Waterfall Plains v1.0",
            "visibility": "true",
            "isOwner": "false",
            "author": {
                "DisplayName": "Titanium",
                "username": "Titanium",
                "history": {"joined": "1900-01-01T00:00:00.000Z"},
                "profile": {
                    "id": None,
                    "images": {
                        "90x90": "/IMGStorage/Logos/Titanium.jpeg?width=90&height=90",
                        "60x60": "/IMGStorage/Logos/Titanium.jpeg?width=60&height=60",
                        "55x55": "/IMGStorage/Logos/Titanium.jpeg?width=55&height=55",
                        "50x50": "/IMGStorage/Logos/Titanium.jpeg?width=50&height=50",
                        "32x32": "/IMGStorage/Logos/Titanium.jpeg?width=32&height=32",
                    },
                },
            },
        }
        return jsonify(metadata)

    else:
        # Return error for unsupported methods
        return jsonify({"status": "error", "error": "method not implemented"}), 405
