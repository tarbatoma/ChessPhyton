"""
Aceasta clasa este responsabila sa stocheze toate informatiile actuala ale jocului de sah si sa o sa se ocupe de mutarile valide  si va pastralog-ul de mutari
"""

class GameState():
    def __init__(self):
        # tabla de sah este o lista  8X8 2d si fiecare element din lista are 2 caractere
        #primul caracter reprezinta culoarea piese, 'b' sau ' white'
        #cel de-al doilea reprezinta tipul piese care poate fi  'k'=King, 'Q'=Queen, 'R'=Rook, 'B'=Bishop, 'N'=Knight sau 'P'=Pawn
        # '--'= spatiu liber fara piese
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "wR", "--", "--", "bK", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"],
        ]
        self.moveFunctions = {'p': self.getPawnMoves, 'R': self.getRookMoves, 'N': self.getKnightMoves,
                              'B': self.getBishopMoves, 'Q': self.getQueenMoves, 'K': self.getKingMoves}

        self.whiteToMove = True
        self.moveLog = []


    #Preia o mutare ca parametru si o executa ( nu va function pentru castling, pown promotion, si en-passant(capturarea pionului))
    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "--"     #dupa ce mutam piesa lasa spatiul gol
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move) #inregistram mutarea ca sa o putem modifica ulterior daca este necesar
        self.whiteToMove = not self.whiteToMove #schimbam turele playerilor


    def undoMove(self):
        if len(self.moveLog) != 0: # ne asiguram ca este o mutare care putem face undo la ea
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove #facem schimb de tura inapoi

    '''
    Toate mutarile considerate valide
    '''
    def getValidMoves(self):
        return self.getAllPossibleMoves()

    '''
    Toate mutarile fara validare
    '''
    def getAllPossibleMoves(self):
        moves = []
        for r in range(len(self.board)): #numarul de randuri
            for c in range(len(self.board[r])): #numarul de coloane in randurile date
                turn = self.board[r][c][0]
                if (turn == 'w' and self.whiteToMove) or (turn == 'b' and not self.whiteToMove):
                    piece = self.board[r][c][1]
                    self.moveFunctions [piece](r, c, moves) #apeleaza corect functia move in baza tipului piesei
        return moves




    '''
    Preia toate mutarile  pionul localizat in randul si coloana respectiva si creeaza mutari in lista
    '''
    def getPawnMoves(self, r, c, moves):
        if self.whiteToMove: #mutarea  pionilor albi
            if self.board[r-1][c] == "--": #mutare de un patrat a pionului
                moves.append(Move((r, c) , (r-1, c), self.board))
                if r == 6 and self.board[r-2][c] =="--": # 2 patrate mutare pion
                    moves.append(Move((r, c), (r-2, c), self.board))
            if c-1 >= 0:
                if self.board[r-1][c-1][0] == 'b': #este o piesa inima de capturat
                    moves.append(Move((r, c), (r - 1 , c - 1), self.board))
                if c+1 <= 7: #captureaza piesa inamica la dreapta
                    if self.board[r-1][c+1][0] == 'b': # piesa inamica de capturat
                        moves.append(Move((r, c),(r-1, c+1), self.board))

        else: #pionul negru mutari
            if self.board[r + 1][c] == "--": # mutare 1 patrat
                moves.append(Move((r,c), (r + 1, c), self.board))
                if r == 1 and self.board[r+2][c] == "--": #2 square moves
                    moves.append(Move((r,c), (r + 2, c), self.board))
            # captures
            if c - 1 >= 0: #captura la stanga
                if self.board[r + 1][c - 1][0] == 'w':
                    moves.append(Move((r, c), (r + 1, c - 1), self.board))
            if c + 1 <=7: #captura la dreapta
                if self.board[r+1][c+1][0] == 'w':
                    moves.append(Move((r, c), (r + 1, c + 1), self.board))

    '''
    Preia toate mutarile  turei localizat in randul si coloana respectiva si creeaza mutari in lista
    '''
    def getRookMoves(self, r, c, moves):
        directions = ((-1, 0), (0, -1), (1,0), (0, 1)) # sus, stanga, jos , dreapta
        enemyColor = "b" if self.whiteToMove else "w"
        for d in directions:
            for i in range(1, 8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8: #pe tabla
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--": #spatiu gol valid
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                    elif endPiece[0] == enemyColor: # enemy piece valid
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                        break
                    else:  # piesa proprie rezulta invalid
                        break
                else :  # inafara tablei de joc
                    break


    '''
    Preia toate mutarile  turei localizat in randul si coloana respectiva si creeaza mutari in lista
    '''
    def getKnightMoves(self, r, c, moves):
        knightMoves = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
        allyColor = "w" if self.whiteToMove else "b"
        for m in knightMoves:
            endRow = r + m[0]
            endCol = c + m[1]
            if 0 <= endRow < 8 and 0 <= endCol <8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColor: #nnu este piesa aliata (spatiu gol sau piesa inamica)
                    moves.append(Move((r, c), (endRow, endCol), self.board))


    '''
    Preia toate mutarile  nebunului localizat in randul si coloana respectiva si creeaza mutari in lista
    '''
    def getBishopMoves(self, r, c, moves):
        directions = ((-1, -1), (-1, 1), (1, -1), (1, 1)) #diagonale
        enemyColor = "b" if self.whiteToMove else "w"
        for d in directions:
            for i in range(1, 8): #nebunul poate traversa doar 7 casute
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8: #daca este pe tabla
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--" : #spatiu gol valid
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                    elif endPiece[0] == enemyColor: #enemy piece valid
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                        break
                    else: #friendly piece invalid
                        break
                else:   # off board
                    break

    '''
    Preia toate mutarile  reginei localizat in randul si coloana respectiva si creeaza mutari in lista
    '''
    def getQueenMoves(self, r, c, moves):
        self.getRookMoves(r, c, moves)
        self.getBishopMoves(r, c, moves)

    '''
    Preia toate mutarile  regelui localizat in randul si coloana respectiva si creeaza mutari in lista
    '''
    def getKingMoves(self, r, c, moves):
        kingMoves = ((-1, 1), (-1, 0), (-1, 1), (0, -1), (0, 1 ), (1, -1), (1, 0), (1, 1))
        allyColor = "w" if self.whiteToMove else "b"
        for i in range(8):
            endRow = r + kingMoves[i][0]
            endCol = c + kingMoves[i][1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColor: #nu este o piesa aliata( spatiu gol sau piesa inamica)
                    moves.append(Move((r, c), (endRow, endCol), self.board))

class Move():
    # maps key to values
    # key : value
    #Creeam notarea in sah a tablei
    ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4,
                  "5": 3, "6": 2, "7": 1, "8":0}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}
    filesToCols = {"a":0, "b":1, "c":2, "d": 3,
                   "e": 4, "f": 5, "g": 6, "h": 7}
    colsToFiles = {v: k for k, v in filesToCols.items()}

    def __init__(self, startSq, endSq, board):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow *10 + self.endCol


    '''
    Overriding metodele =
    '''
    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False


    def getChessNotation(self):
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)

    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]

