from .updateUserAuthToken import UUAT_routes
from .updateProjectStatus import UPS_routes
from .updateProjectTitle import UPT_routes
from .deleteProject import deleteProject_routes

def internal_register_routes(app):
    app.add_url_rule("/internal/updateUserAuthToken", methods=['POST', 'OPTIONS'], view_func=UUAT_routes)
    app.add_url_rule("/internal/updateProjectStatus", methods=['POST', 'OPTIONS'], view_func=UPS_routes)
    app.add_url_rule("/internal/updateProjectTitle", methods=['POST', 'OPTIONS'], view_func=UPT_routes)
    app.add_url_rule("/internal/deleteProject", methods=['POST', 'OPTIONS'], view_func=deleteProject_routes)