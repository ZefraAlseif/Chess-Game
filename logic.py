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
        
    # Takes a move and makes it (Except. castling, en-pessant, and pawn promotion)
    def makeMove(self,move):
        self.board[move.start_row][move.start_col] = "--"
        self.board[move.end_row][move.end_col] = move.piece_moved
        self.move_log.append(move) # log the move
        self.white_to_move = not self.white_to_move # swap player turn
    
    # Undo the last move made by a player
    def undoMove(self):
        if len(self.move_log) != 0: # make sure there is a move to undo
            move = self.move_log.pop()
            self.board[move.start_row][move.start_col] = move.piece_moved
            self.board[move.end_row][move.end_col] = move.piece_captured  
            self.white_to_move = not self.white_to_move
    
    # Obtain all of the legal moves considering checks        
    def validMoves(self):
        return self.possibleMoves() # for now is returning possible moves
    
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
        pass                    
    
    # Get all Knight moves
    def getKnightMoves(self,r,c,possible_moves):
        pass
    
    # Get all Bishop Moves
    def getBishopMoves(self,r,c,possible_moves):
        pass
    
    # Get all Queen Moves
    def getQueenMoves(self,r,c,possible_moves):
        self.getRookMoves(r,c,possible_moves)
        self.getBishopMoves(r,c,possible_moves)
    
    # Get all King Moves
    def getKingMoves(self,r,c,possible_moves):
        pass
    
    
class Move():
    ranks_to_rows = {"1": 7, "2": 6, "3": 5, "4": 4,
                     "5": 3, "6": 2, "7": 1, "8": 1}
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
