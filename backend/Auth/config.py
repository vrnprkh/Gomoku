from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from datetime import timedelta
from config import Config
from app.auth import auth_bp
from app.players import players_bp

app = Flask(__name__)
app.config.from_object(Config)
CORS(app, supports_credentials=True)  # Ensure CORS is correctly configured

# JWT Configuration
app.config['JWT_SECRET_KEY'] = Config.JWT_SECRET_KEY
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = Config.JWT_ACCESS_TOKEN_EXPIRES
jwt = JWTManager(app)

app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(players_bp, url_prefix='/api')

if __name__ == "__main__":
    app.run(debug=True)
