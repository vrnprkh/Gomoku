from flask import Blueprint, request, jsonify
import mysql.connector
import logging
import os
from config import Config
db_password = os.getenv('DB_PASSWORD')
players_bp = Blueprint('players', __name__)
logger = logging.getLogger(__name__)
def get_db_connection():
    try:
        conn = mysql.connector.connect(
            user="gomoku_db_admin",
            password=db_password,
            host="gomoku-database.mysql.database.azure.com",
            port=3306,
            database="prod_db",
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
        
        logger.info(f"Players fetched: {players}")
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
        # response.headers.add("Access-Control-Allow-Origin", "*")
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
