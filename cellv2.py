import conway
import pygame
import numpy as np

"""
Now using a convolution
"""

class Game:
    def __init__(self, m, n, size):
        self.size = round((1/m) * size)
        self.m = m
        self.n = n
        self.board = np.zeros((self.m, self.n))
        self.screen = pygame.display.set_mode((m*self.size, n*self.size))
        self.clock = pygame.time.Clock()
        self.running = True
        self.pause = True
        self.draw = False
        self.erase = False
        self.background = (25,25,25)
        self.cellColor = (255,255,0)
        self.updateGrid()

    def painter(self):
        if self.draw:
            self.drawing()
        if self.erase:
            self.erasing()

    def drawing(self):
        x, y = pygame.mouse.get_pos()
        self.board[x//self.size][y//self.size] = 1
        self.updateGrid()

    def erasing(self):
        x, y = pygame.mouse.get_pos()
        self.board[x//self.size][y//self.size] = 0
        self.updateGrid()

    def update(self):
        self.painter()
        if not self.pause:
            
            self.progressBoard()
            self.updateGrid()

    def updateGrid(self):
        self.screen.fill(self.background)
        for i in range(self.m):
            for j in range(self.n):
                if self.board[i][j] == 1:
                    pygame.draw.rect(self.screen, self.cellColor, (i*self.size, j*self.size, self.size, self.size))
    def progressBoard(self):
        self.board = conway.conway(self.board)

    def run(self):
        while self.running:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                    if event.key == pygame.K_SPACE:
                        self.pause = not self.pause

                    if event.key == pygame.K_c:
                        self.board = np.zeros((self.m, self.n))
                        self.updateGrid()


                    if event.key == pygame.K_r:
                        self.board = np.random.random(self.m*self.n).reshape((self.m, self.n)).round()
                        self.updateGrid()


                    if event.key == pygame.K_RIGHT and self.pause:
                        self.updateGrid()
                        self.progressBoard()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.draw = True
                    if event.button == 3:
                        self.erase = True
                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        self.draw = False
                    if event.button == 3:
                        self.erase = False
            
            

            self.update()
            #background
            pygame.display.flip()
            self.clock.tick(165)


if __name__ == "__main__":
    game = Game(100, 100, 300)
    game.run()
