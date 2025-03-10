from .assets import assets_route
from .projects import projects_route
from .projectsMETA import projectsMETA_route

def register_routes(app):
    app.add_url_rule("/assets", methods=['GET', 'POST', 'OPTIONS'], view_func=assets_route)
    app.add_url_rule("/assets/<path:subpath>", methods=['GET', 'POST', 'OPTIONS'], view_func=assets_route)
    app.add_url_rule("/projects", methods=['PUT', 'GET', 'POST', 'OPTIONS'], view_func=projects_route)
    app.add_url_rule("/projects/", methods=['PUT', 'GET', 'POST', 'OPTIONS'], view_func=projects_route)
    app.add_url_rule("/projects/<path:subpath>", methods=['PUT', 'GET', 'POST', 'OPTIONS'], view_func=projects_route)
    app.add_url_rule('/projectsMETA', methods=['GET', 'OPTIONS'], view_func=projectsMETA_route)    