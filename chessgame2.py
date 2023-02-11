import pygame           
import pieces       #andere Datei aus gleichem Ordner

pygame.init()



class ChessGame():
    def __init__(self): #soll später in "Einstelungen" veränderbar sein
        self.screen_color = pygame.Color('white')
        self.root = 8   #jedes Schachspiel 8x8 Feld
        self.FIELD_SIZE = 100   
        self.piece_Size = self.FIELD_SIZE - 10
        self.screen = pygame.display.set_mode((self.FIELD_SIZE*self.root, self.FIELD_SIZE*self.root))
        self.screen_rect = self.screen.get_rect()
        self.clock = pygame.time.Clock()
        self.done = False
        self.fps = 60.0
        self.board = []
        self.font = pygame.font.SysFont(None, self.FIELD_SIZE//2)
        
        #für die Züge
        self.legal_moves = []
        self.clickedPiece = None     
        self.moving = False
        
        
        
        #die Figuren auf dem Brett 
        self.pieces_on_board = [
            pieces.Rock('Rock', 'B', (1,1)), 
            pieces.Knight('Knight', 'B',(2,1)),
            pieces.Bishop('Bishop', 'B',(3,1)),
            pieces.Queen('Queen', 'B',(4,1)),
            pieces.King('King', 'B',(5,1)),
            pieces.Bishop('Bishop', 'B',(6,1)),
            pieces.Knight('Knight', 'B',(7,1)),
            pieces.Rock('Rock', 'B',(8,1)),
            pieces.Pawn('Pawn', 'B',(1,2)),
            pieces.Pawn('Pawn', 'B',(2,2)),
            pieces.Pawn('Pawn', 'B',(3,2)),
            pieces.Pawn('Pawn', 'B',(4,2)),
            pieces.Pawn('Pawn', 'B',(5,2)),
            pieces.Pawn('Pawn', 'B',(6,2)),
            pieces.Pawn('Pawn', 'B',(7,2)),
            pieces.Pawn('Pawn', 'B',(8,2)),
            pieces.Pawn('Pawn', 'W',(1,7)),
            pieces.Pawn('Pawn', 'W',(2,7)),
            pieces.Pawn('Pawn', 'W',(3,7)),
            pieces.Pawn('Pawn', 'W',(4,7)),
            pieces.Pawn('Pawn', 'W',(5,7)),
            pieces.Pawn('Pawn', 'W',(6,7)),
            pieces.Pawn('Pawn', 'W',(7,7)),
            pieces.Pawn('Pawn', 'W',(8,7)),
            pieces.Rock('Rock', 'W',(1,8)),
            pieces.Knight('Knight', 'W',(2,8)),
            pieces.Bishop('Bishop', 'W',(3,8)),
            pieces.Queen('Queen', 'W',(4,8)),
            pieces.King('King', 'W',(5,8)),
            pieces.Bishop('Bishop', 'W',(6,8)),
            pieces.Knight('Knight', 'W',(7,8)),
            pieces.Rock('Rock', 'W',(8,8))]
        
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
            if piece.pos == field and piece.pieceColor == color:
                return False
        return True
    
    def isOnBoard(self, field):   # überprüft ob das Feld auf dem Brett ist
        x,y = field
        if x <= self.root and  x > 0 and y <= self.root and y > 0:
            return True
        else: 
            return False
    
    def checkMove(self, field, color):     # vereint die isOnboard und checkFree
        if self.checkFree(field, color) and self.isOnBoard(field): 
            return True
        else: 
            return False
    
    def get_legal_moves(self,pos):  # fasst in liste(legal_moves) die züge aus moveSet der Pieces zusammen wenn diese checkmove Test standhalten
        for piece in self.pieces_on_board:
            if piece.pos == pos:
                for i in piece.moveSet:
                    move = piece.pos[0] + i[0], piece.pos[1] + i[1]
                    if self.checkMove(move, piece.pieceColor):
                        self.legal_moves.append(move)
                        
    def move1(self):     # move beginn
        if not self.moving:
            for piece in self.pieces_on_board: 
                if self.getFieldfromPosition() == piece.pos:
                    self.clickedPiece = piece
                    self.get_legal_moves(piece.pos)
                    if self.legal_moves != []: self.moving = True
                
    
              
    def move2(self):        #  move Ende      
        posTar = self.getFieldfromPosition()                      
        if self.moving:
            for field in self.legal_moves:
                if posTar == field:
                    for piece1 in self.pieces_on_board:      # schlagen
                        if piece1.pos == posTar:
                            self.pieces_on_board.remove(piece1)
                    self.clickedPiece.pos = field
                    
                    #reset
                    self.clickedPiece = None
                    self.legal_moves = []
                    self.moving = False
    
    
                
                
    
    def getFieldfromPosition(self): #übersetzt mouseposition in Feld 
        x,y = pygame.mouse.get_pos()
        x += self.FIELD_SIZE
        y += self.FIELD_SIZE
        return round(x//self.FIELD_SIZE),round(y//self.FIELD_SIZE)
    
    def drawBoard(self): # malt das Brett auf den Screen
        color1 = pygame.Color('lightgrey')
        color2 = pygame.Color('skyblue3')
        
        for i in self.board:
            x,y = i
            x = (x-1)*self.FIELD_SIZE
            y = (y-1)*self.FIELD_SIZE
            fontStr = str(i).replace('(', ' ').replace(')', ' ')
            if self.checkColor(i) == 'W':
                self.screen.fill(color1, pygame.Rect(x, y, self.FIELD_SIZE, self.FIELD_SIZE))
                fontImg = self.font.render(fontStr, True, pygame.Color('darkslategray'))
                self.screen.blit(fontImg, (x+ self.FIELD_SIZE//2 - fontImg.get_width()//2, y+ self.FIELD_SIZE//2 - fontImg.get_height()//2))
            else:
                self.screen.fill(color2, pygame.Rect(x, y, self.FIELD_SIZE, self.FIELD_SIZE))
                fontImg = self.font.render(fontStr, True, pygame.Color('darkslategray'))
                self.screen.blit(fontImg, (x+ self.FIELD_SIZE//2 - fontImg.get_width()//2, y+ self.FIELD_SIZE//2 - fontImg.get_height()//2))
    
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
            
    
    
    
    def event_loop(self):   #eventloop - reagiert auf keys und mouse
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.done = True
            if event.type == pygame.MOUSEBUTTONDOWN:    #! hier zug einfügen
                self.move1()
                self.move2()
                
                
                
            
                        
                                       
    def main_loop(self):    #fasst draw methoden zusammen
        while not self.done:
            
            self.clock.tick(self.fps)
            self.screen.fill(self.screen_color)
            self.drawBoard()
            self.drawPieces()
            if self.moving: self.draw_move()
        
            
            self.event_loop()
            
            
            
            
            pygame.display.update() 
            


b = ChessGame()
b.main_loop()



#Todo: Wie reagiern auf pinned Pieces und Schach
#Todo: legalmoves: was wenn was dazwischen
#Todo: Pawn soll schräg schlagen + wenn auf 2.Reihe zwei FeldZug + en passant
