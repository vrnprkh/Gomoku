from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
import logging
from secret import db_password
import bcrypt

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

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
        
        # Fetch user from database
        cursor.execute("SELECT * FROM Users WHERE username = %s", (username,))
        user = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        if user:
            logger.info(f"User found: {user}")
            if bcrypt.checkpw(password.encode('utf-8'), user['pwd'].encode('utf-8')):
                logger.info("Password match, login successful")
                return jsonify({'message': 'Login successful', 'uid': user['uid']}), 200
            else:
                logger.info("Password mismatch")
                return jsonify({'message': 'Invalid password'}), 401
        else:
            logger.info("User not found")
            return jsonify({'message': 'User not found'}), 404
    except Exception as e:
        logger.error(f"Error in login: {str(e)}", exc_info=True)
        return jsonify({'message': 'Login failed', 'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)