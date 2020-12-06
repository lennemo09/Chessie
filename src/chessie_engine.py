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

all_colors = ['w','b']

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
        return self.name

    def __str__(self):
        return self.name


class Move:
    """
    Chess (rank-file) notations:
    Ranks := Rows (1-8)
    Files := Colums (a-h)
    """
    ranks_to_rows = [{"1": 7, "2": 6, "3": 5, "4": 4,
                      "5": 3, "6": 2, "7": 1, "8": 0},
                     {"1": 0, "2": 1, "3": 2, "4": 3,
                      "5": 4, "6": 5, "7": 6, "8": 7}]

    rows_to_ranks = [{x: y for y, x in ranks_to_rows[0].items()},
                     {x: y for y, x in ranks_to_rows[1].items()}]

    files_to_cols = [{"a": 0, "b": 1, "c": 2, "d": 3,
                      "e": 4, "f": 5, "g": 6, "h": 7},
                     {"a": 7, "b": 6, "c": 5, "d": 4,
                      "e": 3, "f": 2, "g": 1, "h": 0}]

    cols_to_files = [{x: y for y, x in files_to_cols[0].items()},
                     {x: y for y, x in files_to_cols[1].items()}]



    def __init__(self,src,dst,board,player=0):
        """
        Using Move class to have convenient data storage with each move.
        """
        self.player = player # 0: white, 1: player
        self.src_row = src[0]
        self.src_col = src[1]
        self.dst_row = dst[0]
        self.dst_col = dst[1]
        self.move_hash = src[0]*1000 + src[1]*100 + dst[0]*10 + dst[1]

        self.piece = board[self.src_row,self.src_col]
        self.capture = board[self.dst_row,self.dst_col]

    def __eq__(self,other):
        """
        Checks if 2 move objects are the same
        """
        if isinstance(other, Move):
            return self.move_hash == other.move_hash

    def __repr__(self):
        return str(self.move_hash)

    def get_notation(self):
        """
        Return Rank-File notation of the move.
        """
        return self.get_tile(self.src_row,self.src_col) + self.get_tile(self.dst_row,self.dst_col)

    def get_tile(self,row,col):
        """
        Return Rank-File notation of the tile.
        """
        return self.cols_to_files[self.player][col] + self.rows_to_ranks[self.player][row]


class State:
    def __init__(self,player_view=0,size=8):
        """
        player_view: {0 = white's view; 1 = black's view}
        """
        self.board = self.create_board(player_view)
        self.size = size
        self.player_view = player_view
        self.moving_player = 0 # White moves first
        self.moves = 0 # Number of moves made so far
        self.history = [] # Keep track of moves made so far
        self.kings = [(7,3,'w'),(0,3,'b')] # Keep track of kings' coordinates for mate checks [white,black] from white's view

    def get_moving_player(self):
        self.moving_player = self.moves % 2 # Even number: White's turn, odd number: Black's turn
        if self.moving_player == 0:
            print("White's turn to move.")
        else:
            print("Black's turn to move.")
        return self.moving_player

    def get_kings(self):
        """
        Return the kings' positions (White,Black)
        """
        if self.moving_player == 0:
            assert self.kings[0][2] == 'w'
            return (self.kings[0][::2],self.kings[1][::2])
        else:
            assert self.kings[1][2] == 'w'
            return (self.kings[1][::2],self.kings[0][::2])

    def create_board(self,player_view=0):
        if player_view == 0:
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
        else:
            board = np.array([
            [Piece("w_r"),Piece("w_n"),Piece("w_b"),Piece("w_k"),Piece("w_q"),Piece("w_b"),Piece("w_n"),Piece("w_r")],
            [Piece("w_p"),Piece("w_p"),Piece("w_p"),Piece("w_p"),Piece("w_p"),Piece("w_p"),Piece("w_p"),Piece("w_p")],
            ["---","---","---","---","---","---","---","---"],
            ["---","---","---","---","---","---","---","---"],
            ["---","---","---","---","---","---","---","---"],
            ["---","---","---","---","---","---","---","---"],
            [Piece("b_p"),Piece("b_p"),Piece("b_p"),Piece("b_p"),Piece("b_p"),Piece("b_p"),Piece("b_p"),Piece("b_p")],
            [Piece("b_r"),Piece("b_n"),Piece("b_b"),Piece("b_k"),Piece("b_q"),Piece("b_b"),Piece("b_n"),Piece("b_r")]
            ])
        return board

    def move_piece(self,move):
        """
        Special moves like castling, promotions, etc. not handled.
        """
        self.board[move.src_row,move.src_col] = "---"
        self.board[move.dst_row,move.dst_col] = move.piece
        self.history.append(move) # Added move to log
        self.moves += 1
        self.moving_player = self.get_moving_player()
        self.kings.reverse()

    def undo(self):
        """
        Undo last move.
        """
        if len(self.history) > 0:
            move = self.history.pop()
            self.board[move.src_row,move.src_col] = move.piece
            self.board[move.dst_row,move.dst_col] = move.capture
            self.moves -= 1
            self.moving_player = self.get_moving_player()
            self.kings.reverse()

    def get_valid_moves(self):
        """
        Get all valid moves for the current player taking into account the opponent's possible moves in the next turn (cannot move if King is checked next turn.)
        """
        return self.get_all_moves()

    def get_all_moves(self):
        """
        Get all legal moves for the current player.
        """
        moves = []

        print("Getting moves.")

        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                piece = self.board[row,col]
                if piece != '---':
                    color = piece.color
                    type = piece.type
                    #print(color,type,self.moving_player)
                    if (color == 'w' and self.moving_player == 0) or (color == 'b' and self.moving_player == 1):
                        self.get_piece_moves(row,col,piece,moves)
                        #print(moves)
        return moves


    def get_piece_moves(self,row,col,piece,moves):
        """
        Get valid moves for a given piece.
        """
        color = piece.color
        type = piece.type

        if type == 'p': # Should be using switch cases if Python has it.
            if self.moving_player == 0: # White pawn
                if self.board[row-1,col] == "---":  # White pawn can only move up
                    moves.append(Move((row,col),(row-1,col),self.board))
                    if row == 6 and self.board[row-2,col] == "---":
                        moves.append(Move((row,col),(row-2,col),self.board))
                # White pawn capturing
                if col-1 >= 0:
                    tile = self.board[row-1,col-1]
                    if tile != "---":
                        if tile.color == 'b':
                            moves.append(Move((row,col),(row-1,col-1),self.board))
                if col+1 <= self.size-1:
                    tile = self.board[row-1,col+1]
                    if tile != "---":
                        if tile.color == 'b':
                            moves.append(Move((row,col),(row-1,col+1),self.board))

            elif self.moving_player == 1: # Black pawn
                if self.board[row+1,col] == "---":
                    moves.append(Move((row,col),(row+1,col),self.board))
                    if row == 1 and self.board[row+1,col] == "---":
                        moves.append(Move((row,col),(row+2,col),self.board))
                # Black pawn capturing
                if col-1 >= 0:
                    tile = self.board[row+1,col-1]
                    if tile != "---":
                        if tile.color == 'w':
                            moves.append(Move((row,col),(row+1,col-1),self.board))
                if col+1 <= self.size-1:
                    tile = self.board[row+1,col+1]
                    if tile != "---":
                        if tile.color == 'w':
                            moves.append(Move((row,col),(row+1,col+1),self.board))

        elif type == 'n': # Knight

            enemy = all_colors[(self.moving_player+1) % len(all_colors)]

            if row-1 >= 0 and col+2 <= self.size-1 and (self.board[row-1,col+2] == "---" or self.board[row-1,col+2].color == enemy):
                moves.append(Move((row,col),(row-1,col+2),self.board))

            if row-1 >= 0 and col-2 >= 0 and (self.board[row-1,col-2] == "---" or self.board[row-1,col-2].color == enemy):
                moves.append(Move((row,col),(row-1,col-2),self.board))

            if row-2 >= 0 and col+1 <= self.size-1 and (self.board[row-2,col+1] == "---" or self.board[row-2,col+1].color == enemy):
                moves.append(Move((row,col),(row-2,col+1),self.board))

            if row-2 >= 0 and col-1 >= 0 and (self.board[row-2,col-1] == "---" or self.board[row-2,col-1].color == enemy):
                moves.append(Move((row,col),(row-2,col-1),self.board))

            if row+1 <= self.size-1 and col+2 <= self.size-1 and (self.board[row+1,col+2] == "---" or self.board[row+1,col+2].color == enemy):
                moves.append(Move((row,col),(row+1,col+2),self.board))

            if row+1 <= self.size-1 and col-2 >= 0 and (self.board[row+1,col-2] == "---" or self.board[row+1,col-2].color == enemy):
                moves.append(Move((row,col),(row+1,col-2),self.board))

            if row+2 <= self.size-1 and col+1 <= self.size-1 and (self.board[row+2,col+1] == "---" or self.board[row+2,col+1].color == enemy):
                moves.append(Move((row,col),(row+2,col+1),self.board))

            if row+2 <= self.size-1 and col-1 >= 0 and (self.board[row+2,col-1] == "---" or self.board[row+2,col-1].color == enemy):
                moves.append(Move((row,col),(row+2,col-1),self.board))

        elif type == 'r':
            enemy = all_colors[(self.moving_player+1) % len(all_colors)]

            for new_col in range(col+1,self.size):
                if self.board[row,new_col] == '---':
                    moves.append(Move((row,col),(row,new_col),self.board))
                elif self.board[row,new_col].color == enemy:
                    moves.append(Move((row,col),(row,new_col),self.board))
                    break
                else:
                    break

            for new_col in range(col-1,-1,-1):
                if self.board[row,new_col] == '---':
                    moves.append(Move((row,col),(row,new_col),self.board))
                elif self.board[row,new_col].color == enemy:
                    moves.append(Move((row,col),(row,new_col),self.board))
                    break
                else:
                    break

            for new_row in range(row+1,self.size):
                if self.board[new_row,col] == '---':
                    moves.append(Move((row,col),(new_row,col),self.board))
                elif self.board[new_row,col].color == enemy:
                    moves.append(Move((row,col),(new_row,col),self.board))
                    break
                else:
                    break

            for new_row in range(row-1,-1,-1):
                if self.board[new_row,col] == '---':
                    moves.append(Move((row,col),(new_row,col),self.board))
                elif self.board[new_row,col].color == enemy:
                    moves.append(Move((row,col),(new_row,col),self.board))
                    break
                else:
                    break



        elif type == 'b':
            pass
        elif type == 'q':
            pass
        elif type == 'k':
            pass
