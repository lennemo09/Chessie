"""
ENGINE TO PROCESS CHESSIE'S STATES AND GAME RULES.
"""
import numpy as np

pieces_full_names = {
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

pieces_names = ["b_b", "b_k", "b_n", "b_p", "b_q", "b_r", "w_b", "w_k", "w_n", "w_p", "w_q", "w_r"]

pieces_types = ["b","k","n","p","q","r"]

class Piece:
    def __init__(self,name):
        if name not in pieces_names:
            raise Exception("Invalid piece name.")

        self.name = name

        self.color = self.get_color(name)
        self.type = self.get_type(name)

        self.full_name = pieces_full_names[name]
        self.sprite = self.get_sprite()

    def get_color(self,name):
        if name[0] == 'w':
            color = 'w'
            return color
        elif name[0] == 'b':
            color = 'b'
            return color
        else:
            raise Exception("Invalid color.")

    def get_type(self,name):
        if len(name) < 3:
            return Exception("Invalid name.")
        type = name[2]
        if type not in pieces_types:
            raise Exception("Invalid type.")
        return type

    def get_sprite(self):
        addr = "../sprites/pieces/{}.png".format(self.type)
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
        self.moving_player = 0 # White moves first
        self.moves = 0 # Number of moves made so far
        self.history = [] # Keep track of moves made so far

    def moving_player(self):
        self.moving_player = moves % 2 # Even number: White's turn, odd number: Black's turn

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
