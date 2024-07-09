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


friends_bp = Blueprint('friends', __name__)
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

@friends_bp.route('/friends', methods=['GET'])
@jwt_required()
def get_friends():
    try:
        current_user_id = get_jwt_identity()
        search = request.args.get('search', '')

        logger.info(f"Current user ID: {current_user_id}, Search: {search}")

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # Simplified query to ensure basic functionality
        query = """
        SELECT
            CASE
                WHEN f.uid1 = %s THEN f.uid2
                WHEN f.uid2 = %s THEN f.uid1
            END AS friend_uid, 
            CASE
                WHEN f.uid1 = %s THEN u2.username
                WHEN f.uid2 = %s THEN u1.username
            END AS friend_username
        FROM
            Friends f
        JOIN
            Users u1 ON f.uid1 = u1.uid
        JOIN 
            Users u2 ON f.uid2 = u2.uid
        WHERE 
            f.uid1 = %s OR f.uid2 = %s
        """
        
        cursor.execute(query, (
            current_user_id, current_user_id, 
            current_user_id, current_user_id, 
            current_user_id, current_user_id
        ))
        friends_details = cursor.fetchall()
        cursor.close()
        conn.close()

        logger.info(f"Friends fetched for user {current_user_id}: {friends_details}")
        return jsonify(friends_details)
    except Exception as e:
        logger.error(f"Error fetching friends: {str(e)}", exc_info=True)
        return jsonify({'message': 'Failed to fetch friends'}), 500
