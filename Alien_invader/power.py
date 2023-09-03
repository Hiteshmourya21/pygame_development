import pygame

class Power(pygame.sprite.Sprite ):
    def __init__(self,pos,screen_h,speed,type):
        super().__init__()
        self.image = pygame.Surface((4,20)) 
        if type == 'health':
            self.image.fill('red')
        if type == 'speed':
            self.image.fill('green')
        self.rect = self.image.get_rect(center = pos)
        self.speed = speed
        self.height_y_constraint = screen_h
    
    def destroy(self):
        if self.rect.y <= -50 or self.rect.y >= self.height_y_constraint:
            self.kill()

    def update(self):
        self.rect.y += self.speed
        self.destroy()