import pygame           
import pieces1       #andere Datei aus gleichem Ordner
import os
import time

pygame.init()



class ChessGame():
    def __init__(self): #soll später in "Einstelungen" veränderbar sein
        self.screen_color = pygame.Color('white')
        self.root = 8   #jedes Schachspiel 8x8 Feld
        self.FIELD_SIZE = 100
        self.piece_Size = self.FIELD_SIZE - self.FIELD_SIZE//8
        self.screen = pygame.display.set_mode((self.FIELD_SIZE*self.root + self.FIELD_SIZE, self.FIELD_SIZE*self.root))
        self.screen_rect = self.screen.get_rect()
        self.clock = pygame.time.Clock()
        self.done = False
        self.fps = 60.0
        self.amZug = 'W' #Weiß am Zug
        self.imageFolder = 'piecesImg'
        self.lastmove = []
        
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
        self.lastmoveCol = [pygame.Color(162, 42, 42), pygame.Color(212, 140, 140)]
        
        #für die Züge
        self.legal_moves = []  
        self.currentMove = []
        
        #umwandlung
        self.umwandlung = False
        self.umwandlungRectsImg = []
        self.umwandlungsPos = None
        
        #punkte berechnung
        self.punkteDiff = 0 

        #die Figuren auf dem Brett 
        self.boardDict = self.FENinterpreter('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR')     #rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR    - start FEN
        self.whitePositions = []
        self.blackPositions = []
        
        self.setup_figureList()
    
    def setup_figureList(self):
        self.whitePositions = []
        self.blackPositions = []
        for i in self.boardDict.keys():
            if self.boardDict[i] != None:
                if self.boardDict[i].pieceColor == 'W':
                    self.whitePositions.append(i)
                else:
                    self.blackPositions.append(i)
            
    def switchAmZug(self): #Wechselt spielende Seiten
        if self.amZug == 'W':
            self.amZug = 'B'
        else:
            self.amZug = 'W'
        
            
    
    def checkColor(self, field):  # kontrolliert ob ein Feld (Bsp. (4,5)) W-white oder B-black ist
        if (field[0]+field[1])%2 == 0:
            return 'W'
        else:
            return 'B'
    
    
    def checkFree(self, field, color):   # überprüft ob das Feld frei ist von Figuren eigener Farbe
        if self.boardDict[field] == None:          #überprüft ob andere Figur auf dem Feld
            return True
        elif self.boardDict[field].pieceColor == color:   #wenn figur von eigener Farbe
            return False
        else:
            return 'otherCol'       #wenn feld belegt von anderer Farbe dann Rückgabewert= 'otherCol'
        
    
    def isOnBoard(self, field):   # überprüft ob das Feld auf dem Brett ist
        if field in self.boardDict:
            return True
        else: 
            return False
    
    def checkMove(self, field, color):     # vereint die isOnboard und checkFree  #Todo: schach
        if self.isOnBoard(field):                       # wernn feld auf dem brett soll es erbnis von checkFree zurück geben möglich: Tru/False/'otherCol'
            return self.checkFree(field, color)
        else: 
            return False
    
    def get_legal_moves(self, field):  # fasst in liste(legal_moves) die züge aus moveSet der Pieces zusammen wenn diese checkmove Test standhalten
        piece = self.boardDict[field]
        if piece.pieceColor == self.amZug:
            piece.reset_moveSet()
            checking_list_moves = piece.moveSet
    
            if piece.pieceKind == 'King': checking_list_moves = self.getMovesKing(field)
            if piece.pieceKind == 'Pawn': checking_list_moves = self.getMovesPawn(field)
            
            #*eigentliches getlegalmoves      
            for i in checking_list_moves:
                for j in i:
                    move = field[0] + j[0], field[1] + j[1]
                    resCheck = self.checkMove(move, piece.pieceColor)
                    if resCheck == True:                #falls auf Brett und frei 
                        self.legal_moves.append(move)
                    elif resCheck == 'otherCol':        #falls figur anderer Farbe auf Feld
                        self.legal_moves.append(move)       #soll das feld noch hinzufügen und dann abbrechen
                        break
                    else:                   #abbrechen wenn nicht feld nicht auf dem Brett o. Figur eigener Farbe auf Feld
                        break
    
    #* legal Moves for Pawn:
    def getMovesPawn(self, field):
        pawn = self.boardDict[field]
        checking_list_moves = pawn.moveSet
        
        #doubleMove
        if pawn.pieceColor == 'W' and field[1] == 7 and self.checkMove((field[0], field[1] - 2), 'W') == True:
            checking_list_moves[0].append((0,-2))
        if pawn.pieceColor == 'B' and field[1] == 2 and self.checkMove((field[0], field[1] + 2), 'B') == True:
            checking_list_moves[0].append((0,2))

        #schlagen
        if self.checkMove((field[0] + 1, field[1]+pawn.moveSet[0][0][1]), pawn.pieceColor) == 'otherCol':
            checking_list_moves.append([(1, pawn.moveSet[0][0][1])])
        if self.checkMove((field[0] - 1, field[1]+pawn.moveSet[0][0][1]), pawn.pieceColor) == 'otherCol':
            checking_list_moves.append([(-1, pawn.moveSet[0][0][1])])
        
        #enpassant
        if pawn.enPassant:
            checking_list_moves.append([(pawn.enPassant, pawn.moveSet[0][0][1])])
              
        #blockiert
        if self.checkMove((field[0], field[1]+pawn.moveSet[0][0][1]), pawn.pieceColor) != True:
            checking_list_moves.remove(checking_list_moves[0])

        return checking_list_moves
        
    #* legalmoves for King
    def getMovesKing(self, field):
        king = self.boardDict[field]
        checking_list_moves = king.moveSet
        #Rochade
        
        if king.moved == False:      
            if king.pieceColor == 'W':  
                if self.checkFree((6,8), 'W') and self.checkFree((7,8), 'W'):
                    #kleine Rochade für weiß
                    rockRoch = self.boardDict[(8,8)]
                    if rockRoch != None and rockRoch.pieceKind == 'Rock' and rockRoch.moved == False :
                        checking_list_moves.append([(2,0)])
                        
                if self.checkFree((2,8), 'W') and self.checkFree((3,8), 'W') and self.checkFree((4,8), 'W'):
                    #große Rochade für weiß
                    rockRoch = self.boardDict[((1,8))]
                    if rockRoch != None and rockRoch.pieceKind == 'Rock' and rockRoch.moved == False:  
                        checking_list_moves.append([(-2,0)])
                    
            else:
                if self.checkFree((6,1), 'B') and self.checkFree((7,1), 'B'):
                    #kleine Rochade für schwart       
                    rockRoch = self.boardDict[(8,1)]
                    if rockRoch != None and rockRoch.pieceKind == 'Rock' and rockRoch.moved == False:
                        checking_list_moves.append([(2,0)])
                        
                if self.checkFree((2,1), 'B') and self.checkFree((3,1), 'B') and self.checkFree((4,1), 'B'):
                    #große Rochade für schwarz
                    rockRoch = self.boardDict[(1,1)]
                    if rockRoch != None and rockRoch.pieceKind == 'Rock' and rockRoch.moved == False:
                        checking_list_moves.append([(-2,0)])
           
         
        return checking_list_moves       
                
    def moveChoice(self):     # move beginn --- !für Mensch --------
        if len(self.currentMove) == 1:
            clickedField = self.getFieldfromPosition()
            if self.isOnBoard(clickedField):
                self.currentMove.append(clickedField)
                
        if self.currentMove == []:
            clickedField = self.getFieldfromPosition()
            if self.isOnBoard(clickedField) and self.boardDict[clickedField] != None:
                self.get_legal_moves(clickedField)
                self.rootSquare = clickedField
                if self.legal_moves != []: 
                    self.currentMove.append(clickedField)
                
         
        
                    
    
              
    def makeMove(self, move):        #  move Ende                   
        if len(move) == 2:
            rootField = move[0]
            posTar = move[1]
            clickedPiece = self.boardDict[rootField]
            for field in self.legal_moves:
                if posTar == field:
                    self.lastmove = []  
                    
                    if clickedPiece.pieceKind == 'King':
                        #Rochade (Turmbewegung)
                        if (rootField[0] - field[0]) == 2:      #große Rochade
                            rockField = 1,rootField[1]
                            rockRoch = self.boardDict[rockField]
                            if rockRoch != None  and rockRoch.pieceKind == 'Rock' and rockRoch.pieceColor == clickedPiece.pieceColor:
                                self.lastmove.append((rockField, rockRoch)) #undo
                                self.lastmove.append(((rockField[0] + 3, rockField[1]), None)) #undo
                                if rockRoch.pieceColor == 'W': #Figurlist
                                    self.whitePositions.remove(rockField)
                                    self.whitePositions.append((rockField[0] + 3, rockField[1]))
                                else:
                                    self.blackPositions.remove(rockField)
                                    self.blackPositions.append((rockField[0] + 3, rockField[1]))
                                self.boardDict.update({(rockField[0] + 3, rockField[1]): rockRoch})
                                self.boardDict.update({rockField: None})
                                
            
                        elif (rootField[0] - field[0]) == -2:     #kleine Rochade
                            rockField = 8,rootField[1]
                            rockRoch = self.boardDict[rockField]
                            if rockRoch != None and rockRoch.pieceKind == 'Rock' and rockRoch.pieceColor == clickedPiece.pieceColor:
                                self.lastmove.append((rockField, rockRoch))  #undo
                                self.lastmove.append(((rockField[0] - 2, rockField[1]), None)) #undo
                                if rockRoch.pieceColor == 'W': #Figurlist
                                    self.whitePositions.remove(rockField)
                                    self.whitePositions.append((rockField[0] - 2, rockField[1]))
                                else:
                                    self.blackPositions.remove(rockField)
                                    self.blackPositions.append((rockField[0] - 2, rockField[1]))
                                self.boardDict.update({(rockField[0] - 2, rockField[1]): rockRoch})
                                self.boardDict.update({rockField: None})
                    
                    #Pawn
                    if clickedPiece.pieceKind == 'Pawn':
                    
                        #Enpassant wenn Doublemove - pawn enpassant zugewiesen
                        if (field[1] - rootField[1] == -2) or (field[1] - rootField[1] == 2):
                            enPassantPawn = self.boardDict[field[0]+1,field[1]] if self.isOnBoard((field[0]+1,field[1])) else None
                            if enPassantPawn != None and enPassantPawn.pieceKind == 'Pawn' and enPassantPawn.pieceColor != clickedPiece.pieceColor:
                                enPassantPawn.enPassant = -1
                                
                            enPassantPawn = self.boardDict[field[0]-1,field[1]] if self.isOnBoard((field[0]-1,field[1])) else None
                            if enPassantPawn != None and enPassantPawn.pieceKind == 'Pawn' and enPassantPawn.pieceColor != clickedPiece.pieceColor:
                                enPassantPawn.enPassant = 1 
                                
                        #enpassant schlagen
                        if clickedPiece.enPassant:
                            if field[0] - rootField[0] == clickedPiece.enPassant:
                                if clickedPiece.pieceColor == 'W':
                                    enPassantSchlag = (field[0], field[1] + 1)
                                    self.lastmove.append((enPassantSchlag, self.boardDict[enPassantSchlag]))
                                    self.boardDict.update({enPassantSchlag : None})
                                    self.blackPositions.remove(enPassantSchlag)
                                else:
                                    enPassantSchlag = (field[0], field[1] + 1)
                                    self.lastmove.append((enPassantSchlag, self.boardDict[enPassantSchlag]))
                                    self.boardDict.update({enPassantSchlag : None})
                                    self.whitePositions.remove(enPassantSchlag)
                                    
                        #umwandlung
                        if field[1] == 1 and clickedPiece.pieceColor == 'W':
                            self.umwandlungMeth1(field)
                        elif field[1] == 8 and clickedPiece.pieceColor == 'B':
                            self.umwandlungMeth1(field)
                            
                    ########################################################################     
                    schlagPiece = self.boardDict[posTar]
                    if schlagPiece != None:
                        if self.amZug == 'B':
                            self.whitePositions.remove(posTar)
                        else:
                            self.blackPositions.remove(posTar)
                        self.punkteBerechnungSchlag(schlagPiece)
                    
                    
                    self.lastmove.append((rootField, clickedPiece)) #für UndoMove 
                    self.lastmove.append((posTar, schlagPiece)) #für UndoMove 
                    print(self.lastmove)
                    
                    #*eigentlicher Zug
                    self.boardDict.update({posTar : clickedPiece})
                    self.boardDict.update({rootField : None})
                    
                    if self.amZug == 'W':
                        self.whitePositions.remove(rootField)
                        self.whitePositions.append(posTar)
                    else:
                        self.blackPositions.remove(rootField)
                        self.blackPositions.append(posTar)
                    
                    
                    if clickedPiece.pieceKind == 'Rock':
                        clickedPiece.moved = True
                    
                    if clickedPiece.pieceKind == 'King':
                        clickedPiece.moved = True
                    
                    #reset nach zug
                    self.currentMove = []
                    self.legal_moves = []
                    self.switchAmZug()    #später wieder reinnehemn
            
           
                  
            #reset nach click auf anderes Feld
            self.legal_moves = []
            self.currentMove = []
            
    
    
    #Methode um letztem Zug zurückzunehmen
    def undoMove(self):
        if self.lastmove != []:
            self.switchAmZug() 
            
            for i in self.lastmove:    
                self.boardDict.update({i[0] : i[1]})
            
            self.setup_figureList()
                
            self.lastmove = []
            self.legal_moves = []
            
    
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
        color = self.boardDict[self.currentMove[0]].pieceColor
        umwandlungList = [[pygame.image.load(os.path.join(self.imageFolder,f'Queen_{color}.png')), pieces1.Queen('Queen', color)],
                                    [pygame.image.load(os.path.join(self.imageFolder,f'Rock_{color}.png')), pieces1.Rock('Rock', color)],
                                    [pygame.image.load(os.path.join(self.imageFolder,f'Bishop_{color}.png')), pieces1.Bishop('Bishop', color)],
                                    [pygame.image.load(os.path.join(self.imageFolder,f'Knight_{color}.png')), pieces1.Knight('Knight', color)]]
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
                self.boardDict.update({self.umwandlungsPos : i[1]})
                self.punkteBerechnungUmwand(i[1])
                self.umwandlung = False
    
    #3.Part der Umwandlung, macht sie sichtbar
    def drawUmwandlung(self):
        for i in self.umwandlungRectsImg:
            self.screen.fill(pygame.Color(223, 213, 213), i[2])
            pygame.draw.rect(self.screen, pygame.Color(78, 78, 78), i[2], 1)
            self.screen.blit(i[0], i[2])
            
    #punkteberechnung 
    def punkteBerechnungSchlag(self, piece):
        color = piece.pieceColor
        if color == 'B': #Wenn schwarzes Piece geschlagen
            self.punkteDiff += piece.points     #Weiß bekommt punkte dazu (+)
        else:                       #Wenn weißes Piece geschlagen
            self.punkteDiff -= piece.points     #Schwarze bekommt punkte dazu (-)
            
    def punkteBerechnungUmwand(self, piece):
        if self.umwandlung:
            color = piece.pieceColor
            if color == 'B': #Wenn schwarzes Piece umgewandelt
                self.punkteDiff -= piece.points     #Schwarz bekommt punkte dazu (+)
            else:                       #Wenn weißes Piece umgewandelt
                self.punkteDiff += piece.points     #Weiß bekommt punkte dazu (-)
            
            
                
    def FENinterpreter(self, FENstring):    #übersetzt FEN Notation
        self.boardDict = {}
        rows = FENstring.split('/')
        isInt = False
        for i in range(1,9):
            count = 1
            for j in rows[i-1]:
                try:
                    for num in range(int(j)):
                        self.boardDict.update({(count,i): None})
                        count += 1
                    isInt = True
                except ValueError:
                    isInt = False
                
                if not isInt:
                    if j == 'r':
                        self.boardDict.update({(count,i): pieces1.Rock('Rock', 'B')})
                    if j == 'R':
                        self.boardDict.update({(count,i): pieces1.Rock('Rock', 'W')})
                    if j == 'n':
                        self.boardDict.update({(count,i): pieces1.Knight('Knight', 'B')})
                    if j == 'N':
                        self.boardDict.update({(count,i): pieces1.Knight('Knight', 'W')})
                    if j == 'b':
                        self.boardDict.update({(count,i): pieces1.Bishop('Bishop', 'B')})
                    if j == 'B':
                        self.boardDict.update({(count,i): pieces1.Bishop('Bishop', 'W')})
                    if j == 'q':
                        self.boardDict.update({(count,i): pieces1.Queen('Queen', 'B')})
                    if j == 'Q':
                        self.boardDict.update({(count,i): pieces1.Queen('Queen', 'W')})
                    if j == 'k':
                        self.boardDict.update({(count,i): pieces1.King('King', 'B')})
                    if j == 'K':
                        self.boardDict.update({(count,i): pieces1.King('King', 'W')})
                    if j == 'p':
                        self.boardDict.update({(count,i): pieces1.Pawn('Pawn', 'B')})
                    if j == 'P':
                        self.boardDict.update({(count,i): pieces1.Pawn('Pawn', 'W')})
                        
                    count += 1   
        return self.boardDict     
    
    def getFieldfromPosition(self): #übersetzt mouseposition in Feld 
        x,y = pygame.mouse.get_pos()
        x += self.FIELD_SIZE
        y += self.FIELD_SIZE
        return round(x//self.FIELD_SIZE),round(y//self.FIELD_SIZE)
    
    def drawBoard(self): # malt das Brett auf den Screen
        color1 = self.colorB1
        color2 = self.colorB2
        
        for i in range(1,9):
            for j in range(1,9):
                x, y = j, i
                abc = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
                x = (x-1)*self.FIELD_SIZE
                y = (y-1)*self.FIELD_SIZE
                if self.checkColor((j, i)) == 'W':
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
        for field in self.boardDict:
            piece = self.boardDict[field]
            if piece != None:
                clickedHighlightSize = self.piece_Size + 10
                x,y = field
                x = (x-1)*self.FIELD_SIZE
                y = (y-1)*self.FIELD_SIZE
                if  self.currentMove != [] and field == self.currentMove[0]:
                    img = pygame.transform.scale(piece.pieceImg, (clickedHighlightSize, clickedHighlightSize))
                    self.screen.blit(img, (x + self.FIELD_SIZE//2 - clickedHighlightSize//2, y + self.FIELD_SIZE//2 - clickedHighlightSize//2))
                else:
                    img = pygame.transform.scale(piece.pieceImg, (self.piece_Size,self.piece_Size))
                    self.screen.blit(img, (x + self.FIELD_SIZE//2 - self.piece_Size//2, y + self.FIELD_SIZE//2 - self.piece_Size//2))
    
    def draw_move(self):    #visuelle darstellung des Zuges
        if self.legal_moves != []:
            for i in self.legal_moves:
                x,y = i
                x = (x-1)*self.FIELD_SIZE
                y = (y-1)*self.FIELD_SIZE
                pygame.draw.circle(self.screen, pygame.Color('darkgoldenrod2'), [x + self.FIELD_SIZE//2, y + self.FIELD_SIZE//2], self.FIELD_SIZE//6, 0)  
            
    def drawLastMove(self): #visuelle darstellung des letzten Zuges
        if self.lastmove != []:
            for i in range(2):
                x,y = self.lastmove[i][0]
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
    
    def drawPoints(self):
        points = self.punkteDiff
        if points > 0:
            fontImgWhite = self.font.render(str(points), True, pygame.Color('black'))
            fontImgBlack = self.font.render('0', True, pygame.Color('black'))
        else:
            points = -points
            fontImgBlack = self.font.render(str(points), True, pygame.Color('black'))
            fontImgWhite = self.font.render('0', True, pygame.Color('black'))
            
        self.screen.blit(fontImgBlack, (self.FIELD_SIZE*8 + self.FIELD_SIZE//20, 0))
        self.screen.blit(fontImgWhite, (self.FIELD_SIZE*8 + self.FIELD_SIZE//20, self.FIELD_SIZE*8 - fontImgWhite.get_height()))
        
    
    def drawPiecesPos(self):
        if self.amZug == 'W':
            for i in self.whitePositions:
                x = (i[0] - 1)* self.FIELD_SIZE
                y = (i[1] - 1)* self.FIELD_SIZE
                pygame.draw.circle(self.screen, pygame.Color('lightgreen'), [x + self.FIELD_SIZE//2, y + self.FIELD_SIZE//2], self.FIELD_SIZE//3, 0)
        else:
            for i in self.blackPositions:
                x = (i[0] - 1)* self.FIELD_SIZE
                y = (i[1] - 1)* self.FIELD_SIZE
                pygame.draw.circle(self.screen, pygame.Color('darkgreen'), [x + self.FIELD_SIZE//2, y + self.FIELD_SIZE//2], self.FIELD_SIZE//3, 0)
    
    #*################################################# KI
    def get_all_legalMoves(self):
        pass
    
    #*################################################# KI ende
        
    
    def event_loop(self):   #eventloop - reagiert auf keys und mouse
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.done = True
            if event.type == pygame.MOUSEBUTTONDOWN:  
                if not self.umwandlung: 
                    self.moveChoice()
                    self.makeMove(self.currentMove)
                else: 
                    self.umwandlungMeth2()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:     #reset zu folgendem FEN-string
                    self.pieces_on_board = self.FENinterpreter('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR')
                    self.lastmove = []
                    self.punkteDiff = 0
                if event.key == pygame.K_t:     #reset zu folgendem FEN-string
                    self.wechsleTheme()
                if event.key == pygame.K_SPACE:
                    self.undoMove()
                                   
                                              
    def main_loop(self):    #fasst draw methoden zusammen
        while not self.done:
            
            self.clock.tick(self.fps)
            self.screen.fill(self.screen_color)
            self.drawBoard()
            self.drawPoints()
            self.drawLastMove()
            self.drawPiecesPos()
            self.drawPieces()
            self.draw_move()
            if self.umwandlung: self.drawUmwandlung()
            
            
            self.event_loop()

            pygame.display.update() 
            

b = ChessGame()
b.main_loop()
 

#Todo: undoMethode: moved Rechte zurückgeben
#Todo: eigene getlegalmoves methoden für die Figuren
#Todo: getAllLegalMoves - Methoden implementieren

#! Regel: Schach
