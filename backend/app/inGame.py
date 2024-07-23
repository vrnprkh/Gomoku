from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
import mysql.connector
import logging
import os
from dotenv import load_dotenv
from datetime import datetime



load_dotenv()


db_user = os.getenv("DB_USER")
db_password = os.getenv('DB_PASSWORD')
db_host = os.getenv("DB_HOST")
db_name = os.getenv("DB_NAME")


in_game_bp = Blueprint('ingame', __name__)
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




@in_game_bp.route('/poll-turn', methods=['GET'])
@jwt_required()
def poll_turn():
    try:
        current_user_id = get_jwt_identity()
        gid = request.args.get('gid')

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True, buffered=True)

        queryGame = """
        Select *
        FROM Games g
        WHERE g.gid = %s
        """

        cursor.execute(queryGame, [gid])
        game = cursor.fetchone()
        if game == None:
            # user is not in this game
            cursor.close()
            conn.close()
            return jsonify(), 500
        if game["uid2"] == None:
            return jsonify({"turn" : False})
        
        
        isPlayerOne = current_user_id == game["uid1"]

        queryMoves = """
        SELECT move_number
        FROM DetailedMoves
        WHERE gid = %s
        """

        cursor.execute(queryMoves, [gid])
        moves = cursor.fetchall()
        cursor.close()
        conn.close()


        return jsonify({"turn" : bool((len(moves) % 2) ==  (not isPlayerOne))})
    except Exception as e:
        logger.error(f"Error fetching turn: {str(e)}", exc_info=True)
        return jsonify({'message': 'Failed to fetch friend turn'}), 500
