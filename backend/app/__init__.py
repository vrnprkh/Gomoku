from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    CORS(app)
    JWTManager(app)
    
    from .auth import auth_bp
    from .players import players_bp
    from .friends import friends_bp

    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(players_bp, url_prefix='/api')
    app.register_blueprint(friends_bp, url_prefix='/api')
    return app
