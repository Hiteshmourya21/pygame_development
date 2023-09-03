import pygame
from support import import_folder
from math import sin


class Player(pygame.sprite.Sprite):
    def __init__(self,pos,surface,create_jump_particles,change_health):
        super().__init__()
        self.import_character_asset()
        self.frame_index = 0
        self.animation_speed = 0.1
        self.image = self.animation['idle'][self.frame_index]
        self.rect = self.image.get_rect(topleft = pos)

        self.jump_sound = pygame.mixer.Sound('../audio/effects/jump.wav')
        self.jump_sound.set_volume(0.1)
        self.hit_sound = pygame.mixer.Sound('../audio/effects/hit.wav')
        self.hit_sound.set_volume(0.3)

        self.import_dust_run()  
        self.dust_frame_index = 0
        self.dust_animation_speed = 0.1
        self.display_surface = surface
        self.create_jump_particle = create_jump_particles

        self.direction = pygame.math.Vector2(0,0)
        self.speed = 8
        self.gravity =0.8
        self.jump_speed = -16
        self.collision_rect = pygame.Rect(self.rect.topleft,(50 ,self.rect.height))

        self.status = 'idle'
        self.facing_right = True
        self.on_ground = False
        self.on_celling = False
        self.on_left = False
        self.on_right = False

        self.change_health = change_health
        self.invincible = False
        self.invincibility_duration = 900
        self.hurt_time = 0

    def import_character_asset(self):
        character_path = '../graphics\character/'
        self.animation = {'idle':[],'run':[],'jump':[],'fall':[]}

        for animation in self.animation.keys():
                full_path = character_path + animation
                self.animation[animation] = import_folder(full_path)

    def import_dust_run(self):
        self.dust_run_particle = import_folder('..\graphics\character\dust_particles/run')

    def get_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.direction.x = -1
            self.facing_right =False
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.direction.x = 1
            self.facing_right = True
        else    :
            self.direction.x = 0
        if keys[pygame.K_SPACE] and self.on_ground:
            self.jump()
            self.create_jump_particle(self.rect.midbottom)

    def animate(self):
        animation = self.animation[self.status]

        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0

        image = animation[int(self.frame_index)]
        if self.facing_right :
            self.image = image
            self.rect.bottomleft = self.collision_rect.bottomleft

        else : 
            flipped_image = pygame.transform.flip(image,True,False)
            self.image = flipped_image
            self.rect.bottomright = self.collision_rect.bottomright

        if self.invincible:
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)

        self.rect =self.image.get_rect(midbottom = self.rect.midbottom)

        

    def run_dust_animation(self):
        if self.status == 'run' and self.on_ground:
            self.dust_frame_index += self.dust_animation_speed
            if self.dust_frame_index > len(self.dust_run_particle):
                self.dust_frame_index = 0

            dust_particel = self.dust_run_particle[int(self.dust_frame_index)]

            if self.facing_right :
                pos = self.rect.bottomleft - pygame.math.Vector2(6,10)
                self.display_surface.blit(dust_particel,pos)
            else :
                pos = self.rect.bottomright - pygame.math.Vector2(6,10)
                flipped_dust_particle = pygame.transform.flip(dust_particel,True,False)
                self.display_surface.blit(flipped_dust_particle,pos)
        
    def get_status(self):
        if self.direction.y < 0:
            self.status = 'jump'
        elif self.direction.y > 1 :
            self.status = 'fall'
        else :
            if self.direction.x  != 0:
                self.status = 'run'
            else :
                self.status = 'idle'

    def apply_gravity(self):
        self.direction.y += self.gravity
        self.collision_rect.y +=  self.direction.y

    def jump(self):
            self.jump_sound.play()
            self.direction.y = self.jump_speed

    def get_damage(self):
        if not self.invincible:
            self.hit_sound.play()
            self.change_health(-10)
            self.invincible = True
            self.hurt_time = pygame.time.get_ticks()
    def invincibility_timer(self):
        if self.invincible:
            current_time = pygame.time.get_ticks()
            if current_time - self.hurt_time >= self.invincibility_duration:
                self.invincible = False

    def wave_value(self):
        value = sin(pygame.time.get_ticks())
        if value >= 0 :return 255
        else : return 0

    def update(self):
        self.get_input()
        self.get_status()
        self.animate()
        self.run_dust_animation()
        self.invincibility_timer()