from flask import Flask
from app.auth.auth_api import auth_rest_api
from app.auth.routes import auth_bp
from app.api.routes import api_bp, api_generator
from app.db.models import init_db
from app.api.views import api_services
from app.config import Config
from dotenv import load_dotenv

load_dotenv()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    init_db()
    app.register_blueprint(auth_bp)
    app.register_blueprint(api_bp, url_prefix='/api')
    app.register_blueprint(api_generator)
    app.register_blueprint(api_services)
    app.register_blueprint(auth_rest_api)
    return app
