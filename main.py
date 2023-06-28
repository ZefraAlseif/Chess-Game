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
    move_made = False # flag variable for when a move is made
    animate = False # flag variable for animation
    loadImages()
    running = True
    sq_selected = () # no square is selected
    player_clicks = [] # keep tracks of player clicks
    game_over = False
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            # handles mouse click   
            elif e.type == p.MOUSEBUTTONDOWN: 
                if not game_over:    
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
                        for i in range(len(valid_moves)):    
                            if move == valid_moves[i]:
                                game_state.makeMove(valid_moves[i])
                                move_made = True
                                sq_selected = () # reset user clicks
                                animate = True
                                player_clicks = []
                        if not move_made:    
                            player_clicks = [sq_selected]
            # handles key presses
            elif e.type == p.KEYDOWN: 
                if e.key == p.K_z:
                    game_state.undoMove() # undo move when z is pressed
                    move_made = True
                    animate = False
                if e.key == p.K_r: # reset the board when 'r' is pressed
                    game_state = Logic()  
                    valid_moves = game_state.validMoves()
                    sq_selected = ()
                    player_clicks = []
                    move_made = True
                    animate = False
                    game_over = False 
        if move_made:
            if animate:
                animateMove(game_state.move_log[-1],screen,game_state.board,clock)
            valid_moves = game_state.validMoves()
            move_made = False
            animate = False
        drawGameState(screen, game_state,valid_moves,sq_selected)
        if game_state.check_mate:
            game_over = True
            if game_state.white_to_move:
                drawText(screen, "Black wins by checkmate")
            else:
                drawText(screen, "White wins by checkmate")
        elif game_state.stale_mate:
            game_over = True
            drawText(screen,"Stalemate")
        clock.tick(MAX_FPS)
        p.display.flip()
        """
        Ending the game 
        if game_state.check_mate:
            running = False
        elif game_state.stale_mate:
            running = False
        else:
            running = True
        """


"""
Responsible for all graphics in the current game state
"""

# Highligh square selected
def highlightSquares(screen,game_state,valid_moves,sq_selected):
    if sq_selected != ():
        r,c = sq_selected
        if game_state.board[r][c][0] == ("w" if game_state.white_to_move else "b"):
            # highlight selected square
            s = p.Surface((SQ_SIZE,SQ_SIZE))
            s.set_alpha(250) # transperancy value 
            s.fill(p.Color("green"))
            screen.blit(s,(c * SQ_SIZE, r * SQ_SIZE))
            # highlight moves from that square
            s.fill(p.Color("red"))
            for move in valid_moves:
                if move.start_row == r and move.start_col == c:
                    screen.blit(s,(move.end_col * SQ_SIZE , move.end_row * SQ_SIZE ))
                    
# Draw the current game state
def drawGameState(screen, game_state, valid_moves,sq_selected):
    drawBoard(screen)  # draw the squares on the board
    highlightSquares(screen,game_state,valid_moves,sq_selected)
    drawPieces(screen, game_state.board)  # draw pieces on top of those squares
    
# Draw the board
def drawBoard(screen):
    global colors
    colors = [p.Color("gold"), p.Color("blue")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r + c) % 2)]
            p.draw.rect(screen, color, p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))
            
# Draw the pieces
def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--":
                screen.blit(IMAGES[piece],p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))

# Animating a move
def animateMove(move,screen,board,clock):
    global colors
    dR = move.end_row - move.start_row
    dC = move.end_col - move.start_col
    frames_per_square = 10 # frames to move one square
    frame_count = (abs(dR) + abs(dC)) * frames_per_square
    for frame in range(frame_count + 1):
        r,c = (move.start_row + dR*frame/frame_count,move.start_col + dC*frame/frame_count)
        drawBoard(screen)
        drawPieces(screen,board)
        # erase the piece moved from ending square
        color = colors[(move.end_row+move.end_col) % 2] 
        end_square = p.Rect(move.end_col * SQ_SIZE, move.end_row * SQ_SIZE, SQ_SIZE, SQ_SIZE)
        p.draw.rect(screen,color,end_square)
        # draw captured piece onto rectangle
        if move.piece_captured != "--":
            screen.blit(IMAGES[move.piece_captured], end_square)
        # draw moving piece
        screen.blit(IMAGES[move.piece_moved],p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))
        p.display.flip()
        clock.tick(60)
    
def drawText(screen,text):
    font = p.font.SysFont("Helvitca",32,True,False)
    text_obj = font.render(text,0,p.Color("Gray"))
    text_location = p.Rect(0,0,WIDTH,HEIGHT).move(WIDTH/2-text_obj.get_width()/2,HEIGHT/2-text_obj.get_height()/2)
    screen.blit(text_obj,text_location)
    text_obj = font.render(text,0,p.Color("Black"))
    screen.blit(text_obj,text_location.move(2,2))
if __name__ == "__main__":
    main()
