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


friends_bp = Blueprint('friends', __name__)
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

@friends_bp.route('/friends', methods=['GET'])
@jwt_required()
def get_friends():
    try:
        current_user_id = get_jwt_identity()
        search = request.args.get('search', '')

        # logger.info(f"Current user ID: {current_user_id}, Search: {search}")

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




@friends_bp.route('/friend-requests', methods=['GET'])
@jwt_required()
def get_friend_requests():
    try:
        current_user_id = get_jwt_identity()

        logger.info(f"Current user ID: {current_user_id}")

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)


        query = """
        SELECT u.username, fr.to_uid, fr.from_uid
        FROM FriendRequests fr, Users u
        WHERE fr.to_uid = %s AND u.uid = fr.from_uid
        """
        
        cursor.execute(query, [current_user_id])
        friends_details = cursor.fetchall()
        cursor.close()
        conn.close()

        logger.info(f"Friends fetched for user {current_user_id}: {friends_details}")
        return jsonify(friends_details)
    except Exception as e:
        logger.error(f"Error fetching friend requests: {str(e)}", exc_info=True)
        return jsonify({'message': 'Failed to fetch friend requests'}), 500


@friends_bp.route('/accept-request', methods=['POST'])
@jwt_required()
def accept_friend_request():
    try:
        current_user_id = get_jwt_identity()
        from_uid = request.json.get('from_uid')
        logger.info(f"Current user ID: {current_user_id}")
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)


        queryinsert = """
        INSERT INTO friends (uid1, uid2)
        SELECT from_uid, to_uid
        FROM friendrequests
        WHERE from_uid = %s AND to_uid = %s;
        """
        querydelete = """
        DELETE FROM friendrequests
        WHERE from_uid = %s AND to_uid = %s;
        """
        
        cursor.execute(queryinsert, [from_uid, current_user_id])
        cursor.execute(querydelete, [from_uid, current_user_id])

        conn.commit()
        cursor.close()
        conn.close()

        logger.info(f"Friends inserted {current_user_id}: {from_uid}")
        return jsonify()
    except Exception as e:
        logger.error(f"Error accepting friend request: {str(e)}", exc_info=True)
        return jsonify({'message': 'accept friend request'}), 500


@friends_bp.route('/deny-request', methods=['POST'])
@jwt_required()
def deny_friend_request():
    try:
        current_user_id = get_jwt_identity()
        from_uid = request.json.get('from_uid')
        logger.info(f"Current user ID: {current_user_id}")
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        querydelete = """
        DELETE FROM friendrequests
        WHERE from_uid = %s AND to_uid = %s;
        """
        
        cursor.execute(querydelete, [from_uid, current_user_id])

        conn.commit()
        cursor.close()
        conn.close()

        logger.info(f"Friends inserted {current_user_id}: {from_uid}")
        return jsonify()
    except Exception as e:
        logger.error(f"Error accepting friend request: {str(e)}", exc_info=True)
        return jsonify({'message': 'accept friend request'}), 500



@friends_bp.route('/send-request', methods=['POST'])
@jwt_required()
def send_friend_request():
    try:
        from_uid = get_jwt_identity()
        to_uid = request.json.get('to_uid')
        
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        #check uid not same
        if (from_uid == to_uid):
            cursor.close()
            conn.close()
            return jsonify()
        # check if in friends
        querycheckfriends = """
        SELECT * 
        FROM Friends f 
        WHERE (f.uid1 = %s and f.uid2 = %s) or (f.uid1 = %s and f.uid2 = %s)
        """
        cursor.execute(querycheckfriends, [to_uid, from_uid, from_uid, to_uid])
        if cursor.fetchone() != None:
            cursor.close()
            conn.close()
            return jsonify()
        
        # check if in friend requests
        querycheckrequests = """
        SELECT *
        FROM FriendRequests fr
        WHERE fr.from_uid = %s and fr.to_uid = %s
        """
        cursor.execute(querycheckrequests, [from_uid, to_uid])
        if cursor.fetchone() != None:
            cursor.close()
            conn.close()
            return jsonify()
        
        # create
        querycreaterequest = """
        INSERT INTO FriendRequests (from_uid, to_uid, requestTime, status)
        VALUES (%s, %s, %s, %s)
        
        """
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute(querycreaterequest, [from_uid, to_uid, timestamp, 1])
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify()



    except Exception as e:
        logger.error(f"Error accepting friend request: {str(e)}", exc_info=True)
        return jsonify({'message': 'accept friend request failed'}), 500