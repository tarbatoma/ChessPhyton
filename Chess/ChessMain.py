"""
Acesta este fisierul driver. Se va ocupa de inputul utilizatorului si afisarea GameState-ului
"""

import pygame as p
from Chess import ChessEngine

WIDTH = HEIGHT = 512 # 512 este putere de 2 si se imparte bine cu 2
DIMENSION = 8 # dimensiunea tablei de sah este de 8x8
SQ__SIZE = HEIGHT // DIMENSION  #Square size
MAX_FPS = 15 # pentru animatii mai tarziu
IMAGES = {}

'''
Vom initializa un dictionar global de imagini. Va fi accesat doar o data in main si stocat
'''

def loadImages():
    pieces = ['wp','wR', 'wN', 'wB', 'wK', 'wQ', 'bp', 'bR', 'bN', 'bB', 'bK', 'bQ']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"), (SQ__SIZE, SQ__SIZE))
        #Nota: putem accesa o imagine folosing dictionarul  folosing 'Images['wp']'
    '''
    Main driver care va manipula user input si grafica
    '''
def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = ChessEngine.GameState()
    validMoves = gs.getValidMoves() #stocam intr-o lista si cand un user creeaza o lista vedem ce miscare a facut userului si vedem daca este o miscare valida astfel nu vom putea efectua mutarea
    moveMade = False #flag variable atunci cand o miscare este efectuata
    loadImages() # o faci doar o data, inainte de loop-ul while
    running = True
    sqSelected = () # nici un patrat nu este selectat initial, urmareste ultimul click al userului(este un tuplu row , col)
    playerClicks = [] #urmareste click-ul player-ului (compus din 2xTuplu [(6, 4), (4, 4)]
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            #mouse handler
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos() #(x, y) locatia mouse-ului// nu ne facem griji ca ar iesii din cadru deoarece board-ul este tot screen-ul
                col =location[0]//SQ__SIZE
                row = location[1]//SQ__SIZE
                if sqSelected == (row,col): #userul a dat click pe accelasi patratel
                    sqSelected = () #deselectam piesa
                    playerClicks = [] #golim playerClicks
                else:
                    sqSelected = (row, col)
                    playerClicks.append(sqSelected) #stocam primul click si al 2-lea
                if len(playerClicks) == 2: #inseamna ca este dupa al 2-lea click
                    move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                    print(move.getChessNotation())
                    if move in validMoves: #verificam daca mutarea se afla in lista de mutari valide
                        gs.makeMove(move)
                        moveMade = True
                        sqSelected = () #resetam click-urile userului
                        playerClicks = []
                    else:
                        playerClicks = [sqSelected]
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z: #undo cand 'Z' este apasat
                    gs.undoMove()
                    moveMade = True

        if moveMade:
            validMoves = gs.getValidMoves()
            moveMade= False

        drawGameState(screen, gs)  # problema de neafisare a patratelor
        clock.tick(MAX_FPS)
        p.display.flip()



'''
Se ocupa de toate graficele in curent game state
'''
def drawGameState(screen, gs):
    drawBoard(screen) #o da deseneze patratele pe tabla
    #adaugam highlight la piese (mai tarziu)
    drawPieces(screen, gs.board) #deseneaza piesele deasupra patratelor

'''
Desenam patratele pe tabla, tot timpul cel din stanga o sa fie alb
'''
def drawBoard(screen):
    colors = [p.Color("white"), p.Color("gray")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color= colors[ ( ( r + c ) % 2) ]
            p.draw.rect(screen, color, p.Rect(c * SQ__SIZE, r * SQ__SIZE, SQ__SIZE, SQ__SIZE))

'''
Desenam piesele pe tabla folosind GameState.board
'''
def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--":
                screen.blit(IMAGES[piece], p.Rect(c * SQ__SIZE, r * SQ__SIZE, SQ__SIZE, SQ__SIZE))

if __name__ == "__main__":
    main()

