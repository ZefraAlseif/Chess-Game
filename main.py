import pygame as p
from logic import Logic
from logic import Move

p.init()
WIDTH = HEIGHT = 512  # Resolution of the screen
DIMENSION = 8  # dimensions of the chess board
SQ_SIZE = HEIGHT // DIMENSION  # dimension of each square
MAX_FPS = 15  # for animations later on
IMAGES = {}


# Initialize a global dictionary of images
def loadImages():
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
    valid_moves = game_state.validMoves()
    move_made = False #flag variable for when a move is made
    loadImages()
    running = True
    sq_selected = () # no square is selected
    player_clicks = [] # keep tracks of player clicks
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            # handles mouse click   
            elif e.type == p.MOUSEBUTTONDOWN: 
                location = p.mouse.get_pos() #(x,y) location of mouse
                col = location[0] // SQ_SIZE
                row = location[1] // SQ_SIZE
                if sq_selected == (row,col): # clicked the same square twice
                    sq_selected = () # corresponds to undo click
                    player_clicks = [] #clear
                else:    
                    sq_selected = (row,col)
                    player_clicks.append(sq_selected) # append for both clicks
                if len(player_clicks) == 2: # two clicks have occured
                    move = Move(player_clicks[0],player_clicks[1],game_state.board)
                    print(move.getChessNotation())
                    if move in valid_moves:
                        game_state.makeMove(move)
                        move_made = True
                        sq_selected = () #reset user clicks
                        player_clicks = []
                    else:
                        player_clicks = [sq_selected]
            # handles key presses
            elif e.type == p.KEYDOWN and e.key == p.K_z:
                game_state.undoMove() # undo move when z is pressed
                move_made = True
        if move_made:
            valid_moves = game_state.validMoves()
            move_made = True
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
