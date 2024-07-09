from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
import logging
from secret import db_password
import bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from datetime import timedelta

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# JWT Configuration
app.config['JWT_SECRET_KEY'] = 'e0bfbdc6f20e75761fed41afc58dd29561363be23b22be29a6c42f6e60395054'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=30)
jwt = JWTManager(app)

def get_db_connection():
    try:
        conn = mysql.connector.connect(
            user="gomoku_db_admin",
            password=db_password,
            host="gomoku-database.mysql.database.azure.com",
            port=3306,
            database="test_database",
            ssl_ca="DigiCertGlobalRootG2.crt.pem",
            ssl_disabled=False
        )
        logger.info("Database connection successful")
        return conn
    except Exception as e:
        logger.error(f"Database connection failed: {str(e)}", exc_info=True)
        raise

@app.route('/')
def home():
    return "Welcome to the Gomoku API"

@app.route('/test_db')
def test_db():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return "DB connection successful"
    except Exception as e:
        logger.error(f"DB connection failed: {str(e)}", exc_info=True)
        return f"DB connection failed: {str(e)}"

#SIGN UP
@app.route('/api/signup', methods=['POST'])
def signup():
    try:
        data = request.json
        username = data.get('username')
        password = data.get('password')
        
        if len(username) > 16 or len(password) > 16:
            return jsonify({'message': 'Username and password must be 16 characters or less'}), 400
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Check if user already exists
        cursor.execute("SELECT * FROM Users WHERE username = %s", (username,))
        if cursor.fetchone():
            return jsonify({'message': 'Username already exists'}), 400
        
        cursor.execute("SELECT MAX(uid) FROM Users")
        max_uid = cursor.fetchone()[0]
        new_uid = 1 if max_uid is None else max_uid + 1
        
        # Hash the password
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        
        cursor.execute("INSERT INTO Users (uid, username, pwd) VALUES (%s, %s, %s)", (new_uid, username, hashed_password))
        conn.commit()
        
        cursor.close()
        conn.close()
        
        return jsonify({'message': 'User created successfully'}), 201
    except Exception as e:
        logger.error(f"Error in signup: {str(e)}", exc_info=True)
        return jsonify({'message': 'Signup failed', 'error': str(e)}), 500

#LOGIN
@app.route('/api/login', methods=['POST'])
def login():
    try:
        data = request.json
        username = data.get('username')
        password = data.get('password')
        
        logger.info(f"Login attempt for username: {username}")
        
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute("SELECT * FROM Users WHERE username = %s", (username,))
        user = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        if user and bcrypt.checkpw(password.encode('utf-8'), user['pwd'].encode('utf-8')):
            access_token = create_access_token(identity=user['uid'])
            return jsonify(access_token=access_token, user_id=user['uid']), 200
    except Exception as e:
        logger.error(f"Error in login: {str(e)}", exc_info=True)
        return jsonify({'message': 'Login failed', 'error': str(e)}), 500


@app.route('/api/user/<int:user_id>', methods=['GET'])
@jwt_required()
def get_user_data(user_id):
    current_user_id = get_jwt_identity()
    logger.info(f"Requested user_id: {user_id}, Current user_id: {current_user_id}")
    
    if current_user_id != user_id:
        logger.warning(f"Unauthorized access attempt: requested {user_id}, current user {current_user_id}")
        return jsonify({'message': 'Unauthorized access'}), 403

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute("SELECT username FROM Users WHERE uid = %s", (current_user_id,))
        user_data = cursor.fetchone()
        
        if not user_data:
            logger.warning(f"No user found for user_id: {current_user_id}")
            return jsonify({'message': 'User not found'}), 404

        logger.info(f"User data fetched: {user_data}")
        
        cursor.close()
        conn.close()

        return jsonify({
            'username': user_data['username'],
            'profilePicture': 'https://via.placeholder.com/150'
        }), 200
    except Exception as e:
        logger.error(f"Error fetching user data: {str(e)}", exc_info=True)
        return jsonify({'message': 'Failed to fetch user data'}), 500

if __name__ == '__main__':
    app.run(debug=True)