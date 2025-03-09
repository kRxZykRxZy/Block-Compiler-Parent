# Internal API Structure

There are 3 files that scratch calls:

## assets.py
Responsible for managing project assets

`POST`: updates/creates a new asset

`GET`: returns a specific asset

## projects.py
Responsible for managing the projects JSON file

`PUT`: updates the projects JSON file

`GET`: returns the projects JSON file

`POST`: creates a new project 

## projectsMETA.py
Used to get a project's metadata (EG: likes, loves, views)

`GET`: returns the metadata for a project