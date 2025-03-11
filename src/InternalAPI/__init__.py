from .updateUserAuthToken import UUAT_routes

def internal_register_routes(app):
    app.add_url_rule("/internal/updateUserAuthToken", methods=['POST', 'OPTIONS'], view_func=UUAT_routes)
