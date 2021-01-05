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

        if (self.piece != '---') and ((self.piece.type == 'p' and self.piece.color == 'w' and self.dst_row == 0) or (self.piece.type == 'p' and self.piece.color == 'b' and self.dst_row == 7)):
            self.promotion = True
        else:
            self.promotion = False

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
        self.kings = [(7,4),(0,4)] # Keep track of kings' coordinates for mate checks [white,black] from white's view

        self.pins = []
        self.checks = []
        self.checked = [False,False]

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
        return self.kings

    def get_enemy_king(self):
        return self.kings[(self.moving_player+1) % len(self.kings)]

    def get_my_king(self):
        return self.kings[(self.moving_player)]

    def create_board(self,player_view=0):
        if player_view == 0:
            board = np.array([
            [Piece("b_r"),Piece("b_n"),Piece("b_b"),Piece("b_q"),Piece("b_k"),Piece("b_b"),Piece("b_n"),Piece("b_r")],
            [Piece("b_p"),Piece("b_p"),Piece("b_p"),Piece("b_p"),Piece("b_p"),Piece("b_p"),Piece("b_p"),Piece("b_p")],
            ["---","---","---","---","---","---","---","---"],
            ["---","---","---","---","---","---","---","---"],
            ["---","---","---","---","---","---","---","---"],
            ["---","---","---","---","---","---","---","---"],
            [Piece("w_p"),Piece("w_p"),Piece("w_p"),Piece("w_p"),Piece("w_p"),Piece("w_p"),Piece("w_p"),Piece("w_p")],
            [Piece("w_r"),Piece("w_n"),Piece("w_b"),Piece("w_q"),Piece("w_k"),Piece("w_b"),Piece("w_n"),Piece("w_r")]
            ])
        else:
            board = np.array([
            [Piece("w_r"),Piece("w_n"),Piece("w_b"),Piece("w_q"),Piece("w_k"),Piece("w_b"),Piece("w_n"),Piece("w_r")],
            [Piece("w_p"),Piece("w_p"),Piece("w_p"),Piece("w_p"),Piece("w_p"),Piece("w_p"),Piece("w_p"),Piece("w_p")],
            ["---","---","---","---","---","---","---","---"],
            ["---","---","---","---","---","---","---","---"],
            ["---","---","---","---","---","---","---","---"],
            ["---","---","---","---","---","---","---","---"],
            [Piece("b_p"),Piece("b_p"),Piece("b_p"),Piece("b_p"),Piece("b_p"),Piece("b_p"),Piece("b_p"),Piece("b_p")],
            [Piece("b_r"),Piece("b_n"),Piece("b_b"),Piece("b_q"),Piece("b_k"),Piece("b_b"),Piece("b_n"),Piece("b_r")]
            ])
        return board

    def move_piece(self,move):
        """
        Special moves like castling, promotions, etc. not handled.
        """
        self.board[move.src_row,move.src_col] = "---"
        self.board[move.dst_row,move.dst_col] = move.piece
        self.history.append(move) # Added move to log

        if move.piece.type == 'k':
            self.kings[(self.moving_player) % len(self.kings)] = (move.dst_row,move.dst_col)

        self.moves += 1
        self.moving_player = self.get_moving_player()

        if move.promotion:
            self.board[move.dst_row,move.dst_col] = Piece(move.piece.color + '_q')

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

            if move.piece.type == 'k':
                self.kings[(self.moving_player) % len(self.kings)] = (move.src_row,move.src_col)

    def get_valid_moves(self):
        """
        Get all valid moves for the current player taking into account the opponent's possible moves in the next turn (cannot move if King is checked next turn.)
        """
        moves = []
        self.checked[self.moving_player], self.pins, self.checks = self.get_pins_and_checks()

        #print("Pins:",self.pins)
        king_row, king_col = self.get_my_king()
        king = self.board[king_row,king_col]

        if self.checked[self.moving_player]:
            #print("Is checked.")
            if len(self.checks) == 1: # 1 checked, we can block or dodge
                moves = self.get_all_moves()

                check = self.checks[0]
                check_row = check[0]
                check_col = check[1]

                check_piece = self.board[check_row,check_col]

                valid_tiles = []

                if check_piece.type == 'n':
                    valid_tiles = [(check_row, check_col)] # Knight check, can't block only capture
                else:
                    for i in range(1,8):
                        valid_tile = (king_row + check[2]*i, king_col + check[3]*i)
                        valid_tiles.append(valid_tile)

                        if valid_tile[0] == check_row and valid_tile[1] == check_col:
                            break

                # Remove unsafe moves
                for i in range(len(moves)-1,-1,-1):
                    if moves[i].piece.type != 'k':
                        if not (moves[i].dst_row, moves[i].dst_col) in valid_tiles:
                            moves.remove(moves[i])
            else:
                self.get_piece_moves(king_row,king_col,king,moves,'k')
        else:
            moves = self.get_all_moves()

        return moves

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

    def get_piece_moves(self,row,col,piece,moves,override=None):
        """
        Get valid moves for a given piece.
        """
        color = piece.color
        if override is None:
            type = piece.type
        else:
            type = override # Override is used by the queens to get (bishops && rooks)-like moves

        if type == 'p': # Should be using switch cases if Python has it.
            piece_pinned = False
            pin_direction = ()

            for i in range(len(self.pins)-1,-1,-1):
                if self.pins[i][0] == row and self.pins[i][1] == col:
                    piece_pinned = True
                    pin_direction = (self.pins[i][2], self.pins[i][3])
                    self.pins.remove(self.pins[i])
                    break

            if self.moving_player == 0: # White pawn
                if self.board[row-1,col] == "---":  # White pawn can only move up
                    if not piece_pinned or pin_direction == (-1,0):
                        moves.append(Move((row,col),(row-1,col),self.board))
                        if row == 6 and self.board[row-2,col] == "---":
                            moves.append(Move((row,col),(row-2,col),self.board))
                # White pawn capturing
                if col-1 >= 0:
                    if not piece_pinned or pin_direction == (-1,-1):
                        tile = self.board[row-1,col-1]
                        if tile != "---":
                            if tile.color == 'b':
                                moves.append(Move((row,col),(row-1,col-1),self.board))
                if col+1 <= self.size-1:
                    if not piece_pinned or pin_direction == (-1,1):
                        tile = self.board[row-1,col+1]
                        if tile != "---":
                            if tile.color == 'b':
                                moves.append(Move((row,col),(row-1,col+1),self.board))

            elif self.moving_player == 1: # Black pawn
                if self.board[row+1,col] == "---":
                    if not piece_pinned or pin_direction == (1,0):
                        moves.append(Move((row,col),(row+1,col),self.board))
                        if row == 1 and self.board[row+2,col] == "---":
                            moves.append(Move((row,col),(row+2,col),self.board))
                # Black pawn capturing
                if col-1 >= 0:
                    if not piece_pinned or pin_direction == (1,-1):
                        tile = self.board[row+1,col-1]
                        if tile != "---":
                            if tile.color == 'w':
                                moves.append(Move((row,col),(row+1,col-1),self.board))
                if col+1 <= self.size-1:
                    if not piece_pinned or pin_direction == (1,1):
                        tile = self.board[row+1,col+1]
                        if tile != "---":
                            if tile.color == 'w':
                                moves.append(Move((row,col),(row+1,col+1),self.board))

        elif type == 'n': # Knight
            piece_pinned = False
            pin_direction = ()

            for i in range(len(self.pins)-1,-1,-1):
                if self.pins[i][0] == row and self.pins[i][1] == col:
                    piece_pinned = True
                    pin_direction = (self.pins[i][2],self.pins[i][3])
                    self.pins.remove(self.pins[i])
                    break

            enemy = all_colors[(self.moving_player+1) % len(all_colors)]

            L_shape = [(row-1,col+2),(row-1,col-2),(row-2,col+1),(row-2,col-1),(row+1,col+2),(row+1,col-2),(row+2,col+1),(row+2,col-1)]

            for tile in L_shape:
                new_row = tile[0]
                new_col = tile[1]

                if (new_row in range(self.size)) and (new_col in range(self.size)):
                    if not piece_pinned:
                        if self.board[new_row,new_col] == '---':
                            moves.append(Move((row,col),(new_row,new_col),self.board))
                        elif self.board[new_row,new_col].color == enemy:
                            moves.append(Move((row,col),(new_row,new_col),self.board))

        elif type == 'r': # Rooks
            enemy = all_colors[(self.moving_player+1) % len(all_colors)]

            piece_pinned = False
            pin_direction = ()

            for i in range(len(self.pins)-1,-1,-1):
                if self.pins[i][0] == row and self.pins[i][1] == col:
                    piece_pinned = True
                    pin_direction = (self.pins[i][2],self.pins[i][3])
                    if self.board[row,col].type != 'q': # Can't remove queen from pin on rook move
                        self.pins.remove(self.pins[i])
                        break

            directions = [(-1,0),(0,-1),(1,0),(0,1)]

            for new_col in range(col+1,self.size):
                if not piece_pinned or pin_direction == (0,1):
                    if self.board[row,new_col] == '---':
                        moves.append(Move((row,col),(row,new_col),self.board))
                    elif self.board[row,new_col].color == enemy:
                        moves.append(Move((row,col),(row,new_col),self.board))
                        break
                    else:
                        break

            for new_col in range(col-1,-1,-1):
                if not piece_pinned or pin_direction == (0,-1):
                    if self.board[row,new_col] == '---':
                        moves.append(Move((row,col),(row,new_col),self.board))
                    elif self.board[row,new_col].color == enemy:
                        moves.append(Move((row,col),(row,new_col),self.board))
                        break
                    else:
                        break

            for new_row in range(row+1,self.size):
                if not piece_pinned or pin_direction == (1,0):
                    if self.board[new_row,col] == '---':
                        moves.append(Move((row,col),(new_row,col),self.board))
                    elif self.board[new_row,col].color == enemy:
                        moves.append(Move((row,col),(new_row,col),self.board))
                        break
                    else:
                        break

            for new_row in range(row-1,-1,-1):
                if not piece_pinned or pin_direction == (-1,0):
                    if self.board[new_row,col] == '---':
                        moves.append(Move((row,col),(new_row,col),self.board))
                    elif self.board[new_row,col].color == enemy:
                        moves.append(Move((row,col),(new_row,col),self.board))
                        break
                    else:
                        break

        elif type == 'b':   # Bishops
            piece_pinned = False
            pin_direction = ()

            for i in range(len(self.pins)-1,-1,-1):
                if self.pins[i][0] == row and self.pins[i][1] == col:
                    piece_pinned = True
                    pin_direction = (self.pins[i][2],self.pins[i][3])
                    self.pins.remove(self.pins[i])
                    break

            enemy = all_colors[(self.moving_player+1) % len(all_colors)]

            north_east = list(zip(range(row-1,-1,-1),range(col+1,self.size)))
            north_west = list(zip(range(row-1,-1,-1),range(col-1,-1,-1)))
            south_east = list(zip(range(row+1,self.size),range(col+1,self.size)))
            south_west = list(zip(range(row+1,self.size),range(col-1,-1,-1)))

            diagonals = [north_east,north_west,south_east,south_west]
            directions = [(-1,1),(-1,-1),(1,1),(1,-1)]
            direction_i = 0
            for diag in diagonals:
                direction = directions[direction_i]
                direction_i += 1
                for tile in diag:
                    new_row = tile[0]
                    new_col = tile[1]

                    if not piece_pinned or pin_direction == direction or pin_direction == (-direction[0],-direction[1]):
                        if self.board[new_row,new_col] == '---':
                            moves.append(Move((row,col),(new_row,new_col),self.board))
                        elif self.board[new_row,new_col].color == enemy:
                            moves.append(Move((row,col),(new_row,new_col),self.board))
                            break
                        else:
                            break

        elif type == 'q':   # Queens
            self.get_piece_moves(row,col,piece,moves,'b')
            self.get_piece_moves(row,col,piece,moves,'r')

        elif type == 'k':
            enemy = all_colors[(self.moving_player+1) % len(all_colors)]

            adjacents = [(row,col+1),(row,col-1),(row+1,col),(row-1,col),(row+1,col+1),(row+1,col-1),(row-1,col+1),(row-1,col-1)]

            for tile in adjacents:
                new_row = tile[0]
                new_col = tile[1]

                if (0 <= new_row) and (new_row <= self.size-1) and (0 <= new_col) and (new_col <= self.size-1):
                    piece = self.board[new_row,new_col]
                    if piece == '---' or piece.color == enemy:
                        self.kings[self.moving_player] = (new_row,new_col)
                        checked, pins, checks = self.get_pins_and_checks()
                        if not checked:
                            moves.append(Move((row,col),(new_row,new_col),self.board))
                        self.kings[self.moving_player] = (row,col)

    def get_pins_and_checks(self):
        pins = []
        checks = []
        checked = False

        enemy = all_colors[(self.moving_player+1) % len(all_colors)]

        king_row, king_col = self.get_my_king()

        directions = [(-1,0),(0,-1),(1,0),(0,1),(-1,-1),(-1,1),(1,-1),(1,1)]

        for j in range(len(directions)):
            direction = directions[j]
            possible_pin = ()

            for i in range(1,8):
                end_row = king_row + direction[0]*i
                end_col = king_col + direction[1]*i

                if 0 <= end_row < 8 and 0 <= end_col < 8:
                    piece = self.board[end_row,end_col]
                    if piece != '---':
                        type = piece.type
                        if piece.color != enemy and type != 'k':
                            if possible_pin == (): # First ally in direction
                                possible_pin = (end_row, end_col, direction[0], direction[1])
                            else: # Second ally
                                break

                        elif piece.color == enemy:
                            # Checks for all directions from king + knight's L tiles from kings for possible checks/pins.

                            if (0 <= j <= 3 and type == 'r') \
                            or (4 <= j <= 7 and type == 'b') \
                            or (i == 1 and type == 'p' and ((enemy == 'w' and 6 <= j <= 7) or (enemy == 'b' and 4 <= j <= 5))) \
                            or (type == 'q') or (i == 1 and type == 'k'):

                                if possible_pin == (): # No blocking ally -> Check
                                    checked = True
                                    checks.append((end_row,end_col,direction[0],direction[1]))
                                    break
                                else:
                                    pins.append(possible_pin)
                                    break
                            else:
                                break

        knight_moves = [(-2,-1),(-2,1),(-1,-2),(-1,2),(1,-2),(1,2),(2,-1),(2,1)]

        for move in knight_moves:
            end_row = king_row + move[0]
            end_col = king_col + move[1]

            if 0 <= end_row < 8 and 0 <= end_col < 8:
                piece = self.board[end_row,end_col]
                if piece != '---':
                    if piece.color == enemy and piece.type == 'n':
                        checked = True
                        checks.append((end_row,end_col,move[0],move[1]))
        return checked, pins, checks
