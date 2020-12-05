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
SPRITE_SCALE = 0.8 # Percentage of piece sprite occupying the tile (1 = fill entire tile)

FPS = 25
SPRITES = {}

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
    pass

def draw_board(screen,state):
    """
    Render graphics.
    """
    render_board(screen)
    render_tiles(screen,state.board)


def main():
    screen = pg.display.set_mode((WINDOW_W, WINDOW_H))
    clock = pg.time.Clock()
    screen.fill(pg.Color("white"))

    state = State()
    load_sprites()

    running = True
    while running:
        for e in pg.event.get():
            if e.type == pg.QUIT:
                running = False

        clock.tick(FPS)
        pg.display.flip()

        render_board(screen)

if __name__ == "__main__":
    main()
