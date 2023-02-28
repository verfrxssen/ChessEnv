import os
import pygame




class Piece:
    def __init__(self, pieceKind, color): # pieceKind Bsp. Kight  color Bsp. 'W'
        self.pieceKind = pieceKind
        self.pieceColor = color
        self.pieceImg = pygame.image.load(os.path.join('piecesImg',f'{pieceKind}_{color}.png'))
        
    def update_moveSet(self, piecesOnBoard):
        pass
    

class Pawn(Piece):  #erbt von Piece
    def __init__(self, pieceKind, color):
        self.points = 1
        self.moveSet = [[(0,1)]] if color == 'B' else [[(0,-1)]]
        self.enPassant = None
        super(Pawn, self).__init__(pieceKind, color,  )
    
    def reset_moveSet(self):
        self.moveSet = [[(0,1)]] if self.pieceColor == 'B' else [[(0,-1)]]
        
    def update_moveSet(self, piecesOnBoard):
        self.reset_moveSet()
        
   

class Rock(Piece):
    def __init__(self, pieceKind, color):
        self.points = 5
        self.moveSet = [[], [], [], []] 
        self.prozessmoveSet()
        self.moved = False
        super(Rock, self).__init__(pieceKind, color)
        
    def reset_moveSet(self):
        pass

    def prozessmoveSet(self):
        for i in range(1,8):
            self.moveSet[0].append((i,0))
            self.moveSet[1].append((0,i))
        
        for i in range(-1,-8,-1):
            self.moveSet[2].append((i,0))
            self.moveSet[3].append((0,i))

class Knight(Piece):
    def __init__(self, pieceKind, color):
        self.points = 3
        self.moveSet = [[(1,2)], [(1,-2)], [(-1,2)], [(-1,-2)], [(2,1)], [(2,-1)],[(-2,1)], [(-2,-1)]]
        super(Knight, self).__init__(pieceKind, color)

    def reset_moveSet(self):
        pass
        
class Bishop(Piece):
    def __init__(self, pieceKind, color):
        self.points = 3
        self.moveSet = [[], [], [], []]
        self.prozessmoveSet()
        super(Bishop, self).__init__(pieceKind, color)
    
    def prozessmoveSet(self):
        for i in range(1,8):
            self.moveSet[0].append((i,i))
            self.moveSet[1].append((-i,i))
        
        for i in range(-1,-8,-1):
            self.moveSet[2].append((i,i))
            self.moveSet[3].append((-i,i))

    def reset_moveSet(self):
        pass
    
class Queen(Piece):
    def __init__(self, pieceKind, color):
        self.points = 9
        self.moveSet = [[], [], [], [], [], [], [], []]
        self.prozessmoveSet()
        super(Queen, self).__init__(pieceKind, color)
    
    def reset_moveSet(self):
        pass
    
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
    def __init__(self, pieceKind, color):
        self.points = 1000
        self.moveSet = [[(1,1)], [(1,0)], [(1,-1)], [(0,-1)], [(-1,-1)], [(-1,0)], [(-1,1)], [(0,1)]]
        self.moved = False
        super(King, self).__init__(pieceKind, color)

    def reset_moveSet(self):
        self.moveSet = [[(1,1)], [(1,0)], [(1,-1)], [(0,-1)], [(-1,-1)], [(-1,0)], [(-1,1)], [(0,1)]]

   
                    


    
    