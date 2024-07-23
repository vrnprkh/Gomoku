from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
import mysql.connector
from dotenv import load_dotenv
import os
import logging
from config import Config

load_dotenv()

db_user = os.getenv("DB_USER")
db_password = os.getenv('DB_PASSWORD')
db_host = os.getenv("DB_HOST")
db_name = os.getenv("DB_NAME")

detailed_moves_bp = Blueprint('detailed_moves', __name__)
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

@detailed_moves_bp.route('/detailed_moves', methods=['GET'])
@jwt_required()
def join_lobby():
    try:
        current_user_id = get_jwt_identity()
        gid = request.args.get('gid')

        logger.info(f"Finding detailed moves for {gid}")

        conn = get_db_connection()
        cursor = conn.cursor()

        # Get detailed move info given gid
        query = """
        SELECT move_number, coordinateX, coordinateY
        FROM DetailedMoves
        WHERE gid = %s
        """
        cursor.execute(query, ([gid]))
        moveCount = cursor.fetchall()

        cursor.close()
        conn.close()

        logger.debug(f"Successfully fetched detailed moves: {moveCount}")
        return jsonify(moveCount)
    
    except Exception as e:
        logger.error(f"Error fetching detailed moves: {str(e)}", exc_info=True)
        return jsonify({'message': 'Failed to fetch detailed moves'}), 500

