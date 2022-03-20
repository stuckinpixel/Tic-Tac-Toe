
import pygame, sys, time, random, json
from pygame.locals import *

pygame.init()
WIDTH, HEIGHT = 1000, 600
surface=pygame.display.set_mode((WIDTH, HEIGHT),0,32)
fps=64
ft=pygame.time.Clock()
pygame.display.set_caption("Tic Tac Toe")

background = pygame.image.load("background.png")
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

font = pygame.font.SysFont("Arial", 13)



class Players:
    def __init__(self):
        self.player1_color = (0, 255, 0)
        self.player2_color = (0, 0, 255)
        self.current = 1
    def change(self):
        if self.current == 1:
            self.current = 2
        else:
            self.current = 1



class Game:
    def __init__(self, surface):
        self.surface = surface
        self.play = True
        self.mouse=pygame.mouse.get_pos()
        self.click=pygame.mouse.get_pressed()
        self.color = {
            "background": (255, 255, 255),
            "alpha": (30, 210, 180)
        }
        self.players = Players()
        self.matrix = []
        self.size = 3
        self.initialize_matrix()
        self.blocks_x = WIDTH*0.2
        self.blocks_y = HEIGHT*0.1
        self.blocks_width = WIDTH*0.7
        self.blocks_height = HEIGHT*0.8
        self.last_time_clicked = time.time()
        self.min_gap_between_clicks = 0.5
        self.unit_width = self.blocks_width/self.size
        self.unit_height = self.blocks_height/self.size
        self.texts = (WIDTH*0.01, HEIGHT*0.2)
        self.winner_label = (WIDTH*0.01, HEIGHT*0.5)
        self.winner = None
        self.waiting = False
    def initialize_matrix(self):
        self.matrix = [ [ 0 for _ in range(self.size) ] for _ in range(self.size) ]
    def render(self):
        for i in range(self.size):
            for j in range(self.size):
                x = self.blocks_x+(i*self.unit_width)
                y = self.blocks_y+(j*self.unit_height)
                if self.matrix[j][i] == 1:
                    pygame.draw.rect(self.surface, self.players.player1_color, (x, y, self.unit_width, self.unit_height))
                elif self.matrix[j][i] == 2:
                    pygame.draw.rect(self.surface, self.players.player2_color, (x, y, self.unit_width, self.unit_height))
                pygame.draw.rect(self.surface, self.color["alpha"], (x, y, self.unit_width, self.unit_height), 1)
        pygame.draw.rect(self.surface, self.color["alpha"], (self.blocks_x, self.blocks_y, self.blocks_width, self.blocks_height), 1)
        # draw texts
        font_surface = font.render("Player 1", True, self.color["alpha"])
        self.surface.blit(font_surface, (10, 100))
        pygame.draw.rect(self.surface, self.players.player1_color, (80, 100, 30, 20))
        font_surface = font.render("Player 2", True, self.color["alpha"])
        self.surface.blit(font_surface, (10, 150))
        pygame.draw.rect(self.surface, self.players.player2_color, (80, 150, 30, 20))
        # print winner
        if self.waiting:
            font_surface = font.render("Winner "+str(self.winner), True, self.color["alpha"])
            self.surface.blit(font_surface, (10, 250))
    def check_clicks(self):
        if self.click[0] == 1:
            if (self.blocks_x)<=self.mouse[0]<=(self.blocks_x+self.blocks_width) and (self.blocks_y)<=self.mouse[1]<=(self.blocks_y+self.blocks_height):
                if (time.time()-self.last_time_clicked) >= self.min_gap_between_clicks:
                    self.last_time_clicked = time.time()
                    x, y = self.mouse
                    i = int((x-self.blocks_x)//self.unit_width)
                    j = int((y-self.blocks_y)//self.unit_height)
                    if self.matrix[j][i] == 0:
                        self.matrix[j][i] = self.players.current
                        self.players.change()
    def check_win(self):
        # check horizontals
        for row in self.matrix:
            if 0 not in row:
                first_value = row[0]
                equals = True
                for cell in row:
                    if cell != first_value:
                        equals = False
                if equals:
                    return first_value
        # check vertically
        for i in range(self.size):
            first_value = self.matrix[0][i]
            if first_value != 0:
                equals = True
                for j in range(self.size):
                    if self.matrix[j][i] != first_value:
                        equals = False
                if equals:
                    return first_value
        # check vertically
        if self.matrix[0][0]!=0 and (self.matrix[0][0]==self.matrix[1][1]==self.matrix[2][2]):
            return self.matrix[0][0]
        if self.matrix[2][0]!=0 and (self.matrix[2][0]==self.matrix[1][1]==self.matrix[0][2]):
            return self.matrix[2][0]
        # else no winner
        return 0
    def events(self):
        winner = self.check_win()
        if winner != 0:
            self.waiting = True
            self.winner = winner
        if not self.waiting:
            self.check_clicks()
    def enable_replay(self):
        if self.waiting:
            self.waiting = False
            self.winner = None
            self.initialize_matrix()
    def run(self):
        while self.play:
            self.surface.blit(background, (0, 0))
            self.mouse=pygame.mouse.get_pos()
            self.click=pygame.mouse.get_pressed()
            for event in pygame.event.get():
                if event.type==QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type==KEYDOWN:
                    if event.key==K_TAB:
                        self.play=False
                    elif event.key==K_SPACE:
                        self.enable_replay()
            #--------------------------------------------------------------
            self.render()
            self.events()
            # -------------------------------------------------------------
            pygame.display.update()
            ft.tick(fps)



if  __name__ == "__main__":
    game = Game(surface)
    game.run()
