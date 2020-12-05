"""
MAIN DRIVER FOR CHESSIE.

@ ACKNOWLEDGEMENT:
@ Chess sprites from: JohnPablok's improved Cburnett chess set.
@ Found at: https://opengameart.org/content/chess-pieces-and-board-squares
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


def load_sprites():
    for piece in pieces_names:
        #print("Loading piece:","../sprites/pieces/{}.png".format(piece))
        sprite = pg.image.load("../sprites/pieces/{}.png".format(piece))
        SPRITES[piece] = pg.transform.scale(sprite, (int(SPRITE_SCALE*TILE_SIZE),int(SPRITE_SCALE*TILE_SIZE)))


def main():
    screen = pg.display.set_mode((WINDOW_W, WINDOW_H))
    clock = pg.time.Clock()
    screen.fill(pg.Color("white"))

    state = State()
    print(state.board)

main()
