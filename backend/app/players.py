from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
import mysql.connector
import logging
import os
from config import Config
from dotenv import load_dotenv

load_dotenv()

db_user = os.getenv("DB_USER")
db_password = os.getenv('DB_PASSWORD')
db_host = os.getenv("DB_HOST")
db_name = os.getenv("DB_NAME")

players_bp = Blueprint('players', __name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
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

@players_bp.route('/players', methods=['GET'])
def get_players():
    try:
        search = request.args.get('search', '')
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        if search:
            query = "SELECT uid, username FROM Users WHERE username REGEXP %s"
            cursor.execute(query, (search,))
        else:
            query = "SELECT uid, username FROM Users"
            cursor.execute(query)
        
        players = cursor.fetchall()
        cursor.close()
        conn.close()
        
        # logger.info(f"Players fetched: {players}")
        response = jsonify(players)
        return jsonify(players)
    except Exception as e:
        logger.error(f"Error fetching players: {str(e)}", exc_info=True)
        return jsonify({'message': 'Failed to fetch players'}), 500

@players_bp.route('/player-stats/<int:uid>', methods=['GET'])
def get_player_stats(uid):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM User_Stats WHERE uid = %s"
        cursor.execute(query, (uid,))
        player_stats = cursor.fetchone()
        cursor.close()
        conn.close()
        
        if not player_stats:
            return jsonify({'message': 'User stats not found'}), 404
        
        response = jsonify(player_stats)
        return response
    except Exception as e:
        logger.error(f"Error fetching player stats: {str(e)}", exc_info=True)
        return jsonify({'message': 'Failed to fetch player stats'}), 500

@players_bp.route('/games/<int:uid>', methods=['GET'])
def get_games(uid):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM Games WHERE uid1 = %s OR uid2 = %s"
        cursor.execute(query, (uid, uid))
        games = cursor.fetchall()
        cursor.close()
        conn.close()
        
        return jsonify(games)
    except Exception as e:
        logger.error(f"Error fetching games: {str(e)}", exc_info=True)
        return jsonify({'message': 'Failed to fetch games'}), 500

@players_bp.route('/favourite', methods=['POST'])
@jwt_required()
def add_to_favourites():
    try:
        user_id = get_jwt_identity()
        gid = request.json.get('gid')

        conn = get_db_connection()
        cursor = conn.cursor()

        query = "INSERT INTO FavouriteGames (uid, gid) VALUES (%s, %s)"
        cursor.execute(query, (user_id, gid))
        logger.info(f"Adding to favourites: user_id={user_id}, gid={gid}")
        conn.commit()
        
        cursor.close()
        conn.close()
        
        return jsonify({'message': 'Game added to favourites'}), 201
    except Exception as e:
        logger.error(f"Error adding to favourites: {str(e)}", exc_info=True)
        return jsonify({'message': 'Failed to add to favourites'}), 500

@players_bp.route('/favourite', methods=['DELETE'])
@jwt_required()
def remove_from_favourites():
    try:
        user_id = get_jwt_identity()
        gid = request.json.get('gid')

        conn = get_db_connection()
        cursor = conn.cursor()

        query = "DELETE FROM prod_db.FavouriteGames WHERE uid = %s AND gid = %s"
        cursor.execute(query, (user_id, gid))
        conn.commit()
        
        cursor.close()
        conn.close()
        
        return jsonify({'message': 'Game removed from favourites'}), 200
    except Exception as e:
        logger.error(f"Error removing from favourites: {str(e)}", exc_info=True)
        return jsonify({'message': 'Failed to remove from favourites'}), 500
