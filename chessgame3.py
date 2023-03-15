import pygame           
import pieces1       #andere Datei aus gleichem Ordner
import os
import time
import sys
from timer import Timer

pygame.init()



class ChessGame():
    def __init__(self): #soll später in "Einstelungen" veränderbar sein
        self.screen_color = pygame.Color(90, 90, 90)
        self.root = 8   #jedes Schachspiel 8x8 Feld
        self.FIELD_SIZE = 80
        self.piece_Size = self.FIELD_SIZE - self.FIELD_SIZE//8
        self.screen = pygame.display.set_mode((self.FIELD_SIZE*self.root + self.FIELD_SIZE*4, self.FIELD_SIZE*self.root))
        self.screen_rect = self.screen.get_rect()
        self.clock = pygame.time.Clock()
        self.done = False
        self.fps = 60.0
        self.amZug = 'W' #Weiß am Zug
        self.amZugStart = self.amZug
        self.imageFolder = 'piecesImg'
        self.lastmove = []
        
        
        #themes
        self.themeCount = 0
        self.themeList = [[pygame.Color(229, 228, 197), pygame.Color(49, 96, 138), pygame.font.SysFont('monospace', self.piece_Size//3, bold=True)],
                          [pygame.Color(234, 235, 196), pygame.Color(109, 155, 79), pygame.font.SysFont('monospace', self.piece_Size//3, bold=True)],
                          [pygame.Color(240, 208, 160), pygame.Color(174, 114, 73), pygame.font.SysFont('monospace', self.piece_Size//3, bold=True)],
                          [pygame.Color(120, 119, 118), pygame.Color(86, 85, 84), pygame.font.SysFont('monospace', self.piece_Size//3, bold=True)],
                          [pygame.Color(193, 170, 190), pygame.Color(120, 60, 120), pygame.font.SysFont('monospace', self.piece_Size//3, bold=True)]]
        self.colorB1 = pygame.Color(229, 228, 197)
        self.colorB2 = pygame.Color(49, 96, 138)
        self.font = pygame.font.SysFont('monospace', self.piece_Size//3, bold=True)
        self.lastmoveCol = [pygame.Color(255, 219, 77), pygame.Color(162, 42, 42)]
        #self.button1 = Button((self.FIELD_SIZE*8, self.FIELD_SIZE*6, 40, 40), pygame.Color("green"), self.switchAmZug())
        self.buttonColor1 = pygame.Color(49, 96, 138)
        self.buttonColor2 = pygame.Color(109, 155, 79)
        self.buttonColor3 = pygame.Color(174, 114, 73)
        self.buttonColor4 = pygame.Color(86, 85, 84)
        self.buttonColor5 = pygame.Color(120, 60, 120)
        self.buttonColor = self.buttonColor1

        self.buttonColorActive1 = pygame.Color(109, 156, 218)
        self.buttonColorActive2 = pygame.Color(189, 235, 159)
        self.buttonColorActive3 = pygame.Color(254, 194, 153)
        self.buttonColorActive4 = pygame.Color(166, 165, 164)
        self.buttonColorActive5 = pygame.Color(200, 140, 200)
        self.buttonColorActive = pygame.Color(109, 156, 218)
        
        
        self.winCrown = pygame.image.load(os.path.join('settingsImg',f'winCrown.png'))
        self.winCrown = pygame.transform.scale(self.winCrown, (self.piece_Size//1.25, self.piece_Size//1.25))
        self.staleMateIMG = pygame.image.load(os.path.join('settingsImg',f'staleMateIMG.png'))
        self.staleMateIMG = pygame.transform.scale(self.staleMateIMG, (self.piece_Size, self.piece_Size))
        
        #settings color themes
        self.settings_image = pygame.image.load(os.path.join('settingsImg',f'Settings-PNG-File-Download-Free.png'))
        self.image_size = self.settings_image.get_rect()

        self.img = pygame.transform.scale(self.settings_image, (self.FIELD_SIZE//1.5, self.FIELD_SIZE//1.5))
        self.settings_image1 = pygame.image.load(os.path.join('settingsImg',f'back-arrow.webp'))
        self.image_size1 = self.settings_image1.get_rect()
        self.img1 = pygame.transform.scale(self.settings_image1, (self.FIELD_SIZE//2.86, self.FIELD_SIZE//2.86))
        self.pos = pygame.mouse.get_pos()
        self.go2 = False

        #timer
        self.timer = Timer(self.FIELD_SIZE*8 + self.FIELD_SIZE//2, self.FIELD_SIZE*4 - (self.FIELD_SIZE*3)//2, self.FIELD_SIZE*3, 10*60, pygame.Color('grey'), pygame.Color('lightgrey'))
        
        #für die Züge
        self.legal_moves = []  
        self.currentMove = []
        
        #umwandlung
        self.umwandlung = False
        self.umwandlungRectsImg = []
        self.umwandlungsPos = None
        
        #punkte berechnung
        self.punkteDiff = 0 
        self.punkteDiffCopy = self.punkteDiff

        #die Figuren auf dem Brett 
        self.boardDict = self.FENinterpreter('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR')#rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR    - start FEN
        self.boardCopy = self.boardDict.copy()
        
        #undo Logik
        self.revokedList = []
        self.lastEnpassantRevoked = False
        
        #ausgang spiel
        self.gameResult = None
        
            
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
    
    def checkMove(self, field, color):     # vereint die isOnboard und checkFree 
        if self.isOnBoard(field):                       # wernn feld auf dem brett soll es erbnis von checkFree zurück geben möglich: Tru/False/'otherCol'
            return self.checkFree(field, color)
        else: 
            return False
    
    def get_pseudolegal_moves(self, field):  # fasst in liste(legal_moves) die züge aus moveSet der Pieces zusammen wenn diese checkmove Test standhalten
        posMoves = []
        piece = self.boardDict[field]
        if piece and piece.pieceColor == self.amZug:
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
                        posMoves.append(move)
                    elif resCheck == 'otherCol':        #falls figur anderer Farbe auf Feld
                        posMoves.append(move)       #soll das feld noch hinzufügen und dann abbrechen
                        break
                    else:                   #abbrechen wenn nicht feld nicht auf dem Brett o. Figur eigener Farbe auf Feld
                        break
        return posMoves
                        
    
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
        #Rochad
        
        self.switchAmZug()
        alltarMoves = self.collect_all_tarmovesRoch()
        self.switchAmZug()
        
        if king.moved == False: 
            if king.pieceColor == 'W':
                if not self.checkKing():
                    if (self.checkFree((6,8), 'W') and self.checkFree((7,8), 'W')) and (((6,8) not in alltarMoves) and ((7,8) not in alltarMoves)):
                        #kleine Rochade für weiß
                        rockRoch = self.boardDict[(8,8)]
                        if rockRoch != None and rockRoch.pieceKind == 'Rock' and rockRoch.moved == False :
                            checking_list_moves.append([(2,0)])
                            
                    if self.checkFree((2,8), 'W') and self.checkFree((3,8), 'W') and self.checkFree((4,8), 'W') and (((2,8) not in alltarMoves) and ((3,8) not in alltarMoves)  and ((4,8) not in alltarMoves)):
                        #große Rochade für weiß
                        rockRoch = self.boardDict[((1,8))]
                        if rockRoch != None and rockRoch.pieceKind == 'Rock' and rockRoch.moved == False:  
                            checking_list_moves.append([(-2,0)])
                    
            else:
                if not self.checkKing():
                    if (self.checkFree((6,1), 'B') and self.checkFree((7,1), 'B')) and (((6,1) not in alltarMoves) and ((7,1) not in alltarMoves)):
                        #kleine Rochade für schwart       
                        rockRoch = self.boardDict[(8,1)]
                        if rockRoch != None and rockRoch.pieceKind == 'Rock' and rockRoch.moved == False:
                            checking_list_moves.append([(2,0)])
                            
                    if self.checkFree((2,1), 'B') and self.checkFree((3,1), 'B') and self.checkFree((4,1), 'B') and (((2,1) not in alltarMoves) and ((3,1) not in alltarMoves)  and ((4,1) not in alltarMoves)):
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
                self.legal_moves = self.get_realLegal_moves(clickedField)
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
                    self.boardCopy = self.boardDict.copy()  
                    self.punkteDiffCopy = self.punkteDiff 
                    
                    if clickedPiece.pieceKind == 'Rock':
                        if clickedPiece.moved == False:
                            self.revokedList.append(rootField)
                    if clickedPiece.pieceKind == 'King':
                        if clickedPiece.moved == False:
                            self.revokedList.append(rootField)
                        #Rochade (Turmbewegung)
                        if (rootField[0] - field[0]) == 2:      #große Rochade
                            rockField = 1,rootField[1]
                            rockRoch = self.boardDict[rockField]
                            if rockRoch != None  and rockRoch.pieceKind == 'Rock' and rockRoch.pieceColor == clickedPiece.pieceColor:
                                self.lastmove.append((rockField, rockRoch)) #undo
                                self.lastmove.append(((rockField[0] + 3, rockField[1]), None)) #undo
                                self.boardDict.update({(rockField[0] + 3, rockField[1]): rockRoch})
                                self.boardDict.update({rockField: None})
                                rockRoch.moved = True
                                self.revokedList.append(rockField)
                                
            
                        elif (rootField[0] - field[0]) == -2:     #kleine Rochade
                            rockField = 8,rootField[1]
                            rockRoch = self.boardDict[rockField]
                            if rockRoch != None and rockRoch.pieceKind == 'Rock' and rockRoch.pieceColor == clickedPiece.pieceColor:
                                self.lastmove.append((rockField, rockRoch))  #undo
                                self.lastmove.append(((rockField[0] - 2, rockField[1]), None)) #undo
                                self.boardDict.update({(rockField[0] - 2, rockField[1]): rockRoch})
                                self.boardDict.update({rockField: None})
                                rockRoch.moved = True
                                self.revokedList.append(rockField)
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
                                else:
                                    enPassantSchlag = (field[0], field[1] + 1)
                                    self.lastmove.append((enPassantSchlag, self.boardDict[enPassantSchlag]))
                                    self.boardDict.update({enPassantSchlag : None})
                                    
                        #umwandlung
                        if field[1] == 1 and clickedPiece.pieceColor == 'W':
                            self.umwandlungMeth1(field)
                        elif field[1] == 8 and clickedPiece.pieceColor == 'B':
                            self.umwandlungMeth1(field)
                            
                    ########################################################################     
                    schlagPiece = self.boardDict[posTar]
                    if schlagPiece != None:
                        self.punkteBerechnungSchlag(schlagPiece)
                    
                    
                    self.lastmove.append((rootField, clickedPiece)) #für UndoMove 
                    self.lastmove.append((posTar, schlagPiece)) #für UndoMove 
                    
                    #*eigentlicher Zug
                    self.boardDict.update({posTar : clickedPiece})
                    self.boardDict.update({rootField : None})
                    
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

            self.boardDict = self.boardCopy
            if self.revokedList != []:
                for piecePos in self.revokedList:
                    if self.boardDict[piecePos]: self.boardDict[piecePos].moved = False

            self.punkteDiff = self.punkteDiffCopy
            self.lastEnpassantRevoked = False
            self.lastmove = []
            self.revokedList = []
            self.legal_moves = []
            
    
    #sammeln aller Züge
    def collect_all_tarmoves(self):
        tarMoves = []
        for field in self.boardDict.keys():
            piece = self.boardDict[field]
            if piece and piece.pieceColor == self.amZug:
                for tar in self.get_pseudolegal_moves(field):
                    tarMoves.append(tar)
        return tarMoves
    
    #sammeln aller Züge NUR FÜR ROCHADE nötig
    def collect_all_tarmovesRoch(self):
        tarMoves = []
        for field in self.boardDict.keys():
            piece = self.boardDict[field]
            if piece and piece.pieceColor == self.amZug and not piece.pieceKind == 'King':
                for tar in self.get_pseudolegal_moves(field):
                    tarMoves.append(tar)
        return tarMoves
    
    #semmeln aller züge mit betrachtung von schach
    def collect_all_reallegal_moves(self):         
        checkFreePosition = []
        for field in self.boardDict.keys():
            piece = self.boardDict[field]
            if piece and piece.pieceColor == self.amZug:
                for tar in self.get_pseudolegal_moves(field):
                    if not self.checkCheck((field, tar)):
                        checkFreePosition.append(tar)
        return checkFreePosition
    
    #überprüft ob zug in Schach endet
    def checkCheck(self, move):
        self.legal_moves = self.get_pseudolegal_moves(move[0])  #!! sehr langsam self.legalmoves sollte nicht mehr vorkommen
        self.makeMove(move)
        tarList = self.collect_all_tarmoves()
        for i in tarList:
            if self.boardDict[i] and self.boardDict[i].pieceKind == 'King':
                self.undoMove()
                return True
        self.undoMove()
        return False
    

    #collect die möglichen züge die auch kein Schach als Folge haben
    def get_realLegal_moves(self, field):
        tarPositions = []
        for i in self.get_pseudolegal_moves(field):
            move = (field, i)
            if not self.checkCheck(move):
                tarPositions.append(i)
        return tarPositions
    
    #überprüft, ob der könig im schach steht
    def checkKing(self):
        self.switchAmZug()  #Da nach dem Schachsetzten der andere Spieler dran wäre, muss, um die Targetpositions des Schachsetztenden Spieler zu erhalten, wieder der Schachsetztende am Zug sein
        tarList = self.collect_all_tarmovesRoch()
        for i in tarList:
            if self.boardDict[i] and self.boardDict[i].pieceKind == 'King':
                x,y = i #Schach sichtbar machen
                x = (x-1)*self.FIELD_SIZE
                y = (y-1)*self.FIELD_SIZE
                self.screen.fill(pygame.Color(162, 42, 42), pygame.Rect(x, y, self.FIELD_SIZE, self.FIELD_SIZE))
                self.switchAmZug()
                return True
        self.switchAmZug()  #Damit die Mehtode an sich nichts an der Reihenfolge der Spieler ändert, muss diese hier wieder umgekehrt werden
        return False
        
    
    #überprüft, wann schachmatt und wann patt ist
    def get_game_result(self):
        legalmovesCopy = self.legal_moves.copy()    #Da beim überprüfen auf Schach die Listen resetten werden durch dem simuleirten Zug, wird hier die ausgangsstellung gepseichert
        currentMoveCopy = self.currentMove.copy()
        if self.collect_all_reallegal_moves() == [] and self.checkKing() == True:    #Wenn der Gegner sich nicht bewegen kann, ohne dass dadurch kein schach entsteht und er IM schach steht -> schachmatt
            return 'checkMate'
        elif self.collect_all_reallegal_moves() == [] and self.checkKing() == False: #Wenn der Gegner sich nicht bewegen kann, ohne dass dadurch kein schach entsteht und er NICHT schach steht -> patt
            return 'staleMate'
        self.legal_moves = legalmovesCopy   #laden der ausgangsstellung vor dem checken
        self.currentMove = currentMoveCopy
        
    
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
    
    
    
    def resetBoard(self):
        self.lastmove = []
        self.legal_moves = []
        self.currentMove = []
        self.gameResult = None
        self.punkteDiff = 0
        self.amZug = self.amZugStart
        self.boardDict = self.FENinterpreter('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR') #start
    
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
                pygame.draw.circle(self.screen, pygame.Color(170, 170, 170), [x + self.FIELD_SIZE//2, y + self.FIELD_SIZE//2], self.FIELD_SIZE//6, 0)  
            
    def drawLastMove(self): #visuelle darstellung des letzten Zuges
        if self.currentMove != []:
            for i in range(len(self.currentMove)):
                x,y = self.currentMove[i]
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

   
    def drawbutton(self, bx, by, length, height, color_normal, color_active, pos):   #malt einen button auf den frame
        self.bx = bx
        self.by = by
        self.length = length
        self.height = height
        self.color_normal = color_normal
        self.color_active = color_active
        if pos[0] > self.bx and pos[0] < self.bx+self.length and pos[1] > self.by and pos[1] < self.by+self.height:
            pygame.draw.rect(self.screen, self.color_active, (self.bx, self.by, self.length, self.height))
        else:
            pygame.draw.rect(self.screen, self.color_normal, (self.bx, self.by, self.length, self.height))

    
    def drawPoints(self):   #malt die Punktedifferenz aufs Feld
        points = self.punkteDiff
        if points > 0:
            fontImgWhite = self.font.render("Points:" + str(points), True, pygame.Color('black'))
            fontImgBlack = self.font.render('Points: 0', True, pygame.Color('black'))
        else:
            points = -points
            fontImgBlack = self.font.render("Points:" + str(points), True, pygame.Color('black'))
            fontImgWhite = self.font.render('Points: 0', True, pygame.Color('black'))
            
        self.screen.blit(fontImgBlack, (self.FIELD_SIZE*8 + self.FIELD_SIZE//5, 0))
        self.screen.blit(fontImgWhite, (self.FIELD_SIZE*8 + self.FIELD_SIZE//5, self.FIELD_SIZE*8 - fontImgWhite.get_height()))

    def drawResult(self):
        if self.gameResult != None:
            if self.gameResult == 'checkMate':
                for i in self.boardDict.keys():
                    if self.boardDict[i] and self.boardDict[i].pieceKind == 'King' and self.boardDict[i].pieceColor != self.amZug:
                        x,y = i #Win sichtbar machen
                        x = (x-1)*self.FIELD_SIZE + self.FIELD_SIZE//2 - self.winCrown.get_width()//2
                        y = (y-1)*self.FIELD_SIZE - self.FIELD_SIZE//3
                        self.screen.blit(self.winCrown, (x, y))
            elif self.gameResult == 'staleMate':
                for i in self.boardDict.keys():
                    if self.boardDict[i] and self.boardDict[i].pieceKind == 'King' and self.boardDict[i].pieceColor == self.amZug:
                        x,y = i #Win sichtbar machen
                        x = (x-1)*self.FIELD_SIZE + self.FIELD_SIZE//2 - self.staleMateIMG.get_width()//2
                        y = (y-1)*self.FIELD_SIZE
                        self.screen.blit(self.staleMateIMG, (x, y))
    
    
    
    def drawSetup (self):   #baut das Feld auf
        self.clock.tick(self.fps)
        self.screen.fill(self.screen_color)
        self.drawBoard()
        self.drawPoints()
        self.drawLastMove()
        self.checkKing() #!!!!!!!!!!!!!!
        self.drawPieces()
        self.drawResult()
        self.draw_move()
        self.timer.draw(self.screen)
        self.screen.blit(self.img, (self.FIELD_SIZE//0.089, self.FIELD_SIZE//10))
        self.screen.fill(pygame.Color('black'), pygame.rect.Rect(self.FIELD_SIZE*8, self.FIELD_SIZE//9999, self.FIELD_SIZE//10, self.FIELD_SIZE*15))
        
        self.drawbutton((self.FIELD_SIZE*8.33), (self.FIELD_SIZE*7), (self.FIELD_SIZE//1), (self.FIELD_SIZE//2.5), (self.buttonColor), (self.buttonColorActive), pygame.mouse.get_pos())
        Surrender = pygame.font.SysFont('monospace', self.FIELD_SIZE//4)
        text_surface = Surrender.render('Surr.', True, (0, 0, 0))
        self.screen.blit(text_surface, (self.FIELD_SIZE*8.33 + self.FIELD_SIZE//8, self.FIELD_SIZE*7 + self.FIELD_SIZE//12))

        self.drawbutton((self.FIELD_SIZE*8.33 + self.FIELD_SIZE//1 + self.FIELD_SIZE*0.2), (self.FIELD_SIZE*7), (self.FIELD_SIZE//1), (self.FIELD_SIZE//2.5), (self.buttonColor), (self.buttonColorActive), pygame.mouse.get_pos())
        Remis = pygame.font.SysFont('monospace', self.FIELD_SIZE//4)
        text_surface = Remis.render('Remis', True, (0, 0, 0))
        self.screen.blit(text_surface, (self.FIELD_SIZE*8.33 + self.FIELD_SIZE//1 + self.FIELD_SIZE*0.2 + self.FIELD_SIZE//8, self.FIELD_SIZE*7 + self.FIELD_SIZE//12))
        
        self.drawbutton((self.FIELD_SIZE*8.33 + 2*self.FIELD_SIZE//1 + 2*self.FIELD_SIZE*0.2), (self.FIELD_SIZE*7), (self.FIELD_SIZE//1), (self.FIELD_SIZE//2.5), (self.buttonColor), (self.buttonColorActive), pygame.mouse.get_pos())
        reset = pygame.font.SysFont('monospace', self.FIELD_SIZE//4)
        text_surface = reset.render('Reset', True, (0, 0, 0))
        self.screen.blit(text_surface, (self.FIELD_SIZE*8.33 + 2*self.FIELD_SIZE//1 + 2*self.FIELD_SIZE*0.2 + self.FIELD_SIZE//8, self.FIELD_SIZE*7 + self.FIELD_SIZE//12))

    def event_loop(self):   #eventloop - reagiert auf keys und mouse
        for event in pygame.event.get():
            self.pos = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                self.done = True
            if event.type == pygame.MOUSEBUTTONDOWN:  
                if not self.umwandlung: 
                    self.moveChoice()
                    self.makeMove(self.currentMove)
                    self.gameResult = self.get_game_result()     
                else: 
                    self.umwandlungMeth2()
                self.timer.clicked()
                
                
                '''#reset
                if (self.pos[0] >= (self.FIELD_SIZE*8.33) and self.pos[0] <= (self.FIELD_SIZE*8.33 + 2*self.FIELD_SIZE//1 + 2*self.FIELD_SIZE*0.2 + self.FIELD_SIZE//1)) and (self.pos[1] >= (self.FIELD_SIZE*7) and self.pos[1] <= (self.FIELD_SIZE*7 + self.FIELD_SIZE//2.5)):
                    self.resetBoard()'''

                #remis
                if (self.pos[0] >= (self.FIELD_SIZE*8.33 + self.FIELD_SIZE//1 + 2*self.FIELD_SIZE*0.2) and self.pos[0] <= (self.FIELD_SIZE*8.33 + 2*self.FIELD_SIZE//1 + 2*self.FIELD_SIZE*0.2 + self.FIELD_SIZE//1)) and (self.pos[1] >= (self.FIELD_SIZE*7) and self.pos[1] <= (self.FIELD_SIZE*7 + self.FIELD_SIZE//2.5)):
                    self.gameResult = 'staleMate'
                    
                '''
                #surrender
                if (self.pos[0] >= (self.FIELD_SIZE*8.33) and self.pos[0] <= (self.FIELD_SIZE*8.33 + 2*self.FIELD_SIZE//1 + 2*self.FIELD_SIZE*0.2 + self.FIELD_SIZE//1)) and (self.pos[1] >= (self.FIELD_SIZE*7) and self.pos[1] <= (self.FIELD_SIZE*7 + self.FIELD_SIZE//2.5)):
                    self.gameResult = 'checkMate'''


                if (self.pos[0] >= (self.FIELD_SIZE//0.089) and self.pos[0] <= (self.FIELD_SIZE//0.034)) and (self.pos[1] >= (self.FIELD_SIZE//10) and self.pos[1] <= (self.FIELD_SIZE//2)):
                    self.go2 = True
                    self.screen.fill((255, 255, 255))
                    settingsLight_image = pygame.image.load(os.path.join('settingsImg',f'SettingsLight.png'))
                    self.image_size2 = settingsLight_image.get_rect()
                    self.img2 = pygame.transform.scale(settingsLight_image, (self.FIELD_SIZE*8, self.FIELD_SIZE*8))
                    self.screen.blit(self.img2, (self.FIELD_SIZE*4, self.FIELD_SIZE//3.5))
                    pygame.display.flip()
                    while self.go2:
                        self.pos = pygame.mouse.get_pos()
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT: 
                                sys.exit() 

                        #farb buttons drawn, die Positionen sind abhängig von der field_size, damit diese auch bei verkleinerung des chessgames zu sehen sind
                        self.drawbutton((self.FIELD_SIZE//5), (self.FIELD_SIZE//1.667), (self.FIELD_SIZE//2.5), (self.FIELD_SIZE//2.5), (49, 96, 138), (109, 156, 218), pygame.mouse.get_pos())
                        self.drawbutton((self.FIELD_SIZE), (self.FIELD_SIZE//1.667), (self.FIELD_SIZE//2.5), (self.FIELD_SIZE//2.5), (109, 155, 79), (189, 235, 159), pygame.mouse.get_pos())
                        self.drawbutton((self.FIELD_SIZE//0.556), (self.FIELD_SIZE//1.667), (self.FIELD_SIZE//2.5), (self.FIELD_SIZE//2.5), (174, 114, 73), (254, 194, 153), pygame.mouse.get_pos())
                        self.drawbutton((self.FIELD_SIZE//0.385), (self.FIELD_SIZE//1.667), (self.FIELD_SIZE//2.5), (self.FIELD_SIZE//2.5), (86, 85, 84), (166, 165, 164), pygame.mouse.get_pos())
                        self.drawbutton((self.FIELD_SIZE//0.294), (self.FIELD_SIZE//1.667), (self.FIELD_SIZE//2.5), (self.FIELD_SIZE//2.5), (120, 60, 120), (200, 140, 200), pygame.mouse.get_pos())

                        #schrfit drawn
                        pygame.font.init()
                        text = pygame.font.SysFont('monospace', (self.FIELD_SIZE//4))
                        text_surface = text.render('Select Color Theme:', False, (0, 0, 0))
                        self.screen.blit(text_surface, ((self.FIELD_SIZE//5), (self.FIELD_SIZE//10)))
                        self.screen.blit(self.img1, ((self.FIELD_SIZE//4.445), (self.FIELD_SIZE//0.816)))
                        pygame.display.flip()       
                        
                        if event.type == pygame.MOUSEBUTTONDOWN and (self.pos[0] >= (self.FIELD_SIZE//5) and self.pos[0] <= (self.FIELD_SIZE//1.667)) and (self.pos[1] >= (self.FIELD_SIZE//1.667) and self.pos[1] <= (self.FIELD_SIZE//1)):   #blue button, schaut ob ein mausklick im bereich des buttons geschehen ist, bereich abhängig von fieldgröße, damit beim verkleinern an selber stelle
                            self.colorB1 = pygame.Color(229, 228, 197)  #Hauptfarbe
                            self.colorB2 = pygame.Color(49, 96, 138)    #Nebenfarbe
                            self.drawSetup()                            #Board zu Ursprung zurücksetzten
                            self.buttonColor = self.buttonColor1
                            self.buttonColorActive = self.buttonColorActive1
                            pygame.display.flip()   
                            self.done = False   
                            self.go2 = False  
                            pygame.display.flip()    
                        elif event.type == pygame.MOUSEBUTTONDOWN and (self.pos[0] >= (self.FIELD_SIZE//1) and self.pos[0] <= (self.FIELD_SIZE//0.714)) and (self.pos[1] >= (self.FIELD_SIZE//1.667) and self.pos[1] <= (self.FIELD_SIZE//1)): #green button, schaut ob ein mausklick im bereich des buttons geschehen ist, bereich abhängig von fieldgröße, damit beim verkleinern an selber stelle
                            self.colorB1 = pygame.Color(234, 235, 196)  #Hauptfarbe
                            self.colorB2 = pygame.Color(109, 155, 79)   #Nebenfarbe
                            self.drawSetup()
                            self.buttonColor = self.buttonColor2   
                            self.buttonColorActive = self.buttonColorActive2                        #Board zu Ursprung zurücksetzten
                            pygame.display.flip()   
                            self.done = False   
                            self.go2 = False  
                            pygame.display.flip()  
                        elif event.type == pygame.MOUSEBUTTONDOWN and (self.pos[0] >= (self.FIELD_SIZE//0.556) and self.pos[0] <= (self.FIELD_SIZE//0.4546)) and (self.pos[1] >= (self.FIELD_SIZE//1.667) and self.pos[1] <= (self.FIELD_SIZE//1)): #brown button, schaut ob ein mausklick im bereich des buttons geschehen ist, bereich abhängig von fieldgröße, damit beim verkleinern an selber stelle
                            self.colorB1 = pygame.Color(240, 208, 160)  #Hauptfarbe
                            self.colorB2 = pygame.Color(174, 114, 73)   #Nebenfarbe
                            self.drawSetup()                            #Board zu Ursprung zurücksetzten
                            self.buttonColor = self.buttonColor3
                            self.buttonColorActive = self.buttonColorActive3
                            pygame.display.flip()   
                            self.done = False   
                            self.go2 = False  
                            pygame.display.flip()  
                        elif event.type == pygame.MOUSEBUTTONDOWN and (self.pos[0] >= (self.FIELD_SIZE//0.385) and self.pos[0] <= (self.FIELD_SIZE//0.334)) and (self.pos[1] >= (self.FIELD_SIZE//1.667) and self.pos[1] <= (self.FIELD_SIZE//1)): #grey button, schaut ob ein mausklick im bereich des buttons geschehen ist, bereich abhängig von fieldgröße, damit beim verkleinern an selber stelle
                            self.colorB1 = pygame.Color(120, 119, 118)  #Hauptfarbe
                            self.colorB2 = pygame.Color(86, 85, 84)     #Nebenfarbe
                            self.drawSetup()                            #Board zu Ursprung zurücksetzten
                            self.buttonColor = self.buttonColor4
                            self.buttonColorActive = self.buttonColorActive4
                            pygame.display.flip()   
                            self.done = False   
                            self.go2 = False  
                            pygame.display.flip()  
                        elif event.type == pygame.MOUSEBUTTONDOWN and (self.pos[0] >= (self.FIELD_SIZE//0.294) and self.pos[0] <= (self.FIELD_SIZE//0.263)) and (self.pos[1] >= (self.FIELD_SIZE//1.667) and self.pos[1] <= (self.FIELD_SIZE//1)): #purple button, schaut ob ein mausklick im bereich des buttons geschehen ist, bereich abhängig von fieldgröße, damit beim verkleinern an selber stelle
                            self.colorB1 = pygame.Color(193, 170, 190)  #Hauptfarbe
                            self.colorB2 = pygame.Color(120, 60, 120)   #Nebenfarbe
                            self.drawSetup()                            #Board zu Ursprung zurücksetzten
                            self.buttonColor = self.buttonColor5
                            self.buttonColorActive = self.buttonColorActive5
                            pygame.display.flip()   
                            self.done = False   
                            self.go2 = False  
                            pygame.display.flip() 
                        elif event.type == pygame.MOUSEBUTTONDOWN and (self.pos[0] >= (self.FIELD_SIZE//5) and self.pos[0] <= (self.FIELD_SIZE//1.667)) and (self.pos[1] >= (self.FIELD_SIZE//0.8334) and self.pos[1] <= (self.FIELD_SIZE//0.625)): #back button, schaut ob ein mausklick im bereich des buttons geschehen ist, bereich abhängig von fieldgröße, damit beim verkleinern an selber stelle
                            self.drawSetup()                            #Board zu Ursprung zurücksetzten
                            pygame.display.flip()       
                            self.done = False   
                            self.go2 = False  
                            pygame.display.flip()      
                
                             
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:     #reset zu folgendem FEN-string
                    self.resetBoard()
                if event.key == pygame.K_t:     #reset zu folgendem FEN-string
                    self.wechsleTheme()
                if event.key == pygame.K_SPACE:
                    print(self.get_game_result())
                    pass
                if event.key == pygame.K_1:
                    pass
                    
                                
                                            
                                              
    def main_loop(self):    #fasst draw methoden zusammen 
        while not self.done:
            
            self.drawSetup() 
            if self.umwandlung: self.drawUmwandlung()
            
            self.event_loop()

            pygame.display.update() 

            
b = ChessGame()
b.main_loop()
 

#Todo: undoMethode: moved Rechte zurückgeben
#Todo: eigene getlegalmoves methoden für die Figuren
#Todo: getAllLegalMoves - Methoden implementieren

#! Regel: Schach
