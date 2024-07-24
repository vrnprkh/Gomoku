from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
import mysql.connector
import logging
import os
from dotenv import load_dotenv
from datetime import datetime


from enum import Enum
import random
class PieceState(Enum):
    EMPTY = 0
    WHITE = 1
    BLACK = 2


class Gomoku:
    def __init__(self, size = 15) -> None:
        self.size : int = size
        self.board : list[list[PieceState]] = [[PieceState.EMPTY for _ in range(size)] for _ in range(size)]
        self.turn : PieceState = PieceState.BLACK
        self.moves : list[tuple[int,int, int]] = []

    def inBounds(self, x, y):
        return 0 <= x and x < self.size and 0 <= y and y < self.size

    def switchTurn(self):
        if self.turn == PieceState.BLACK:
            self.turn = PieceState.WHITE
        else:
            self.turn = PieceState.BLACK


    def place(self, x, y) -> bool:
        if self.board[y][x] == PieceState.EMPTY and self.turn == self.turn:
            self.board[y][x] = self.turn
            self.switchTurn()
            moveTime = random.random() * 10 + 3
            self.moves.append((x, y, moveTime))
            
            return True
        return False
    
    def checkDraw(self):
        for layer in self.board:
            for e in layer:
                if e == PieceState.EMPTY:
                    return False
        return True
    
    def checkGameState(self):
        # y, x offsets
        offsets = [(0,1), (1,0), (1, 1), (1, -1)]
        for y in range(self.size):
            for x in range(self.size):
                for offset in offsets:
                    checks = [(y + i * offset[0], x + i * offset[1]) for i in range(5)]
                    pieceColor = None
                    for check in checks:
                        if self.inBounds(check[1],check[0]):
                            piece = self.board[check[1]][check[0]]
                            if piece == PieceState.EMPTY:
                                pieceColor = None
                                break
                            if pieceColor == None:
                                pieceColor = piece
                            else:
                                if pieceColor != piece:
                                    pieceColor = None
                                    break
                        else:
                            pieceColor = None
                            break
                    if pieceColor == None:
                        pass
                    else:
                        # this person has won
                        return pieceColor
        return None

    def draw(self):
        s = ""
        for layer in self.board:
            for e in layer: 
                if e == PieceState.EMPTY:
                    s += "."
                elif e == PieceState.WHITE:
                    s += "O"
                else:
                    s += "X"
            s+= "\n"
        return s






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
        WHERE g.gid = %s and (g.uid1 = %s or g.uid2 = %s)
        """

        cursor.execute(queryGame, [gid, current_user_id, current_user_id])
        game = cursor.fetchone()
        if game == None:
            # user is not in this game
            cursor.close()
            conn.close()
            return jsonify(), 500
        if game["uid2"] == None:
            return jsonify({"turn" : False, "started" : False, "moves" : [], "gameOver" : False})
        
        
        isPlayerOne = current_user_id == game["uid1"]
        logger.info(game["uid1"])
        logger.info(current_user_id)
        logger.info(isPlayerOne)
        queryMoves = """
        SELECT gid, move_number, coordinateX, coordinateY
        FROM DetailedMoves
        WHERE gid = %s
        """

        cursor.execute(queryMoves, [gid])
        moves = cursor.fetchall()
      
        turn = (len(moves) % 2) == (not isPlayerOne)

        # if the game is over, it is no longer this players turn
        queryGameOver = """
        SELECT *
        FROM Lobbies
        WHERE gid = %s
        """


        cursor.execute(queryGameOver, [gid])

        gameOver = False
        if cursor.fetchone() == None:
            turn = False
            gameOver = True


        cursor.close()
        conn.close()
        return jsonify({"turn" : turn , 
                        "started" : True,
                        "moves" : moves,
                        "gameOver" : gameOver,
                        })
    


    except Exception as e:
        logger.error(f"Error fetching turn: {str(e)}", exc_info=True)
        return jsonify({'message': 'Failed to fetch friend turn'}), 500

@in_game_bp.route('/make-move', methods=['POST'])
@jwt_required()
def make_move():
    try: 
        current_user_id = get_jwt_identity()
        gid = request.json.get('gid')
        x = int(request.json.get('x'))
        y = int(request.json.get('y'))

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True, buffered=True)

        queryGame = """
        Select *
        FROM Games g, Lobbies l
        WHERE g.gid = %s and l.gid = %s
        """

        cursor.execute(queryGame, [gid, gid])
        game = cursor.fetchone()
        if game == None:
            # user is not in this game
            cursor.close()
            conn.close()
            return jsonify("Game Error"), 500
        if game["uid2"] == None:
            cursor.close()
            conn.close()
            return jsonify(), 500

        if game["uid1"] != current_user_id and game["uid2"] != current_user_id:
            cursor.close()
            conn.close()
            return jsonify(), 500
        
        queryMoves = """
        SELECT *
        FROM DetailedMoves
        WHERE gid = %s
        """

        cursor.execute(queryMoves, [gid])
        moves = cursor.fetchall()


        isPlayerOne = current_user_id == game["uid1"]
        # if it is not this players turn
        if not (len(moves) % 2) ==  (not isPlayerOne):
            cursor.close()
            conn.close()
            return jsonify({"res" : "NOT YOUR TURN >:("}), 502


        # we now can make the move
        b = Gomoku()
        for move in moves:
            b.place(move["coordinateX"], move["coordinateY"])

        # cannot place this piece
        if not b.place(x, y):
            cursor.close()
            conn.close()
            return jsonify(), 500

        # TODO, fix move time please 
        queryAddMove = """
        INSERT INTO DetailedMoves(gid, move_number, coordinateX, coordinateY, moveTime)
        VALUES(%s, %s, %s, %s, 10)
        """

        cursor.execute(queryAddMove, [gid, len(moves), x, y])
        conn.commit()
    



        gameState = b.checkGameState()
        if gameState == None and not b.checkDraw():
            # game not over
            cursor.close()
            conn.close()

            return jsonify()
        
        # get string to push to db
        drawStr = ""
        for layer in b.board:
            for e in layer:
                if e == PieceState.BLACK:
                    drawStr += "O"
                elif e == PieceState.WHITE:
                    drawStr += "X"
                else:
                    drawStr += '.'
        winner = None
        if gameState == PieceState.BLACK:
            winner = 0
        elif gameState == PieceState.WHITE:
            winner = 1
        else:
            winner = 2

        #insert here
        updateGame = """
        UPDATE games
        SET final_game_state = %s,
            result = %s
        WHERE gid = %s;
        """

        cursor.execute(updateGame, [drawStr, winner, gid])

        #remove lobby
        removeLobby = """
        DELETE FROM Lobbies
        WHERE gid = %s
        """
        cursor.execute(removeLobby, [gid])
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify()



        
        
    except Exception as e:
        logger.info(f"Error making turn: {str(e)}", exc_info=True)
        return jsonify({'message': 'Failed to make turn'}), 500


