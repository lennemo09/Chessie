"""
MAIN DRIVER FOR CHESSIE.

@ ACKNOWLEDGEMENT:
@ Chess sprites from: JohnPablok's improved Cburnett chess set.
@ Found at: https://opengameart.org/content/chess-pieces-and-board-squares
@
@ PyGame introduction tutorial by Eddie Sharick: https://www.youtube.com/watch?v=EnYui0e73Rs
"""

from chessie_engine import *
import pygame as pg

## STANDARD PYGAME INITIALIZATION
pg.init()

WINDOW_W = WINDOW_H = 512
BOARD_SIZE = 8

TILE_SIZE = WINDOW_H // BOARD_SIZE
SPRITE_SCALE = 1.0 # Percentage of piece sprite occupying the tile (1 = fill entire tile)

FPS = 25
SPRITES = {}
THEME = 0
PLAYER = 0 # 0 = White, 1 = Black

themes = ["gray","brown"]

def load_sprites():
    """
    Load all pieces sprites.
    """
    for piece in pieces_names:
        #print("Loading piece:","../sprites/pieces/{}.png".format(piece))
        sprite = pg.image.load("../sprites/pieces/{}.png".format(piece))
        SPRITES[piece] = pg.transform.scale(sprite, (int(SPRITE_SCALE*TILE_SIZE),int(SPRITE_SCALE*TILE_SIZE)))

    for col in themes:
        tile_light = pg.image.load("../sprites/pieces/square_{}_light.png".format(col))
        tile_dark = pg.image.load("../sprites/pieces/square_{}_dark.png".format(col))

        SPRITES[col+'_light'] = pg.transform.scale(tile_light, (TILE_SIZE,TILE_SIZE))
        SPRITES[col+'_dark'] = pg.transform.scale(tile_dark, (TILE_SIZE,TILE_SIZE))

    selected = pg.image.load("../sprites/pieces/square_selected.png".format(piece))
    SPRITES['selected'] = pg.transform.scale(selected, (TILE_SIZE,TILE_SIZE))
    valid = pg.image.load("../sprites/pieces/square_valid.png".format(piece))
    SPRITES['valid'] = pg.transform.scale(valid, (TILE_SIZE,TILE_SIZE))
    capture = pg.image.load("../sprites/pieces/square_capture.png".format(piece))
    SPRITES['capture'] = pg.transform.scale(capture, (TILE_SIZE,TILE_SIZE))


def render_board(screen,theme=0):
    """
    Render board's background tiles' colors according to a chosen theme.
    Theme 0: Gray board.
    Theme 1: Brown board.

    NOTE: Due to PyGame's logic, always render board before tiles.
    """
    if theme == 0:
        color = 'gray'
    else:
        color = 'brown'

    # Note: Tile (0,0) for both perspective is a light tile.
    # Because the tiles are interleaved, we can use the tile's coordinates to find its color.
    shades = ['light','dark']
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            shade = shades[(row+col)%2]
            tile = color + '_' + shade
            screen.blit(SPRITES[tile], pg.Rect(col*TILE_SIZE, row*TILE_SIZE, TILE_SIZE, TILE_SIZE))


def render_tiles(screen,board):
    """
    Render the tiles with the correct pieces on it.
    """
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            piece = board[row,col]

            if piece != "---":
                piece_name = piece.name
                screen.blit(SPRITES[piece_name], pg.Rect(col*TILE_SIZE, row*TILE_SIZE, TILE_SIZE, TILE_SIZE))


def render_selection(screen,board,selection,valid_moves):
    row = selection[0]
    col = selection[1]
    screen.blit(SPRITES['selected'], pg.Rect(col*TILE_SIZE, row*TILE_SIZE, TILE_SIZE, TILE_SIZE))

    if board[row,col] != '---':
        for move in valid_moves:
            if move.src_row == row and move.src_col == col:
                new_row = move.dst_row
                new_col = move.dst_col

                if board[new_row,new_col] == '---':
                    screen.blit(SPRITES['valid'], pg.Rect(new_col*TILE_SIZE, new_row*TILE_SIZE, TILE_SIZE, TILE_SIZE))
                else:
                    screen.blit(SPRITES['capture'], pg.Rect(new_col*TILE_SIZE, new_row*TILE_SIZE, TILE_SIZE, TILE_SIZE))

def draw_board(screen,state,selection=(),valid_moves=[]):
    """
    Render graphics.
    """
    render_board(screen,THEME)
    if selection != ():
        render_selection(screen,state.board,selection,valid_moves)
    render_tiles(screen,state.board)


def main():
    screen = pg.display.set_mode((WINDOW_W, WINDOW_H))
    clock = pg.time.Clock()
    screen.fill(pg.Color("white"))

    state = State()
    load_sprites()

    running = True

    selected = () # User's last seletec tile (row,col)
    selection_buffer = [] # Store user's last selected tiles [src,dst]

    valid_moves = state.get_valid_moves()
    moved = False # Only updates  when user made a move, doesn't update every frame

    while running:
        for e in pg.event.get():
            if e.type == pg.QUIT:
                running = False

            elif e.type == pg.MOUSEBUTTONDOWN:
                pos = pg.mouse.get_pos() # Add offset if extra GUI panels are added (mouse coord needs to be relative to the board's borders, not window's)

                col = pos[0] // TILE_SIZE
                row = pos[1] // TILE_SIZE

                if (row,col) == selected: # Selected the same tile twice, deselect
                    selected = ()
                    selection_buffer = []
                else:
                    selected = (row,col)
                    selection_buffer.append(selected)

                if len(selection_buffer) == 2: # 2 tiles selected -> Move
                    move = Move(selection_buffer[0], selection_buffer[1], state.board)

                    if move in valid_moves:
                        state.move_piece(move)
                        print(move.get_notation())
                        moved = True
                        selected = ()
                        selection_buffer = []
                    else:
                        selection_buffer =[selected]

            elif e.type == pg.KEYDOWN:
                if e.key == pg.K_z:
                    print("Undid a move.")
                    state.undo()
                    moved = True
        if moved:
            # Only update moves when the board changes
            valid_moves = state.get_valid_moves()
            moved = False

        draw_board(screen,state,selected,valid_moves)
        clock.tick(FPS)
        pg.display.flip()



if __name__ == "__main__":
    main()
