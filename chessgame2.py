import pygame           
import pieces       #andere Datei aus gleichem Ordner
import os

pygame.init()



class ChessGame():
    def __init__(self): #soll später in "Einstelungen" veränderbar sein
        self.screen_color = pygame.Color('white')
        self.root = 8   #jedes Schachspiel 8x8 Feld
        self.FIELD_SIZE = 100
        self.piece_Size = self.FIELD_SIZE - self.FIELD_SIZE//8
        self.screen = pygame.display.set_mode((self.FIELD_SIZE*self.root, self.FIELD_SIZE*self.root))
        self.screen_rect = self.screen.get_rect()
        self.clock = pygame.time.Clock()
        self.done = False
        self.fps = 60.0
        self.board = []
        self.imageFolder = 'piecesImg'
        
        #themes
        self.themeCount = 0
        self.themeList = [[pygame.Color(229, 228, 197), pygame.Color(49, 96, 138), pygame.font.SysFont('monospace', self.piece_Size//4, bold=True)],
                          [pygame.Color(234, 235, 196), pygame.Color(109, 155, 79), pygame.font.SysFont('monospace', self.piece_Size//4, bold=True)],
                          [pygame.Color(240, 208, 160), pygame.Color(174, 114, 73), pygame.font.SysFont('monospace', self.piece_Size//4, bold=True)],
                          [pygame.Color(120, 119, 118), pygame.Color(86, 85, 84), pygame.font.SysFont('monospace', self.piece_Size//4, bold=True)],
                          [pygame.Color(193, 170, 190), pygame.Color(120, 60, 120), pygame.font.SysFont('monospace', self.piece_Size//4, bold=True, italic=True)]]
        self.colorB1 = pygame.Color(229, 228, 197)
        self.colorB2 = pygame.Color(49, 96, 138)
        self.font = pygame.font.SysFont('monospace', self.piece_Size//4, bold=True)
        self.lastmove = []
        self.lastmoveCol = [pygame.Color(162, 42, 42), pygame.Color(212, 140, 140)]
        
        #für die Züge
        self.legal_moves = []
        self.clickedPiece = None     
        self.moving = False
        
        #umwandlung
        self.umwandlung = False
        self.umwandlungRectsImg = []
        self.umwandlungsPos = None
        
        
        #die Figuren auf dem Brett 
        self.pieces_on_board = self.FENinterpreter('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR')     #rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR    - start FEN
        
        self.buildboard()   # baut das Board
    
    def buildboard(self):   # Funktion: baut das Board
        for i in range(1,9):
            for j in range(1,9):
                self.board.append((i,j))
            
    
    def checkColor(self, field):  # kontrolliert ob ein Feld (Bsp. (4,5)) W-white oder B-black ist
        if (field[0]+field[1])%2 == 0:
            return 'W'
        else:
            return 'B'
    
    
    def checkFree(self, field, color):   # überprüft ob das Feld frei ist von Figuren eigener Farbe
        for piece in self.pieces_on_board:
            if piece.pos == field:          #überprüft ob andere Figur auf dem Feld
                if piece.pieceColor == color:   #wenn figur von eigener Farbe
                    return False
                else:
                    return 'otherCol'       #wenn feld belegt von anderer Farbe dann Rückgabewert= 'otherCol'
        return True
    
    def isOnBoard(self, field):   # überprüft ob das Feld auf dem Brett ist
        x,y = field
        if x <= self.root and  x > 0 and y <= self.root and y > 0:
            return True
        else: 
            return False
    
    def checkMove(self, field, color):     # vereint die isOnboard und checkFree  #Todo: schach
        freeCheck = self.checkFree(field, color)
        onBoard = self.isOnBoard(field)
        if onBoard:                       # wernn feld auf dem brett soll es erbnis von checkFree zurück geben möglich: Tru/False/'otherCol'
            return freeCheck
        else: 
            return False
    
    def get_legal_moves(self,piece):  # fasst in liste(legal_moves) die züge aus moveSet der Pieces zusammen wenn diese checkmove Test standhalten
        piece.update_moveSet(self.pieces_on_board)
        checking_list_moves = piece.moveSet
        
        #ROCHADE -- schnittstelle schach
        if piece.pieceKind == 'King' and piece.moved == False:          
            if piece.pieceColor == 'W':  
                if self.checkFree((6,8), 'W') and self.checkFree((7,8), 'W'):
                    #kleine Rochade für weiß
                    for  i in self.pieces_on_board:
                        if i.pieceKind == 'Rock' and i.moved == False and i.pos == (8,8):
                            checking_list_moves.append([(2,0)])
                        
                if self.checkFree((2,8), 'W') and self.checkFree((3,8), 'W') and self.checkFree((4,8), 'W'):
                    #große Rochade für weiß
                    for  i in self.pieces_on_board:
                        if i.pieceKind == 'Rock' and i.moved == False and i.pos == (1,8):  
                            checking_list_moves.append([(-2,0)])
                    
            else:
                if self.checkFree((6,1), 'B') and self.checkFree((7,1), 'B'):
                    #kleine Rochade für schwart       
                    for  i in self.pieces_on_board:
                        if i.pieceKind == 'Rock' and i.moved == False and i.pos == (8,1):
                            checking_list_moves.append([(2,0)])
                        
                if self.checkFree((2,1), 'B') and self.checkFree((3,1), 'B') and self.checkFree((4,1), 'B'):
                    #große Rochade für schwarz
                    for  i in self.pieces_on_board:
                        if i.pieceKind == 'Rock' and i.moved == False and i.pos == (1,1):
                            checking_list_moves.append([(-2,0)])
        
        #*eigentliches getlegalmoves      
        for i in checking_list_moves:
            for j in i:
                move = piece.pos[0] + j[0], piece.pos[1] + j[1]
                resCheck = self.checkMove(move, piece.pieceColor)
                if resCheck == True:                #falls auf Brett und frei 
                    self.legal_moves.append(move)
                elif resCheck == 'otherCol':        #falls figur anderer Farbe auf Feld
                    self.legal_moves.append(move)       #soll das feld noch hinzufügen und dann abbrechen
                    break
                else:                   #abbrechen wenn nicht feld nicht auf dem Brett o. Figur eigener Farbe auf Feld
                    break
                        
    def move1(self):     # move beginn
        if not self.moving:
            for piece in self.pieces_on_board: 
                if self.getFieldfromPosition() == piece.pos:
                    self.clickedPiece = piece
                    self.get_legal_moves(piece)
                    if self.legal_moves != []: 
                        self.moving = True
                    
    
              
    def move2(self):        #  move Ende      
        posTar = self.getFieldfromPosition()                      
        if self.moving:
            for field in self.legal_moves:
                if posTar == field:
                    
                    #Rochade (Turmbewegung)
                    if self.clickedPiece.pieceKind == 'King':
                        if (self.clickedPiece.pos[0] - field[0]) == 2:      #große Rochade
    	                    for piece in self.pieces_on_board:
                                if piece.pieceColor == self.clickedPiece.pieceColor and piece.pieceKind == 'Rock' and piece.pos[0] == 1:
                                    piece.pos = (piece.pos[0] + 3, piece.pos[1])
            
                        elif self.clickedPiece.pos[0] - field[0] == -2:     #kleine Rochade
                            for piece in self.pieces_on_board:
                                if piece.pieceColor == self.clickedPiece.pieceColor and piece.pieceKind == 'Rock' and piece.pos[0] == 8:
                                    piece.pos = (piece.pos[0] - 2, piece.pos[1])

                    #En Passant
                    list_enpassant = []
                    if self.clickedPiece.pieceKind == 'Pawn':
                        if self.clickedPiece.pos[1] - field[1] == -2:                         #Schwarz mit Doppelzug -> führt zu möglichen En Passant für Weiß
                            for piece in self.pieces_on_board:                                                                          #Sucht nach einem möglichen weißen Piece, welches für En Passant in Frage kommen würde
                                if piece.pieceKind == 'Pawn' and piece.pieceColor == 'W' and piece.pos == (field[0] + 1, field[1]):     #Weiß schlägt schräg nach oben links über den schwarzen Bauer
                                    piece.enPassant = 1
                                    list_enpassant.append((field[0] + 1, field[1]))
                                elif piece.pieceKind == 'Pawn' and piece.pieceColor == 'W' and piece.pos == (field[0] - 1, field[1]):   #Weiß schlägt schräg nach oben rechts über den schwarzen Bauer
                                    piece.enPassant = -1
                                    list_enpassant.append((field[0] - 1, field[1]))
                        
                                
                        elif self.clickedPiece.pos[1] - field[1] == 2:                        #Weiß mit Doppelzug -> führt zu möglichen En Passant für Schwarz
                            for piece in self.pieces_on_board:                                                                          #Sucht nach einem möglichen schwarzen Piece , welches für En Passant in Frage kommen würde
                                if piece.pieceKind == 'Pawn' and piece.pieceColor == 'B' and piece.pos == (field[0] + 1, field[1]):     #Schwarz schlägt schräg nach unten links unter den weißen Bauer
                                    piece.enPassant = 1
                                    list_enpassant.append((field[0] + 1, field[1]))
                                elif piece.pieceKind == 'Pawn' and piece.pieceColor == 'B' and piece.pos == (field[0] - 1, field[1]):   #Schwarz schlägt schräg nach unten rechts unter den weißen Bauer
                                    piece.enPassant = -1
                                    list_enpassant.append((field[0] - 1, field[1]))

                        if  self.clickedPiece.enPassant != None and field == (self.clickedPiece.pos[0] - self.clickedPiece.enPassant, self.clickedPiece.pos[1] + self.clickedPiece.moveSet[0][0][1]):
                            for piece in self.pieces_on_board:
                                if piece.pos == (self.clickedPiece.pos[0] - self.clickedPiece.enPassant, self.clickedPiece.pos[1]):
                                    self.pieces_on_board.remove(piece) 
                            self.clickedPiece.enPassant = None
                    
                        #umwandlung
                        if field[1] == 1 and self.clickedPiece.pieceColor == 'W':
                            self.umwandlungMeth1(field)
                        elif field[1] == 8 and self.clickedPiece.pieceColor == 'B':
                            self.umwandlungMeth1(field)
                    ########################################################################     
                    for piece in self.pieces_on_board:
                        if piece.pieceKind == 'Pawn' and piece.pos not in list_enpassant:   #en passant Recht entzogen falls anderer Zug getätigt    
                            piece.enPassant = None   
                        if piece.pos == posTar:
                            self.pieces_on_board.remove(piece) # schlagen

                    self.lastmove = [self.clickedPiece.pos, field] #last move nur für darstellung 
                    
                    self.clickedPiece.pos = field   #eigentlicher Zug
                    #reset nach zug
                    self.clickedPiece = None
                    self.legal_moves = []
                    self.moving = False
            
            
            if self.clickedPiece and posTar != self.clickedPiece.pos:      
                #reset nach click auf anderes Feld
                self.clickedPiece = None
                self.legal_moves = []
                self.moving = False
            
            
    
    #1. Part der Umwandlung, ausgeführt sobald Buaer auf letzter Reihe, bereitet Liste und Pos vor
    def umwandlungMeth1(self, move):
        self.umwandlung = True
        x, y = move 
        if x == 1:
            x += 1
        elif x == 8:
            x -= 0.5
        x *= self.piece_Size
        y *= self.piece_Size
        color = self.clickedPiece.pieceColor
        umwandlungList = [[pygame.image.load(os.path.join(self.imageFolder,f'Queen_{color}.png')), pieces.Queen('Queen', color, move)],
                                    [pygame.image.load(os.path.join(self.imageFolder,f'Rock_{color}.png')), pieces.Rock('Rock', color, move)],
                                    [pygame.image.load(os.path.join(self.imageFolder,f'Bishop_{color}.png')), pieces.Bishop('Bishop', color, move)],
                                    [pygame.image.load(os.path.join(self.imageFolder,f'Knight_{color}.png')), pieces.Knight('Knight', color, move)]]
        count = 2
        for i in umwandlungList:
            i[0] = pygame.transform.scale(i[0], (self.piece_Size,self.piece_Size))
            rect = pygame.Rect(x - self.piece_Size*count, y, self.piece_Size, self.piece_Size)
            count -= 1
            i.append(rect)
        
        self.umwandlungsPos = move
        self.umwandlungRectsImg = umwandlungList
     
    #2. Part der Umwandlung; führt die Auswahl aus und wandelt das Piece um          
    def umwandlungMeth2(self):
        x,y = pygame.mouse.get_pos()
        for i in self.umwandlungRectsImg:
            if (x > i[2].x and y > i[2].y) and (x < i[2].x + i[2].width and y < i[2].y+i[2].height):
                for j in self.pieces_on_board:
                    if j.pos == self.umwandlungsPos:
                        self.pieces_on_board.remove(j)
                        self.pieces_on_board.append(i[1])
                        self.umwandlung = False
    
    #3.Part der Umwandlung, macht sie sichtbar
    def drawUmwandlung(self):
        for i in self.umwandlungRectsImg:
            self.screen.fill(pygame.Color(223, 213, 213), i[2])
            pygame.draw.rect(self.screen, pygame.Color(78, 78, 78), i[2], 1)
            self.screen.blit(i[0], i[2])
                
    def FENinterpreter(self, FENstring):    #übersetzt FEN Notation
        pieceList = []
        rows = FENstring.split('/')
        isInt = False
        for i in range(1,9):
            count = 1
            for j in rows[i-1]:
                try:
                    int(j)
                    count += int(j)
                    isInt = True
                except ValueError:
                    isInt = False
                
                if not isInt:
                    if j == 'r':
                        pieceList.append(pieces.Rock('Rock', 'B', (count,i)))
                    if j == 'R':
                        pieceList.append(pieces.Rock('Rock', 'W', (count,i)))
                    if j == 'n':
                        pieceList.append(pieces.Knight('Knight', 'B', (count,i)))
                    if j == 'N':
                        pieceList.append(pieces.Knight('Knight', 'W', (count,i)))
                    if j == 'b':
                        pieceList.append(pieces.Bishop('Bishop', 'B', (count,i)))
                    if j == 'B':
                        pieceList.append(pieces.Bishop('Bishop', 'W', (count,i)))
                    if j == 'q':
                        pieceList.append(pieces.Queen('Queen', 'B', (count,i)))
                    if j == 'Q':
                        pieceList.append(pieces.Queen('Queen', 'W', (count,i)))
                    if j == 'k':
                        pieceList.append(pieces.King('King', 'B', (count,i)))
                    if j == 'K':
                        pieceList.append(pieces.King('King', 'W', (count,i)))
                    if j == 'p':
                        pieceList.append(pieces.Pawn('Pawn', 'B', (count,i)))
                    if j == 'P':
                        pieceList.append(pieces.Pawn('Pawn', 'W', (count,i)))
                        
                    count += 1   
        return pieceList     
    
    def getFieldfromPosition(self): #übersetzt mouseposition in Feld 
        x,y = pygame.mouse.get_pos()
        x += self.FIELD_SIZE
        y += self.FIELD_SIZE
        return round(x//self.FIELD_SIZE),round(y//self.FIELD_SIZE)
    
    def drawBoard(self): # malt das Brett auf den Screen
        color1 = self.colorB1
        color2 = self.colorB2
        borderColor = pygame.Color('burlywood4')
        
        for i in self.board:
            x,y = i
            abc = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
            x = (x-1)*self.FIELD_SIZE
            y = (y-1)*self.FIELD_SIZE
            fontStr = str(i).replace('(', ' ').replace(')', ' ')
            if self.checkColor(i) == 'W':
                self.screen.fill(color1, pygame.Rect(x, y, self.FIELD_SIZE, self.FIELD_SIZE))
            else:
                self.screen.fill(color2, pygame.Rect(x, y, self.FIELD_SIZE, self.FIELD_SIZE))
                
        count = 7
        for i in range(1,9):
            fontImg = self.font.render(abc[i-1], True, pygame.Color('black'))
            fontImg2 = self.font.render(str(i), True, pygame.Color('black'))
            self.screen.blit(fontImg, ((self.FIELD_SIZE*i - fontImg.get_width() - self.FIELD_SIZE//15), self.FIELD_SIZE*8 - fontImg.get_height()))
            self.screen.blit(fontImg2, (self.FIELD_SIZE//20, self.FIELD_SIZE*count + self.FIELD_SIZE//10))
            count -= 1
            
        #! Themes sollen einstellbar sein
    
    def drawPieces(self):   #malt die Pieces auf den screen
        for piece in self.pieces_on_board:
            clickedHighlightSize = self.piece_Size + 10
            x,y = piece.pos
            x = (x-1)*self.FIELD_SIZE
            y = (y-1)*self.FIELD_SIZE
            if piece == self.clickedPiece:
                img = pygame.transform.scale(piece.pieceImg, (clickedHighlightSize, clickedHighlightSize))
                self.screen.blit(img, (x + self.FIELD_SIZE//2 - clickedHighlightSize//2, y + self.FIELD_SIZE//2 - clickedHighlightSize//2))
            else:
                img = pygame.transform.scale(piece.pieceImg, (self.piece_Size,self.piece_Size))
                self.screen.blit(img, (x + self.FIELD_SIZE//2 - self.piece_Size//2, y + self.FIELD_SIZE//2 - self.piece_Size//2))
    
    def draw_move(self):    #visuelle darstellung des Zuges
        for i in self.legal_moves:
            x,y = i
            x = (x-1)*self.FIELD_SIZE
            y = (y-1)*self.FIELD_SIZE
            pygame.draw.circle(self.screen, pygame.Color('darkgoldenrod2'), [x + self.FIELD_SIZE//2, y + self.FIELD_SIZE//2], self.FIELD_SIZE//6, 0)    #! noch verändern!!: ist nicht  abhängig von FIELD_SIZE
            
    def drawLastMove(self): #visuelle darstellung des letzten Zuges
        if self.lastmove != []:
            for i in range(2):
                x,y = self.lastmove[i]
                x = (x-1)*self.FIELD_SIZE
                y = (y-1)*self.FIELD_SIZE
                self.screen.fill(self.lastmoveCol[i], pygame.Rect(x, y, self.FIELD_SIZE, self.FIELD_SIZE))
    
    def wechsleTheme(self):
        if self.themeCount >= len(self.themeList) - 1:
            self.themeCount = 0
            self.colorB1 = self.themeList[self.themeCount][0]
            self.colorB2 = self.themeList[self.themeCount][1]
            self.font = self.themeList[self.themeCount][2]
        else:
            self.themeCount += 1
            self.colorB1 = self.themeList[self.themeCount][0]
            self.colorB2 = self.themeList[self.themeCount][1]
            self.font = self.themeList[self.themeCount][2]
    
    def event_loop(self):   #eventloop - reagiert auf keys und mouse
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.done = True
            if event.type == pygame.MOUSEBUTTONDOWN:  
                if not self.umwandlung: 
                    self.move1()
                    self.move2()
                else: 
                    self.umwandlungMeth2()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:     #reset zu folgendem FEN-string
                    self.pieces_on_board = self.FENinterpreter('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR')
                if event.key == pygame.K_t:     #reset zu folgendem FEN-string
                    self.wechsleTheme()
                        
                    
                                              
    def main_loop(self):    #fasst draw methoden zusammen
        while not self.done:
            
            self.clock.tick(self.fps)
            self.screen.fill(self.screen_color)
            self.drawBoard()
            self.drawLastMove()
            self.drawPieces()
            if self.moving: self.draw_move()
            if self.umwandlung: self.drawUmwandlung()
            
            self.event_loop()
            
            
            
            
            pygame.display.update() 
            


b = ChessGame()
b.main_loop()

#Todo: unterschiedliche Themes
#Todo: doppelzug soll nicht schlagen
#Todo: macht den blöden Code schön
#Todo: Schach
#Todo: Fesslung
#Todo: Hashmap anstatt pieces_on_board list
#Todo: derzeitige Partie in FEN

