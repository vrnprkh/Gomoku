from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
import mysql.connector
import logging
import os
from dotenv import load_dotenv

load_dotenv()

db_user = os.getenv("DB_USER")
db_password = os.getenv('DB_PASSWORD')
db_host = os.getenv("DB_HOST")
db_name = os.getenv("DB_NAME")

lobbies_bp = Blueprint('lobbies', __name__)
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

@lobbies_bp.route('/lobbies', methods=['GET'])
@jwt_required()
def get_lobbies():
    try:
        current_user_id = get_jwt_identity()
        search = request.args.get('search', '')
        show_friends_only = request.args.get('show_friends_only', 'false').lower() == 'true'

        logger.info(f"Current user ID: {current_user_id}, Search: {search}, Show friends only: {show_friends_only}")

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        if show_friends_only:
            query = """
            SELECT l.gid, l.uid1, u.username
            FROM Lobbies l
            JOIN Users u ON l.uid1 = u.uid
            JOIN Friends f ON ((f.uid1 = %s AND f.uid2 = l.uid1) OR (f.uid2 = %s AND f.uid1 = l.uid1))
            WHERE l.open = '1';
            """
            cursor.execute(query, (current_user_id, current_user_id))
        else:
            query = """
            SELECT l.gid, l.uid1, u.username
            FROM Lobbies l
            JOIN Users u ON l.uid1 = u.uid
            WHERE l.open = '1';
            """
            cursor.execute(query)

        lobbies_details = cursor.fetchall()
        cursor.close()
        conn.close()

        logger.debug(f"Lobbies fetched: {lobbies_details}")
        return jsonify(lobbies_details)
    except Exception as e:
        logger.error(f"Error fetching lobbies: {str(e)}", exc_info=True)
        return jsonify({'message': 'Failed to fetch lobbies'}), 500

@lobbies_bp.route('/self-lobbies', methods=['GET'])
@jwt_required()
def get_self_lobbies():
    try:
        current_user_id = get_jwt_identity()

        logger.info(f"Current user ID: {current_user_id}, getting self-lobbies")

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        query = """
        SELECT l.gid, l.uid1, l.uid2, u1.username AS username1, u2.username AS username2
        FROM Lobbies l
        JOIN Users u1 ON (l.uid1 = u1.uid)
        JOIN Users u2 ON (l.uid2 = u2.uid)
        WHERE (l.uid1 = %s OR l.uid2 = %s)
        """
        cursor.execute(query, [current_user_id, current_user_id])

        lobbies_details = cursor.fetchall()
        cursor.close()
        conn.close()

        logger.debug(f"Lobbies fetched: {lobbies_details}")
        return jsonify(lobbies_details)
    except Exception as e:
        logger.error(f"Error fetching lobbies: {str(e)}", exc_info=True)
        return jsonify({'message': 'Failed to fetch lobbies'}), 500

@lobbies_bp.route('/join_lobby', methods=['POST'])
@jwt_required()
def join_lobby():
    try:
        current_user_id = get_jwt_identity()
        gid = request.json.get('gid')

        logger.info(f"User {current_user_id} joining lobby {gid}")

        conn = get_db_connection()
        cursor = conn.cursor()

        # Update the lobby to set uid2 and close it
        query = """
        UPDATE Lobbies 
        SET uid2 = %s, open = '0'
        WHERE gid = %s AND open = '1'
        """
        cursor.execute(query, (current_user_id, gid))
        conn.commit()

        cursor.close()
        conn.close()

        if cursor.rowcount == 0:
            return jsonify({'message': 'Failed to join lobby. It might be already closed.'}), 400
        
        return jsonify({'message': 'Successfully joined the lobby'}), 200
    except Exception as e:
        logger.error(f"Error joining lobby: {str(e)}", exc_info=True)
        return jsonify({'message': 'Failed to join lobby'}), 500

@lobbies_bp.route('/create_lobby', methods=['POST'])
@jwt_required()
def create_lobby():
    try:
        current_user_id = get_jwt_identity()

        logger.info(f"Creating a new lobby")

        conn = get_db_connection()
        cursor = conn.cursor()

        # Generate new gid
        getMaxGIDQuery = """
        SELECT MAX(gid)
        FROM Games
        """
        cursor.execute(getMaxGIDQuery)
        newGID = cursor.fetchone()[0] + 1
        
        # Create new game (a new row in the Lobbies table will automatically be created with triggers)
        createLobbyQuery = """
        INSERT INTO Games(gid, uid1, uid2, final_game_state, result, start_time)
        VALUES(%s, %s, NULL, NULL, NULL, NULL);
        """
        cursor.execute(createLobbyQuery, (newGID, current_user_id))
        conn.commit()
        
        cursor.close()
        conn.close()

        logger.debug(f"Successfully created new lobby (gid: {newGID})")
        return jsonify(newGID)
    
    except Exception as e:
        logger.error(f"Error creating a new lobby: {str(e)}", exc_info=True)
        return jsonify({'message': 'Failed to create a new lobby'}), 500
    

