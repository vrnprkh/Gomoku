from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from datetime import timedelta
from config import Config
from app.auth import auth_bp
from app.players import players_bp
from app.friends import friends_bp
from app.lobbies import lobbies_bp
from app.detailedmoves import detailed_moves_bp
import logging
app = Flask(__name__)
app.config.from_object(Config)
CORS(app)

# JWT Configuration
app.config['JWT_SECRET_KEY'] = Config.JWT_SECRET_KEY
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = Config.JWT_ACCESS_TOKEN_EXPIRES
jwt = JWTManager(app)

app.register_blueprint(auth_bp, url_prefix='/api/')
app.register_blueprint(players_bp, url_prefix='/api')
app.register_blueprint(friends_bp, url_prefix='/api')
app.register_blueprint(lobbies_bp, url_prefix='/api')
app.register_blueprint(detailed_moves_bp, url_prefix='/api')


if __name__ == "__main__":
    app.run(debug=True)
