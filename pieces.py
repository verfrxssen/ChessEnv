import os
import pygame




class Piece:
    def __init__(self, pieceKind, color, pos): # pieceKind Bsp. Kight  color Bsp. 'W'
        self.pieceKind = pieceKind
        self.pieceColor = color
        self.pos = pos
        self.pieceImg = pygame.image.load(os.path.join('piecesImg',f'{pieceKind}_{color}.png'))
        

    

class Pawn(Piece):  #erbt von Piece
    def __init__(self, pieceKind, color, pos):
        self.moveSet = [(0,1)] if color == 'B' else [(0,-1)]
        super(Pawn, self).__init__(pieceKind, color, pos)
        
    #* rule: wenn W+2./ B+7. reihe dann 2S möglich sonst 1S und schräg wenn gegnerische Figur außer König

class Rock(Piece):
    def __init__(self, pieceKind, color, pos):
        self.moveSet = [] 
        self.prozessmoveSet()
        super(Rock, self).__init__(pieceKind, color, pos)
       
    
    def prozessmoveSet(self):
        for i in range(-8,8):
            self.moveSet.append((i,0))
            self.moveSet.append((0,i))

class Knight(Piece):
    def __init__(self, pieceKind, color, pos):
        self.moveSet = [(1,2), (1,-2), (-1,2), (-1,-2), (2,1), (2,-1),(-2,1), (-2,-1)]
        super(Knight, self).__init__(pieceKind, color, pos)

class Bishop(Piece):
    def __init__(self, pieceKind, color, pos):
        self.moveSet = []
        self.prozessmoveSet()
        super(Bishop, self).__init__(pieceKind, color, pos)
    
    def prozessmoveSet(self):
        for i in range(-8,8):
            self.moveSet.append((i,i))
            self.moveSet.append((-i,i))

class Queen(Piece):
    def __init__(self, pieceKind, color, pos):
        self.moveSet = []
        self.prozessmoveSet()
        super(Queen, self).__init__(pieceKind, color, pos)
    
    def prozessmoveSet(self):
        for i in range(-8,8):
            self.moveSet.append((i,0))
            self.moveSet.append((0,i))
            self.moveSet.append((i,i))
            self.moveSet.append((-i,i))

class King(Piece):
    def __init__(self, pieceKind, color, pos):
        self.moveSet = [(1,1), (1,0), (1,-1), (0,-1), (-1,-1), (-1,0), (-1,1), (0,1)]
        super(King, self).__init__(pieceKind, color, pos)

    

                    


    
    