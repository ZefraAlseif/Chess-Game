class Logic():
    # Initializes the game of chess
    def __init__(self):
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"],
        ]
        self.white_to_move = True
        self.move_log = []
        self.move_functions = {"P":self.getPawnMoves,"R":self.getRookMoves,"N":self.getKnightMoves,\
                               "B":self.getBishopMoves, "Q":self.getQueenMoves,"K":self.getKingMoves }
        # Keep track of king location
        self.white_king_location = (7,4) 
        self.black_king_location = (0,4)
        # Validate the moves
        self.in_check = False
        self.pins = []
        self.checks = []
        # Checking if the game is over
        self.check_mate = False
        self.stale_mate = False
        
    # Takes a move and makes it (Except. castling, en-pessant, and pawn promotion)
    def makeMove(self,move):
        self.board[move.start_row][move.start_col] = "--"
        self.board[move.end_row][move.end_col] = move.piece_moved
        self.move_log.append(move) # log the move
        self.white_to_move = not self.white_to_move # swap player turn
        # update the king's location if moved
        if move.piece_moved == "wK": 
            self.white_king_location = (move.end_row, move.end_col)
        elif move.piece_moved == "bK":
            self.black_king_location = (move.end_row, move.end_col)
    
    # Undo the last move made by a player
    def undoMove(self):
        if len(self.move_log) != 0: # make sure there is a move to undo
            move = self.move_log.pop()
            self.board[move.start_row][move.start_col] = move.piece_moved
            self.board[move.end_row][move.end_col] = move.piece_captured  
            self.white_to_move = not self.white_to_move
            # update the king's location if needed
            if move.piece_moved == "wK": 
                self.white_king_location = (move.start_row, move.start_col)
            elif move.piece_moved == "bK":
                self.black_king_location = (move.start_row, move.start_col)
                
    # Obtain all of the legal moves considering checks        
    def validMoves(self):
        possible_moves = []
        self.in_check, self.pins, self.checks = self.getPinsAndChecks()
        if self.white_to_move:
            king_row = self.white_king_location[0]
            king_col = self.white_king_location[1]
        else:
            king_row = self.black_king_location[0]
            king_col = self.black_king_location[1]
        if self.in_check:
            if len(self.checks) == 1: # block check or move king
                possible_moves = self.possibleMoves()
                check = self.checks[0] # check info
                check_row = check[0]
                check_col = check[1]
                piece_checking = self.board[check_row][check_col] # enemy piece 
                valid_squares = [] # squares that pieces can move to
                if piece_checking[1] == "N":
                    valid_squares = [(check_row,check_col)]
                else:
                    for i in range(1,8):
                        valid_square = (king_row + check[2] * i, king_col + check[3] * i) # check directions
                        valid_squares.append(valid_square)
                        if valid_square[0] == check_row and valid_square[1] == check_col:
                            break
                # get rid of any moves that dont block check or move king
                for i in range(len(possible_moves)-1,-1,-1):
                    if possible_moves[i].piece_moved[1] != "K":
                       if not (possible_moves[i].end_row,possible_moves[i].end_col) in valid_squares:
                           possible_moves.remove(possible_moves[i])
            else:
                self.getKingMoves(king_row,king_col,possible_moves)
        else:
            possible_moves = self.possibleMoves()
        return possible_moves                                        
    
    # Obtain all of the legal moves whithout considering checks
    def possibleMoves(self):
        possible_moves = []
        for r in range(len(self.board)): # number of rows
            for c in range(len(self.board[r])): # number of cols in the row
                turn = self.board[r][c][0]
                if (turn == "w" and self.white_to_move) or (turn == "b" and not self.white_to_move):
                    piece = self.board[r][c][1]
                    self.move_functions[piece](r,c,possible_moves) # calls the appropriate move function
        return possible_moves
    
    # Get all pawn moves                    
    def getPawnMoves(self,r,c,possible_moves):
        piece_pinned = False
        pin_direction = ()
        for i in range(len(self.pins)-1,-1,-1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piece_pinned = True
                pin_direction = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break
        
        if self.white_to_move: # white pawn moves
            if self.board[r-1][c] == "--": # one square move
                if not piece_pinned or pin_direction == (-1,0):
                    possible_moves.append(Move((r,c),(r-1,c),self.board))
                    if r == 6 and self.board[r-2][c] == "--": # two square move
                        possible_moves.append(Move((r,c),(r-2,c),self.board))
            # captures
            if c-1 >= 0 and self.board[r-1][c-1][0] == "b": # capture enemy piece to the left
                if not piece_pinned or pin_direction == (-1,-1):
                    possible_moves.append(Move((r,c),(r-1,c-1),self.board))
            if c+1 <= 7 and self.board[r-1][c+1][0] == "b": # capture enemy piece to the right
                if not piece_pinned or pin_direction == (-1,1):
                    possible_moves.append(Move((r,c),(r-1,c+1),self.board))
        else: # black pawn moves
            if self.board[r+1][c] == "--":
                if not piece_pinned or pin_direction == (1,0):
                    possible_moves.append(Move((r,c),(r+1,c),self.board))
                    if r == 1 and self.board[r+2][c] == "--": # two square move
                        possible_moves.append(Move((r,c),(r+2,c),self.board))
            if c-1 >= 0 and self.board[r+1][c-1][0] == "w": # capture enemy piece to the right
                if not piece_pinned or pin_direction == (1,-1):
                    possible_moves.append(Move((r,c),(r+1,c-1),self.board))
            if c+1 <= 7 and self.board[r+1][c+1][0] == "w": # capture enemy piece to the left
                if not piece_pinned or pin_direction == (1,1):
                    possible_moves.append(Move((r,c),(r+1,c+1),self.board))
    
    # Get all rook moves
    def getRookMoves(self,r,c,possible_moves):
        piece_pinned = False
        pin_direction = ()
        for i in range(len(self.pins)-1,-1,-1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piece_pinned = True
                pin_direction = (self.pins[i][2], self.pins[i][3])
                if self.board[r][c][1] != "Q": # cant remove queen from pin
                    self.pins.remove(self.pins[i])
                break
        
        directions = ((-1,0),(0,-1),(1,0),(0,1)) # directions the piece can move
        enemycolor = "b" if self.white_to_move else "w" # check the enemy pieces
        for d in directions:
            for i in range(1,8):
                end_row = r + d[0] * i
                end_col = c + d[1] * i
                if 0 <= end_row < 8 and 0 <= end_col < 8:
                    if not piece_pinned or pin_direction == d or pin_direction == (-d[0],-d[1]):
                        end_piece = self.board[end_row][end_col]
                        if end_piece == "--": # empty space on board  
                            possible_moves.append(Move((r,c),(end_row,end_col),self.board))
                        elif end_piece[0] == enemycolor: # enemy piece 
                            possible_moves.append(Move((r,c),(end_row,end_col),self.board)) 
                            break;
                        else: # friendly piece 
                            break;
                else: # out of the board
                    break;                
    
    # Get all Knight moves
    def getKnightMoves(self,r,c,possible_moves):
        piece_pinned = False
        for i in range(len(self.pins)-1,-1,-1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piece_pinned = True
                self.pins.remove(self.pins[i])
                break
        
        directions = ((1,2),(2,1),(2,-1),(1,-2),(-1,-2),(-2,-1),(-2,1),(-1,2))
        enemycolor = "b" if self.white_to_move else "w"
        for d in directions:
            end_row = r + d[0] 
            end_col = c + d[1] 
            if 0 <= end_row < 8 and 0 <= end_col < 8:
                if not piece_pinned:
                    end_piece = self.board[end_row][end_col]
                    if end_piece == "--" or end_piece[0] == enemycolor:
                        possible_moves.append(Move((r,c),(end_row,end_col),self.board))

    # Get all Bishop Moves
    def getBishopMoves(self,r,c,possible_moves):
        piece_pinned = False
        pin_direction = ()
        for i in range(len(self.pins)-1,-1,-1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piece_pinned = True
                pin_direction = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break
        
        directions = ((-1,1),(1,-1),(1,1),(-1,-1)) # directions the piece can move
        enemycolor = "b" if self.white_to_move else "w" # check the enemy pieces
        for d in directions:
            for i in range(1,8):
                end_row = r + d[0] * i
                end_col = c + d[1] * i
                if 0 <= end_row < 8 and 0 <= end_col < 8:
                    if not piece_pinned or pin_direction == d or pin_direction == (-d[0],-d[1]):
                        end_piece = self.board[end_row][end_col]
                        if end_piece == "--": # empty space on board  
                            possible_moves.append(Move((r,c),(end_row,end_col),self.board))
                        elif end_piece[0] == enemycolor: # enemy piece 
                            possible_moves.append(Move((r,c),(end_row,end_col),self.board)) 
                            break;
                        else: # friendly piece 
                            break;
                else: # out of the board
                    break;            
    
    # Get all Queen Moves
    def getQueenMoves(self,r,c,possible_moves):
        self.getRookMoves(r,c,possible_moves)
        self.getBishopMoves(r,c,possible_moves)
    
    # Get all King Moves (without checks)
    def getKingMoves(self,r,c,possible_moves):
        row_moves = (-1,-1,-1,0,0,1,1,1)
        col_moves = (-1,0,1,-1,1,-1,0,1)
        ally_color = "w" if self.white_to_move else "b" # check the enemy pieces
        for i in range(8):
            end_row = r + row_moves[i] 
            end_col = c + col_moves[i]
            if 0 <= end_row < 8 and 0 <= end_col < 8:
                end_piece = self.board[end_row][end_col]
                if end_piece[0] != ally_color:
                    # place king on end square
                    if ally_color == "w":
                        self.white_king_location = (end_row,end_col)
                    else:
                        self.black_king_location = (end_row,end_col)
                in_check, pins, checks = self.getPinsAndChecks()
                if not in_check:
                    possible_moves.append(Move((r,c),(end_row,end_col),self.board))
                # put king back on original location
                if ally_color == "w":
                    self.white_king_location = (r,c)
                else:
                    self.black_king_location = (r,c)

    # Returns if the player is in check, a list of pins and a list of checks
    def getPinsAndChecks(self):
        pins = [] # squares where the allied pinned piece is and direction from
        checks = [] # squares wehre enemy is applying a check
        in_check = False
        if self.white_to_move:
            enemy_color = "b"
            ally_color = "w"
            start_row = self.white_king_location[0]
            start_col = self.white_king_location[1]
        else:
            enemy_color = "w"
            ally_color = "b"
            start_row = self.black_king_location[0]
            start_col = self.black_king_location[1]
        # check outward from king for pins and checks, keep track of pins
        directions =  ((-1,0),(0,-1),(1,0),(0,1),(-1,1),(1,-1),(1,1),(-1,-1))
        for j in range(len(directions)):
            d = directions[j]
            possible_pin = () # reset possible pins
            for i in range(1,8):
                end_row = start_row + d[0] * i
                end_col = start_col + d[1] * i  
                if 0 <= end_row < 8 and 0 <= end_col < 8:
                    end_piece = self.board[end_row][end_col]
                    if end_piece[0] == ally_color and end_piece[1] != "K":
                        if possible_pin == (): 
                            possible_pin = (end_row,end_col,d[0],d[1])
                        else: # no pin in this direction
                            break
                    elif end_piece[0] == enemy_color:
                        # end_piece[1] is the type
                        if (0 <= j <= 3 and end_piece[1] == "R") or \
                            (4 <= j <= 7 and end_piece[1] == "B") or \
                            (i == 1 and end_piece[1] == "P" and ((enemy_color == "w" and 6 <= j <= 7) or (enemy_color == "b" and 4 <= j <= 5))) or \
                            (end_piece[1] == "Q") or (i == 1 and end_piece[1] == "K"):
                            if possible_pin == (): # no piece blocking, so check
                                in_check = True
                                checks.append((end_row,end_col,d[0],d[1]))
                                break
                            else: # piece blocking so pin
                                pins.append(possible_pin)
                                break
                        else: # enemy piece not applying check:
                            break
                else: # off-board
                    break
        # check for knight checks
        knight_directions = ((1,2),(2,1),(2,-1),(1,-2),(-1,-2),(-2,-1),(-2,1),(-1,2))
        for m in knight_directions:
            end_row = start_row + m[0] 
            end_col = start_col + m[1]   
            if 0 <= end_row < 8 and 0 <= end_col < 8:
                end_piece = self.board[end_row][end_col]
                if end_piece[0] == enemy_color and end_piece[1] == "N": # enemy knight attacking king
                    in_check = True
                    checks.append((end_row,end_col,m[0],m[1]))
        return in_check, pins, checks
 
class Move():
    ranks_to_rows = {"1": 7, "2": 6, "3": 5, "4": 4,
                     "5": 3, "6": 2, "7": 1, "8": 0}
    rows_to_ranks = {v: k for k, v in ranks_to_rows.items()}

    files_to_cols = {"a": 0, "b": 1, "c": 2, "d": 3,
                     "e": 4, "f": 5, "g": 6, "h": 7}
    cols_to_files = {v: k for k, v in files_to_cols.items()}

    def __init__(self, start_sq, end_sq, board):
        # Pieces first click
        self.start_row = start_sq[0]
        self.start_col = start_sq[1]
        # Pieces second click
        self.end_row = end_sq[0]
        self.end_col = end_sq[1]
        # Pieces Moved and Captures
        self.piece_moved = board[self.start_row][self.start_col]
        self.piece_captured = board[self.end_row][self.end_col]
        
        self.moveID = self.start_row * 1000 + self.start_col * 100 \
                    + self.end_row * 10 + self.end_col
        #print(self.moveID)
    
    # Overriding the equals method
    def __eq__(self, other):
        if isinstance(other,Move):
            return self.moveID == other.moveID
        return False
    
    # Introduced Proper Chess Notation (ex. Nf3)
    def getChessNotation(self):
        return self.piece_moved[1] + \
               self.getRankedFile(self.end_row, self.end_col)

    def getRankedFile(self, row, col):
        return self.cols_to_files[col] + self.rows_to_ranks[row]
