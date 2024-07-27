from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
import mysql.connector
import logging
import bcrypt
from dotenv import load_dotenv
import os
from config import Config

load_dotenv()

db_user = os.getenv("DB_USER")
db_password = os.getenv('DB_PASSWORD')
db_host = os.getenv("DB_HOST")
db_name = os.getenv("DB_NAME")


auth_bp = Blueprint('auth', __name__)
logger = logging.getLogger(__name__)

def get_db_connection():
    try:
        conn = mysql.connector.connect(
            user=db_user,
            password=db_password,
            host=db_host,
            port=3306,
            database=db_name,
            ssl_ca="DigiCertGlobalRootG2.crt.pem",
            ssl_disabled=False
        )
        logger.info("Database connection successful")
        return conn
    except Exception as e:
        logger.error(f"Database connection failed: {str(e)}", exc_info=True)
        raise

@auth_bp.route('/')
def home():
    return "Welcome to the Gomoku API"

@auth_bp.route('/test_db')
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

@auth_bp.route('/signup', methods=['POST'])
def signup():
    try:
        data = request.json
        username = data.get('username')
        password = data.get('password')
        
        if len(username) > 16 or len(password) > 16:
            return jsonify({'message': 'Username and password must be 16 characters or less'}), 400
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM Users WHERE username = %s", (username,))
        if cursor.fetchone():
            return jsonify({'message': 'Username already exists'}), 400
        
        cursor.execute("SELECT MAX(uid) FROM Users")
        max_uid = cursor.fetchone()[0]
        new_uid = 1 if max_uid is None else max_uid + 1
        
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        logger.info(hashed_password)
        cursor.execute("INSERT INTO Users (uid, username, pwd) VALUES (%s, %s, %s)", (new_uid, username, hashed_password))
        conn.commit()
        
        cursor.close()
        conn.close()
        
        return jsonify({'message': 'User created successfully'}), 201
    except Exception as e:
        logger.error(f"Error in signup: {str(e)}", exc_info=True)
        return jsonify({'message': 'Signup failed', 'error': str(e)}), 500

@auth_bp.route('/login', methods=['POST'])
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
        else:
            return jsonify({'message': 'Invalid username or password'}), 401
    except Exception as e:
        logger.error(f"Error in login: {str(e)}", exc_info=True)
        return jsonify({'message': 'Login failed', 'error': str(e)}), 500

@auth_bp.route('/user/<int:user_id>', methods=['GET'])
@jwt_required()
def get_user_data(user_id):
    current_user_id = get_jwt_identity()
    if current_user_id != user_id:
        return jsonify({'message': 'Unauthorized access'}), 403

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute("SELECT username FROM Users WHERE uid = %s", (current_user_id,))
        user_data = cursor.fetchone()
        
        if not user_data:
            return jsonify({'message': 'User not found'}), 404

        cursor.execute("SELECT uid, elo, total_play_time, total_games_played, wins, losses, draws FROM userstats WHERE uid = %s", (current_user_id,))
        user_stats = cursor.fetchone()

        if user_stats:
            user_stats['total_play_time'] = str(user_stats['total_play_time'])

        cursor.execute("""
            SELECT g.gid, u1.username as player1, u2.username as player2, g.final_game_state, g.result
            FROM Games g
            JOIN Users u1 ON g.uid1 = u1.uid
            JOIN Users u2 ON g.uid2 = u2.uid
            WHERE (g.uid1 = %s OR g.uid2 = %s) AND (g.final_game_state IS NOT NULL)
            ORDER BY g.gid DESC LIMIT 10
        """, (current_user_id, current_user_id))
        match_history = cursor.fetchall()

        cursor.execute("""
            SELECT p.gid, u1.username as player1, u2.username as player2, g.final_game_state, g.result
            FROM FavouriteGames p
            JOIN Games g ON p.gid = g.gid
            JOIN Users u1 ON g.uid1 = u1.uid
            JOIN Users u2 ON g.uid2 = u2.uid
            WHERE p.uid = %s AND (g.final_game_state IS NOT NULL)
        """, (current_user_id,))
        favourite_games = cursor.fetchall()

        cursor.close()
        conn.close()

        return jsonify({
            'username': user_data['username'],
            'profilePicture': 'https://via.placeholder.com/150',
            'userStats': user_stats,
            'matchHistory': match_history,
            'favouriteGames': favourite_games
        }), 200
    except Exception as e:
        logger.error(f"Error fetching user data: {str(e)}", exc_info=True)
        return jsonify({'message': 'Failed to fetch user data'}), 500
