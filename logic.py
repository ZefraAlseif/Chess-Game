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
        possible_moves = self.possibleMoves()
        for i in range(len(possible_moves)-1,-1,-1): # remove from a list from the end first
            self.makeMove(possible_moves[i])
            self.white_to_move = not self.white_to_move
            if self.inCheck():
                possible_moves.remove(possible_moves[i])
            self.white_to_move = not self.white_to_move
            self.undoMove()
        if len(possible_moves) == 0: # either checkmate or stalemate
            if self.inCheck():
                self.check_mate = True
            else:
                self.stale_mate = True
        else:
            self.check_mate = False
            self.stale_mate = False  
        return possible_moves # for now is returning possible moves
    
    # Determines if the current player is in check
    def inCheck(self):
        if self.white_to_move:
            return self.squareUnderAttack(self.white_king_location[0],self.white_king_location[1])
        else:
            return self.squareUnderAttack(self.black_king_location[0],self.black_king_location[1])
        
    # Determines if the enemy can attack a specific square (r,c)
    def squareUnderAttack(self,r,c):
        self.white_to_move = not self.white_to_move
        # Generate all of the possible moves for the opponent
        possible_opp_moves = self.possibleMoves() # switch turn back
        self.white_to_move = not self.white_to_move
        for move in possible_opp_moves:
            if move.end_row == r and move.end_col == c: # square is under attack
                return True
        return False
    
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
        if self.white_to_move: # white pawn moves
            if self.board[r-1][c] == "--": # one square move
                possible_moves.append(Move((r,c),(r-1,c),self.board))
                if r == 6 and self.board[r-2][c] == "--": # two square move
                    possible_moves.append(Move((r,c),(r-2,c),self.board))
            if c-1 >= 0 and self.board[r-1][c-1][0] == "b": # capture enemy piece to the left
                possible_moves.append(Move((r,c),(r-1,c-1),self.board))
            if c+1 <= 7 and self.board[r-1][c+1][0] == "b": # capture enemy piece to the right
                possible_moves.append(Move((r,c),(r-1,c+1),self.board))
        else: # black pawn moves
            if self.board[r+1][c] == "--":
                possible_moves.append(Move((r,c),(r+1,c),self.board))
                if r == 1 and self.board[r+2][c] == "--": # two square move
                    possible_moves.append(Move((r,c),(r+2,c),self.board))
            if c-1 >= 0 and self.board[r+1][c-1][0] == "w": # capture enemy piece to the right
                possible_moves.append(Move((r,c),(r+1,c-1),self.board))
            if c+1 <= 7 and self.board[r+1][c+1][0] == "w": # capture enemy piece to the left
                possible_moves.append(Move((r,c),(r+1,c+1),self.board))
    
    # Get all rook moves
    def getRookMoves(self,r,c,possible_moves):
        directions = ((-1,0),(0,-1),(1,0),(0,1)) # directions the piece can move
        enemycolor = "b" if self.white_to_move else "w" # check the enemy pieces
        for d in directions:
            for i in range(1,8):
                end_row = r + d[0] * i
                end_col = c + d[1] * i
                if 0 <= end_row < 8 and 0 <= end_col < 8:
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
        directions = ((1,2),(2,1),(2,-1),(1,-2),(-1,-2),(-2,-1),(-2,1),(-1,2))
        enemycolor = "b" if self.white_to_move else "w"
        for d in directions:
            end_row = r + d[0] 
            end_col = c + d[1] 
            if 0 <= end_row < 8 and 0 <= end_col < 8:
                end_piece = self.board[end_row][end_col]
                if end_piece == "--" or end_piece[0] == enemycolor:
                    possible_moves.append(Move((r,c),(end_row,end_col),self.board))

    # Get all Bishop Moves
    def getBishopMoves(self,r,c,possible_moves):
        directions = ((-1,1),(1,-1),(1,1),(-1,-1)) # directions the piece can move
        enemycolor = "b" if self.white_to_move else "w" # check the enemy pieces
        for d in directions:
            for i in range(1,8):
                end_row = r + d[0] * i
                end_col = c + d[1] * i
                if 0 <= end_row < 8 and 0 <= end_col < 8:
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
        directions = ((-1,0),(0,-1),(1,0),(0,1),(-1,1),(1,-1),(1,1),(-1,-1))
        enemycolor = "b" if self.white_to_move else "w" # check the enemy pieces
        for d in directions:
            end_row = r + d[0] 
            end_col = c + d[1]
            if 0 <= end_row < 8 and 0 <= end_col < 8:
                end_piece = self.board[end_row][end_col]
                if end_piece == "--" or end_piece[0] == enemycolor: # empty space on board  
                    possible_moves.append(Move((r,c),(end_row,end_col),self.board))   
    
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
