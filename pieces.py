import os
import pygame




class Piece:
    def __init__(self, pieceKind, color, pos): # pieceKind Bsp. Kight  color Bsp. 'W'
        self.pieceKind = pieceKind
        self.pieceColor = color
        self.pos = pos
        self.pieceImg = pygame.image.load(os.path.join('piecesImg',f'{pieceKind}_{color}.png'))
        
    def update_moveSet(self, piecesOnBoard):
        pass
    

class Pawn(Piece):  #erbt von Piece
    def __init__(self, pieceKind, color, pos):
        self.moveSet = [[(0,1)]] if color == 'B' else [[(0,-1)]]
        self.enPassant = None
        super(Pawn, self).__init__(pieceKind, color, pos)
    
    def reset_moveSet(self):
        self.moveSet = [[(0,1)]] if self.pieceColor == 'B' else [[(0,-1)]]
        
    def update_moveSet(self, piecesOnBoard):
        self.reset_moveSet()
        
        #Doppelzug
        if self.pos[1] == 2 and self.pieceColor == 'B':
            self.moveSet[0].append((0,2))
        elif self.pos[1] == 7 and self.pieceColor == 'W':
            self.moveSet[0].append((0,-2))
        
        #schräg schlagen
        if self.pieceColor == 'W':
            for i in piecesOnBoard:
                if i.pos == (self.pos[0] - 1, self.pos[1] - 1):
                    self.moveSet.append([(-1,-1)])
                elif i.pos == (self.pos[0] + 1, self.pos[1] - 1):
                    self.moveSet.append([(1,-1)])
        else:
            for i in piecesOnBoard:
                if i.pos == (self.pos[0] - 1, self.pos[1] + 1):
                    self.moveSet.append([(-1,+1)])
                elif i.pos == (self.pos[0] + 1, self.pos[1] + 1):
                    self.moveSet.append([(1,+1)])
        
        #blockiert wenn Figur vor Bauer
        vorwärts = self.moveSet[0][0]
        for i in piecesOnBoard:
            if i.pos == (self.pos[0] + vorwärts[0], self.pos[1] + vorwärts[1]):
                self.moveSet.remove(self.moveSet[0])

        #en passant
        if self.enPassant != None:
            if self.pieceColor == 'W':              #En Passant für Weiß
                if self.enPassant == -1:
                    self.moveSet.append([(1, -1)])  #schlägt schräg nach oben rechts über den schwarzen Bauer
                else:
                    self.moveSet.append([(-1, -1)]) #schlägt schräg nach oben links über den schwarzen Bauer
            else:
                if self.enPassant == -1:            #En Passant für Schwarz
                    self.moveSet.append([(1, 1)])   #schlägt schräg nach unten links unter den weißen Bauer
                else:
                    self.moveSet.append([(-1, 1)])  #schlägt schräg nach unten rechts unter den weißen Bauer
        
        #zieht enPassant Recht zurück 
        if self.pos[1] > 4 and self.pieceColor == 'W':
            self.enPassant = None
        elif self.pos[1] < 5 and self.pieceColor == 'B':
            self.enPassant = None

            

        
    
    #* rule: wenn W+2./ B+7. reihe dann 2S möglich sonst 1S und schräg wenn gegnerische Figur außer König

class Rock(Piece):
    def __init__(self, pieceKind, color, pos):
        self.moveSet = [[], [], [], []] 
        self.prozessmoveSet()
        self.moved = False
        super(Rock, self).__init__(pieceKind, color, pos)
        
    def reset_moveSet(self):
        self.moveSet = [[], [], [], []]
        self.prozessmoveSet()

    def update_moveSet(self, piecesOnBoard):
        self.reset_moveSet()
        if self.pieceColor == 'W' and not (self.pos == (1,8) or self.pos == (8,8)):
            self.moved = True
        elif self.pieceColor == 'B' and not (self.pos == (1,1) or self.pos == (8,1)):
            self.moved = True
    
    def prozessmoveSet(self):
        for i in range(1,8):
            self.moveSet[0].append((i,0))
            self.moveSet[1].append((0,i))
        
        for i in range(-1,-8,-1):
            self.moveSet[2].append((i,0))
            self.moveSet[3].append((0,i))

class Knight(Piece):
    def __init__(self, pieceKind, color, pos):
        self.moveSet = [[(1,2)], [(1,-2)], [(-1,2)], [(-1,-2)], [(2,1)], [(2,-1)],[(-2,1)], [(-2,-1)]]
        super(Knight, self).__init__(pieceKind, color, pos)

class Bishop(Piece):
    def __init__(self, pieceKind, color, pos):
        self.moveSet = [[], [], [], []]
        self.prozessmoveSet()
        super(Bishop, self).__init__(pieceKind, color, pos)
    
    def prozessmoveSet(self):
        for i in range(1,8):
            self.moveSet[0].append((i,i))
            self.moveSet[1].append((-i,i))
        
        for i in range(-1,-8,-1):
            self.moveSet[2].append((i,i))
            self.moveSet[3].append((-i,i))

class Queen(Piece):
    def __init__(self, pieceKind, color, pos):
        self.moveSet = [[], [], [], [], [], [], [], []]
        self.prozessmoveSet()
        super(Queen, self).__init__(pieceKind, color, pos)
    
    def prozessmoveSet(self):
        for i in range(1,8):
            self.moveSet[0].append((i,0))
            self.moveSet[1].append((0,i))
            self.moveSet[2].append((i,i))
            self.moveSet[3].append((-i,i))
        
        for i in range(-1,-8,-1):
            self.moveSet[4].append((i,0))
            self.moveSet[5].append((0,i))
            self.moveSet[6].append((i,i))
            self.moveSet[7].append((-i,i))

class King(Piece):
    def __init__(self, pieceKind, color, pos):
        self.moveSet = [[(1,1)], [(1,0)], [(1,-1)], [(0,-1)], [(-1,-1)], [(-1,0)], [(-1,1)], [(0,1)]]
        self.moved = False
        super(King, self).__init__(pieceKind, color, pos)

    def reset_moveSet(self):
        self.moveSet = [[(1,1)], [(1,0)], [(1,-1)], [(0,-1)], [(-1,-1)], [(-1,0)], [(-1,1)], [(0,1)]]

    def update_moveSet(self, piecesOnBoard):
        self.reset_moveSet()
        if self.pos != (5,8) and self.pieceColor == 'W':
            self.moved = True
        elif self.pos != (5,1) and self.pieceColor == 'B':
            self.moved = True
                    


    
    