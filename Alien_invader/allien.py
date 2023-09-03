import pygame

class Allien(pygame.sprite.Sprite):
    def __init__(self,color,x,y):
        super().__init__()
        file_path = './images/' +color +'.png'
        self.image = pygame.image.load(file_path).convert_alpha()
        self.rect =self.image.get_rect(topleft = (x,y))

        if color == 'red': self.value = 100
        elif color == 'green': self.value = 200
        elif color == 'yellow': self.value = 300

    def update(self,direction,num):
        self.rect.x += direction*num   

class Extra(pygame.sprite.Sprite):
    def __init__(self,side,screen_w):
        super().__init__()
        self.image = pygame.image.load('.\images\extra.png').convert_alpha()
        self.power = pygame.sprite.Group()
        if side == 'right':
            x = screen_w+50
            self.speed =  -3
        else :
            x = -50
            self.speed = 3
        self.rect = self.image.get_rect(topleft = (x,50))
        #self.power.add(Power(self.rect.center,700,-8))

    def update(self):
        self.rect.x += self.speed
            

