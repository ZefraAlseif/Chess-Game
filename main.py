import pygame as p
from logic import Logic

p.init()
WIDTH = HEIGHT = 512  # Resolution of the screen
DIMENSION = 8  # dimensions of the chess board
SQ_SIZE = HEIGHT // DIMENSION  # dimension of each square
MAX_FPS = 15  # for animations later on
IMAGES = {}


# Initialize a global dictionary of images
def load_images():
    pieces = ["wR", "wN", "wB", "wQ", "wK", "bR", "bN", "bB", "bQ", "bK", "wP", "bP"]
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(
            p.image.load("Pieces_Sprite/" + piece + ".png"), (SQ_SIZE, SQ_SIZE)
        )


"""
The main drive for our code. This will handle user input and updating the graphics
"""


def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    game_state = Logic()
    load_images()
    running = True
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
        drawGameState(screen, game_state)
        clock.tick(MAX_FPS)
        p.display.flip()


"""
Responsible for all graphics in the current game state
"""


def drawGameState(screen, game_state):
    drawBoard(screen)  # draw the squares on the board
    drawPieces(screen, game_state.board)  # draw pieces on top of those squares


def drawBoard(screen):
    colors = [p.Color("gold"), p.Color("blue")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r + c) % 2)]
            p.draw.rect(screen, color, p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))


def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--":
                screen.blit(IMAGES[piece],p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))


if __name__ == "__main__":
    main()
