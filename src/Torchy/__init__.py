from .main import chat,chat_fail,get_ai_models
def torchy_routes(app):
    app.add_url_rule("/torchy/chat", methods=['POST'], view_func=chat)
    app.add_url_rule("/torchy/chat", methods=['GET'], view_func=chat_fail)
    app.add_url_rule("/torchy/AI_models", methods=['GET'], view_func=get_ai_models)
