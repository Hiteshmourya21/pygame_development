from turtle import color
import pygame
class Block(pygame.sprite.Sprite):
    def __init__(self,size,color,x,y):
        super().__init__()
        self.image = pygame.Surface((size,size))
        self.image.fill(color)   
        self.rect = self.image.get_rect(topleft = (x,y))
        self.reset()
    
    def reset(self):
        self.rect.x = self.rect.x
        self.rect.y = self.rect.y

shape = [   
'  XXXXXXX',
' XXXXXXXXX',
'XXXXXXXXXXX',
'XXXXXXXXXXX',
'XXXXXXXXXXX',
'XXX     XXX',
'XX       XX']