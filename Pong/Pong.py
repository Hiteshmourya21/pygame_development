import pygame 
import sys
from pygame.locals import*


pygame.mixer.init()
pygame.init()
black = (0,0,0)
grey = (180,180,180)
screen_w = 1360
screen_h = 768
sound = pygame.mixer.Sound('Stardew.wav')
sound.play(loops=-1)
sound.set_volume(0.3)
beep = pygame.mixer.Sound('Beep.wav')
hit =  pygame.mixer.Sound('mixkit-bed-pillow-hit-the-mattress-1901.wav')
screen = pygame.display.set_mode((screen_w,screen_h))
pygame.display.set_caption("Pong")
clock = pygame.time.Clock()
font = pygame.font.SysFont(False,30)
pygame.display.update()
r_font = pygame.font.SysFont(False,60)
ball = pygame.Rect((screen_w/2-15,screen_h/2,20,20)) 
speed = 5
velx = 1
vely = 1
timer = 0
start_time =0
new_session =1
start_time =True
player_score = 0
opponet_score = 0 

def text_font(text,color,x,y):
    screen_text = font.render(text,True,color)
    screen.blit(screen_text,[x,y])
def text_rfont(text,color,x,y):
    screen_text = r_font.render(text,True,color)
    screen.blit(screen_text,[x,y])

def ball_reset(timer,start_time): 
    current_time = timer - start_time
    timer_surf = font.render(f'{current_time}',True,'grey')
    timer_surf = pygame.transform.rotozoom(timer_surf,0,3)
    timer_rect = timer_surf.get_rect(midbottom = (500,screen_h/2))
    if current_time >3:
         ball_run()
    else:
         screen.blit(timer_surf,timer_rect)
         
    return current_time
    
     
def ball_run():
    global ball,velx,vely,player_score,opponet_score
    ball.x += velx*speed
    ball.y += vely*speed  
    if ball.top <= 0 or ball.bottom>=screen_h:
        vely *= -1
    if ball.left <= 0  :
        velx *= 1
    
        beep.play()
    if ball.right >= screen_w :
        velx *= 1         
        beep.play()
        beep.set_volume(0.2) 
       
vec_y = 0
op_vec_y = 0
fps = 60
game=True
playerx =screen_w-20
opponetx =10
  
player = pygame.Rect((playerx,screen_h/2-70,10,140))   
opponet =  pygame.Rect((opponetx,screen_h/2-70,10,140)) 

# speed_timer = pygame.USEREVENT + 1
# pygame.time.set_timer(speed_timer,800)
    
while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and not  game:
                        game = True
                        player_score = 0
                        opponet_score =0
                        ball = pygame.Rect((screen_w/2-15,screen_h/2,20,20))
                        speed = 5

                # if event.type == speed_timer and game:
                #      ru = random.choice(11,22)
                    
        if game:

            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP] :
                   player.y += -12 
                    #vec_y = -10
            elif keys[pygame.K_DOWN] :
                  player.y += 12
                    #vec_y = 10
            
            #player.y += vec_y
            if opponet.top > ball.bottom and  ball.left < screen_w/2:
                # opponet.y +=  -1*12
                op_vec_y = -8
            elif opponet.bottom < ball.bottom and ball.left < screen_w/2:
                # opponet.y += 12
                op_vec_y = 8
            opponet.y += op_vec_y

            if keys[pygame.K_q] :
                    fps += 1     

            if ball.colliderect(player) and velx > 0:
                speed += 0.5
                hit.set_volume(0.8)
                hit.play()
                if abs(ball.right - player.left)<10:
                    velx *= -1 
                elif abs(ball.bottom - player.top)<10 and vely > 0:
                    vely *= -1 
                elif abs(ball.top - player.bottom)<10 and vely < 0:
                    vely *= -1 
            if ball.colliderect(opponet) and velx < 0:
                speed += 0.5
                hit.set_volume(0.8)
                hit.play()
                if abs(ball.left - opponet.right)<10:
                    velx *= -1 
                elif abs(ball.bottom - opponet.top)<10 and vely > 0:
                    vely *= -1 
                elif abs(ball.top - opponet.bottom)<10 and vely < 0:
                    vely *= -1    

            if player_score >= 10 or opponet_score >= 10 :
                game = False 
                        
            if player.y <= 0  :
                player.y = 0
            if player.y >= screen_h-140:
                player.y = screen_h-140    
            if opponet.y <= 0 :
                opponet.y = 0
            if  opponet.y >= screen_h-140:
                opponet.y = screen_h-140  \
                 
            
            screen.fill(black)
            text_font('Player1 Score: '+str(player_score),grey,800,50)
            text_font('Player2 Score: '+str(opponet_score),grey,100,50)
            pygame.draw.rect(screen,grey,player)           
            pygame.draw.rect(screen,grey,opponet)           
            pygame.draw.aaline(screen,grey,(screen_w/2,0),(screen_w/2 ,screen_h)) 
            pygame.draw.ellipse(screen,grey,ball)       
            
            if ball.left < 1:
                speed =5
                player_score+=1
                ball = pygame.Rect((screen_w/2-15,screen_h/2,20,20))
                start_time = int(pygame.time.get_ticks()/1000)  
                   
            elif ball.right > playerx +15:
                 speed =5
                 opponet_score += 1
                 ball = pygame.Rect((screen_w/2-15,screen_h/2,20,20))
                 start_time = int(pygame.time.get_ticks()/1000)
            
            timer =int(pygame.time.get_ticks()/1000)
            ball_reset(timer,start_time)

        else :
            screen.fill(black)
            if player_score > opponet_score:
                text_rfont('Player1 Wins: ',grey,600,300)
            if player_score < opponet_score:
                text_rfont('Player2 Wins: ',grey,600,300)
            if player_score == opponet_score:
                text_rfont('Tie: ',grey,600,300)

        pygame.display.flip()
        pygame.display.update()
        clock.tick(fps)