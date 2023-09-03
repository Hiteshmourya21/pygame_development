from pickle import TRUE
import pygame
import sys
from math import sin
from laser import Laser
from power import Power
import obsticale
from random import choice,randint
from allien import Allien,Extra
from player import Player


pygame.init()
pygame.mixer.init()
screen_w = 1360
screen_h = 768
screen = pygame.display.set_mode((screen_w,screen_h))
pygame.display.set_caption("Alien Invasion")
clock = pygame.time.Clock()
over = False
score = 0
Bg_music = pygame.mixer.Sound('.\music\music.wav')
Bg_music.set_volume(0.1)
Bg_music.play(loops = -1)
with open('.\hiscore.txt','r') as f:
    hiscore = f.read()
i = 1
a = 1
s = 100
class Game():
    global screen
    def __init__(self) :
        self.blin = Player((screen_w/2,screen_h),screen_w,5)
        player_sprite = Player((screen_w/2,screen_h),screen_w,5)
        self.player =pygame.sprite.GroupSingle(player_sprite)

        self.lives = 3
        self.live_surf = pygame.image.load('.\images\space_ship.bmp').convert_alpha()
        self.live_x_start_pos = screen_w - (self.live_surf.get_size()[0]*2 + 20)
        self.font = pygame.font.Font('.\images\Pixeled.ttf',20)

        self.shape = obsticale.shape
        self.block_size = 15
        self.blocks = pygame.sprite.Group()
        self.obstacle_ammount = 4
        self.obstacle_x_position = [num*(screen_w/self.obstacle_ammount) for num in range(self.obstacle_ammount)]
        self.creat_multiple_obstacle(*self.obstacle_x_position,x_start = screen_w/10 ,y_start =450,)

        self.allien =pygame.sprite.Group()
        self.allien_setup(rows= 7,cols=16)
        self.allien_direction = 1
        self.num = 2
        self.allien_lasers =pygame.sprite.Group()

        self.extra = pygame.sprite.GroupSingle() 
        self.extra_spawn_time = randint(60,120)
        self.extra_laser = pygame.sprite.Group()

        self.laser_sound = pygame.mixer.Sound('.\music\laser.wav')
        self.laser_sound.set_volume(0.1)
        self.explosion_sound = pygame.mixer.Sound('.\music\explosion.wav')
        self.explosion_sound.set_volume(0.1)
        self.player_hit_sound = pygame.mixer.Sound('.\music\pyhit.wav')
        self.player_hit_sound.set_volume(1.0)

        self.sheild = False
        self.timer = 0
        self.timer_duration = 3000
        self.current_time = 0

        self.power_life = False
        self.power_speed = False
        self.power_cooldown = 800
        self.power_type = " "
        
    def create_obstacle(self,x_start,y_start,offset_x):
        for row_index,row in enumerate(self.shape):
            for col_index,col in enumerate(row):     
                if col == 'X':
                    x = x_start + col_index*self.block_size + offset_x
                    y = y_start + row_index*self.block_size + 100
                    block = obsticale.Block(self.block_size,(241,79,80),x,y)
                    self.blocks.add(block)

    def creat_multiple_obstacle(self,*offset,x_start,y_start):
        for offset_x in offset:
            self.create_obstacle(x_start,y_start,offset_x)

    def allien_setup(self,rows,cols,x_distance=60,y_distance=48,x_offset= 200,y_offset=80):
        for row_index,row in enumerate(range(rows)):
            for col_index,col in enumerate(range(cols)):
                x = col_index * x_distance + x_offset
                y = row_index * y_distance  + y_offset
                if row_index == 0 : allien_sprite = Allien('yellow',x,y)
                elif 1<=row_index <= 2 : allien_sprite = Allien('green',x,y)
                else : allien_sprite = Allien('red',x,y)
                self.allien.add(allien_sprite)

    def allien_positon_checkup(self):
        all_allien =self.allien.sprites()
        for alien in all_allien:
            if alien.rect.right >= screen_w:
                self.allien_direction = -1
                self.allien_move_down(2)
            elif alien.rect.left <= 0:
                self.allien_direction = 1
                self.allien_move_down(2)

    def allien_move_down(self,distance):
        if self.allien:
            for alien in self.allien.sprites():
                alien.rect.y += distance 
                if alien.rect.y >= 600 :
                    distance = 0

    def extra_allein_time(self):
        self.extra_spawn_time -= 1
        if self.extra_spawn_time <= 0:
            self.extra.add(Extra(choice(['right','left']),screen_w))
            self.extra_spawn_time = randint(600,1200)
  
    def allien_shoot(self):    
        global i ,a                 
        if self.allien.sprites():
            while i!=0:
                random_alien = choice(self.allien.sprites())
                laser_sprite = Laser(random_alien.rect.center,screen_h,6)
                self.allien_lasers.add(laser_sprite)
                self.laser_sound.play()
                i -= 1
            i = a
        
    def extra_shoot(self,pos):
        self.power_type = choice(['health','speed'])
        laser_sprite = Power(pos,screen_h,6,self.power_type)
        self.extra_laser.add(laser_sprite)

    def collision_checks(self):
        global over ,score
        if self.player.sprite.lasers:
            for laser in self.player.sprite.lasers:
                if pygame.sprite.spritecollide(laser,self.blocks,False) and self.power_speed:       
                    pass#laser.kill()
                elif  pygame.sprite.spritecollide(laser,self.blocks,True) and not self.power_speed:
                    laser.kill()

                if pygame.sprite.spritecollide(laser,self.extra,True):
                    score += 500
                    self.extra_shoot(laser.rect.center)
                    laser.kill()
                    self.explosion_sound.play()
                    
                alien_hit =  pygame.sprite.spritecollide(laser,self.allien,True)
                if alien_hit:
                    for alien in alien_hit :
                        score += alien.value
                        laser.kill()
                        self.explosion_sound.play()

        if self.extra_laser:
            for laser in self.extra_laser:
                if pygame.sprite.spritecollide(laser,self.player,False) and self.power_type == 'health':
                    self.power_life = True
                    laser.kill()
                elif pygame.sprite.spritecollide(laser,self.player,False) and self.power_type == 'speed':
                    self.power_speed = True
                    laser.kill()

        if self.allien_lasers:
            global shiel,s
            for laser in self.allien_lasers:
               if pygame.sprite.spritecollide(laser,self.blocks,True):       
                    laser.kill()   
               if pygame.sprite.spritecollide(laser,self.player,False) and not self.sheild:       
                    laser.kill()
                    self.player_hit_sound.play()
                    self.sheild = True
                    self.lives -=1
                    self.timer   = pygame.time.get_ticks()            
                    if self.lives <= 0:
                        over = True

        if self.allien:
            for alien in self.allien:
                pygame.sprite.spritecollide(alien,self.blocks,True)
                if  pygame.sprite.spritecollide(alien,self.player,False):
                   over = TRUE
                keys = pygame.key.get_pressed()
                if keys[pygame.K_e] :
                    over = TRUE

    def invincible(self):
        if self.sheild:
            self.current_time  = pygame.time.get_ticks()
            alpha = self.wave_value()
            self.player.sprite.image.set_alpha(alpha)
        else:
            self.player.sprite.image.set_alpha(255)  
             
        if self.current_time - self.timer >= self.timer_duration:
                self.sheild = False 
        
    def Powers(self):
        if self.power_life:
            self.lives += 1
            self.power_life = False

        if self.power_speed:
            self.power_cooldown -= 1
            if self.power_cooldown <=0:
                self.power_speed = False

    def wave_value(self):
        value = sin(pygame.time.get_ticks())
        if value >= 0 :return 255
        else : return 0

    def display_live(self):
        for live in range(self.lives - 1):
            x = self.live_x_start_pos + (live*(self.live_surf.get_size()[0]+10))
            screen.blit(self.live_surf,(x,8))

    def display_score(self):
        score_surf = self.font.render(f'score : {score}',False,"light blue")
        score_rect = score_surf.get_rect(topleft = (10,-10))
        screen.blit(score_surf,score_rect)
    
    def display_hiscore(self):
        hiscore_sur = self.font.render(f'Hiscore : {hiscore}',False,"light green")
        hiscore_rect = hiscore_sur.get_rect(topleft = (screen_w/2-70,-10))
        screen.blit(hiscore_sur,hiscore_rect)  

    def victory_message(self):
        global a
        if not self.allien.sprites():
            victory_surf = self.font.render('You Won Press ENTER To CONTINUE',False,'white')
            victory_rect = victory_surf.get_rect(center = (screen_w/2,screen_h/2))
            screen.blit(victory_surf,victory_rect) 
            self.lives = 3
            keys = pygame.key.get_pressed()
            if keys[pygame.K_RETURN] :
                if a > 3:
                    a = 3
                else:
                    a +=1
                run_game()

    def hi_score(self):
        global hiscore
        if score > int(hiscore):
            hiscore = str(score)

    def run(self):
        self.player.sprite.lasers.draw(screen)
        self.allien_lasers.draw(screen)
        self.extra_laser.draw(screen)
        self.extra.draw(screen)
        self.player.draw(screen)
        self.blocks.draw(screen)
        self.allien.draw(screen)

        self.player.update() 
        self.allien.update(self.allien_direction,self.num)
        self.allien_lasers.update()
        self.extra_laser.update()
        
        self.extra_allein_time()
        self.extra.update()

        self.allien_positon_checkup()
        self.hi_score()
        self.display_score()
        self.collision_checks()
        self.display_hiscore()
        self.victory_message()

        self.invincible()
        self.Powers()
        self.display_live()

    
class CRT:
    def __init__(self) :
        self.tv = pygame.image.load('.\images/tv.png').convert_alpha()
        self.tv  = pygame.transform.scale(self.tv,(screen_w,screen_h))

    def creat_crt_line(self):
        line_height = 3
        line_ammount = int(screen_h/line_height)
        for line in range(line_ammount):
            y_pos = line*line_height
            pygame.draw.line(self.tv,"black",(0,y_pos),(screen_w,y_pos),1)

    def draw(self):
        self.tv.set_alpha(randint(75,90))
        self.creat_crt_line()
        screen.blit(self.tv,(0,0))
                  
def run_game(): 
    global over
    pygame.mouse.get_visible()
    pygame.mouse.set_visible(False)
    game = Game()
    crt = CRT()
    ALIENLASER = pygame.USEREVENT + 1
    pygame.time.set_timer(ALIENLASER,800)
    while True:
        if over:
          game_over()  
        else:       
            for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        sys.exit()
                    if event.type == ALIENLASER:
                        game.allien_shoot()
            screen.fill((30,30,30))
            game.run()
            crt.draw() 
            pygame.display.flip()
        pygame.display.update()
        clock.tick(60)                              

def game_over():
    global over ,score
    game = Game()
    pygame.mouse.get_visible()
    pygame.mouse.set_visible(True)
    screen.fill((0,0,0)) 
    with open('.\hiscore.txt','w')as f:
        f.write(hiscore)
    welcome_screen = pygame.image.load('.\images\welcome.jpg').convert_alpha()
    welcome_screen = pygame.transform.scale(welcome_screen,(screen_w,screen_h))
    screen.blit(welcome_screen,(0,0))
    game_over_surf = game.font.render('You Loss',False,'red')
    game_over_rect = game_over_surf.get_rect(center = (screen_w/2,screen_h/2+100))
    screen.blit(game_over_surf,game_over_rect) 
    score_surf = game.font.render('Your Score: ' + str(score),False,'green')
    score_rect = score_surf.get_rect(center = (screen_w/2+10,screen_h/4+20))
    screen.blit(score_surf,score_rect) 
    exit_surf = game.font.render('Press ENTER To ConTinue',False,'purple ')
    exit_rect = exit_surf.get_rect(center = (screen_w/2,screen_h-120))
    screen.blit(exit_surf,exit_rect)
    for event in pygame.event.get():
        if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
                if event.key == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_RETURN:
                    over = False
                    score = 0 
                    welcome()

def welcome():
    screen.fill((0,0,0))
    pygame.mouse.get_visible()
    pygame.mouse.set_visible(True)
    game = Game()
    welcome = pygame.image.load('.\images\space-alien-invaders.png').convert_alpha()
    welcome = pygame.transform.scale(welcome,(screen_w,screen_h))
    screen.blit(welcome,(0,0))
    hiscore_sur = game.font.render(f'Hiscore : {hiscore}',False,"green" )
    hiscore_rect = hiscore_sur.get_rect(topleft = (555,400))
    screen.blit(hiscore_sur,hiscore_rect)
    pygame.draw.rect(screen,"green",(540,390,270,80),3)
    start = False
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT :
                if event.key == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and start:
                global a
                a = 1
                run_game()
        pygame.draw.rect(screen,"green",(540,390,270,80),3)
        mouse = pygame.mouse.get_pos()
        if abs(hiscore_rect.x -mouse[0])<350 and abs(hiscore_rect.y - mouse[1])<200 :
            pygame.draw.rect(screen,"white",(560,506,250,80),3)
            start = True
        else:
            pygame.draw.rect(screen,"black",(560,506,250,80),3)
            start = False
        pygame.display.flip()                 
        pygame.display.update()
welcome()
