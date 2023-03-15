import pygame, sys
import time
import os

pygame.init()
class Timer:
    
    def __init__(self, xPos, yPos, size, startTime, standardCol, highlightedCol):
        self.xPos = xPos
        self.yPos = yPos
        self.size = size
        self.time1 = startTime
        self.time2 = startTime
        self.amZug = 1
        self.lastTime = time
        self.counting = False
        self.standardCol = standardCol
        self.highlightedCol = highlightedCol
        #pygame.font.Font(os.path.join('fonts',f"DS-DIGI.TTF"))
        self.font =  pygame.font.Font("fonts/font.TTF", self.size//5)
        self.gameOverCol = pygame.Color('firebrick2')
        self.color1 = self.standardCol
        self.color2 = self.standardCol
    
    def gameOver(self):
        if self.time1 <= 0:
            self.color1 = self.gameOverCol
            self.counting = False
        elif self.time2 <= 0:  
            self.color2 = self.gameOverCol
            self.counting = False
    

    def update(self):
        if self.counting:
            if self.amZug == 1:
                self.color1 = self.highlightedCol
                self.color2 = self.standardCol
                self.time1 -= (time.time() - self.lastTime)
                self.lastTime = time.time()
            if self.amZug == 2:
                self.color2 = self.highlightedCol
                self.color1 = self.standardCol
                self.time2 -= (time.time() - self.lastTime)
                self.lastTime = time.time()
            self.gameOver()

    def draw(self, screen):
        
        self.update()
        
        screen.fill(pygame.Color('black'), pygame.rect.Rect(self.xPos, self.yPos, self.size, self.size))
        screen.fill(pygame.Color(self.color1), pygame.rect.Rect(self.xPos+self.size//15, self.yPos+self.size//15, self.size-(self.size//15)*2, self.size//2-(self.size//15)*2))
        screen.fill(pygame.Color(self.color2), pygame.rect.Rect(self.xPos+self.size//15, self.yPos+self.size//15+self.size//2, self.size-(self.size//15)*2, self.size//2-(self.size//15)*2))
        minutes1 = self.time1 // 60
        seconds1 = self.time1 % 60
        text1 = f"{str(int(round(minutes1)))}:{str(int(round(seconds1)))}"
        minutes2 = self.time2 // 60
        seconds2 = self.time2 % 60
        text2 = f"{str(int(round(minutes2)))}:{str(int(round(seconds2)))}"
        fontImg1 = self.font.render(text1, True, pygame.Color('black'))
        fontImg2 = self.font.render(text2, True, pygame.Color('black'))
        screen.blit(fontImg1, (self.xPos + self.size//2 - fontImg1.get_width()//2, self.yPos + self.size//3.5 - fontImg1.get_height()//2))
        screen.blit(fontImg2, (self.xPos + self.size//2 - fontImg2.get_width()//2, self.yPos + self.size//1.35 - fontImg1.get_height()//2))
        
        
    def clicked(self):
        x, y = pygame.mouse.get_pos()
        if (x > self.xPos and (x < self.xPos + self.size)) and (y > self.yPos and y < (self.yPos + self.size)):
            if (x > self.xPos and (x < self.xPos + self.size)) and (y > self.yPos and y < (self.yPos + self.size//2)):
                self.amZug = 1
                self.lastTime = time.time()
                self.counting = True
            else:
                self.amZug = 2
                self.lastTime = time.time()
                self.counting = True

        
'''                
class Test:
    
    def __init__(self):
        self.screen_color = pygame.Color('white')
        self.FIELD_SIZE = 100
        self.screen = pygame.display.set_mode((self.FIELD_SIZE*8 + self.FIELD_SIZE, self.FIELD_SIZE*8))
        self.screen_rect = self.screen.get_rect()
        self.clock = pygame.time.Clock()
        self.done = False
        self.fps = 60.0
        self.timer1 = Timer(50, 50, 500, 10)
    
    def event_loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.done = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.timer1.clicked()
                
        
    
    def mainloop(self):
        while not self.done:
            self.clock.tick(self.fps)
            self.screen.fill(self.screen_color)
            self.timer1.draw(self.screen)
            
            self.event_loop()

            pygame.display.update() 

test = Test()
    
test.mainloop()'''