from .ScratchDownloader import ScratchDownloader
def SD_register_routes(app):
    app.add_url_rule("/ScratchDownloader", methods=['POST', 'OPTIONS'], view_func=ScratchDownloader)
