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
            return True
        return False
    
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






def generateRandomGame(size = 15):
    game = Gomoku(size)

    legalMoves = [(y, x) for y in range(size) for x in range(size)]

    while game.checkGameState() == None and len(legalMoves) > 0:
        moveNum = random.randint(0, len(legalMoves) - 1)
        move = legalMoves[moveNum]
        legalMoves.pop(moveNum)
        game.place(move[0], move[1])
    
    return game


