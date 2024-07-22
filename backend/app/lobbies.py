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

        logger.info(f"Current user ID: {current_user_id}, Search: {search}")

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # Simplified query to ensure basic functionality
        query = """
        SELECT l.gid, l.uid1, users.username
        FROM Lobbies l JOIN users ON l.uid1 = users.uid
        WHERE l.open = '1';
        """
        
        cursor.execute(query, ())
        lobbies_details = cursor.fetchall()
        cursor.close()
        conn.close()

        logger.debug(f"Open lobbies fetched: {lobbies_details}")
        return jsonify(lobbies_details)
    except Exception as e:
        logger.error(f"Error fetching lobbies: {str(e)}", exc_info=True)
        return jsonify({'message': 'Failed to fetch lobbies'}), 500
