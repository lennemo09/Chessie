"""
ENGINE TO PROCESS CHESSIE'S STATES AND GAME RULES.
"""
import numpy as np

pieces_name = {
    "b_b": "Black Bishop",
    "b_k": "Black King",
    "b_n": "Black Knight",
    "b_p": "Black Pawn",
    "b_q": "Black Queen",
    "b_r": "Black Rook",
    "w_b": "White Bishop",
    "w_k": "White King",
    "w_n": "White Knight",
    "w_p": "White Pawn",
    "w_q": "White Queen",
    "w_r": "White Rook"
}


class Piece:
    def __init__(self,type):
        self.type = type
        self.name = pieces_name[type]
        self.sprite = self.get_sprite()

    def get_sprite(self):
        addr = "/sprites/pieces/{}.png".format(self.type)
        return addr

    def __repr__(self):
        return self.type

    def __str__(self):
        return self.type

class State:
    def __init__(self,player_view=0):
        """
        player_view: {0 = white's view; 1 = black's view}
        """
        self.board = self.create_board(player_view)
        self.player_view = player_view

    def create_board(self,player_view=0):
        board = np.array([
        [Piece("b_r"),Piece("b_n"),Piece("b_b"),Piece("b_k"),Piece("b_q"),Piece("b_b"),Piece("b_n"),Piece("b_r")],
        [Piece("b_p"),Piece("b_p"),Piece("b_p"),Piece("b_p"),Piece("b_p"),Piece("b_p"),Piece("b_p"),Piece("b_p")],
        ["---","---","---","---","---","---","---","---"],
        ["---","---","---","---","---","---","---","---"],
        ["---","---","---","---","---","---","---","---"],
        ["---","---","---","---","---","---","---","---"],
        [Piece("w_p"),Piece("w_p"),Piece("w_p"),Piece("w_p"),Piece("w_p"),Piece("w_p"),Piece("w_p"),Piece("w_p")],
        [Piece("w_r"),Piece("w_n"),Piece("w_b"),Piece("w_k"),Piece("w_q"),Piece("w_b"),Piece("w_n"),Piece("w_r")]
        ])
        return board
