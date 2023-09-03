import pygame
from settings import tilt_size ,screen_height ,screen_width
from support import import_csv_layout , import_cut_graphics
from Tiles import Tile , Statictile , Crate , Coin ,Palm
from enemy import Enemy
from decoration import Sky ,Water , Cloud
from player import Player
from particles import Particle_effect
from game_data import levels

class Level():
    def __init__(self,current_level,surface,create_overworld,change_coin,change_health):

        self.display_surface = surface
        self.world_shift = 0
        self.current_x = None

        self.coin_sound = pygame.mixer.Sound('../audio/effects/coin.wav')
        self.coin_sound.set_volume(0.1)
        self.stomp_sound = pygame.mixer.Sound('../audio/effects/stomp.wav')
        self.stomp_sound.set_volume(0.2)

        self.create_overworld = create_overworld
        self.current_level = current_level
        level_data = levels[self.current_level]
        self.new_max_level = level_data['unlock']

        self.change_coins  = change_coin

        self.player_on_ground =False

        player_layout = import_csv_layout(level_data['player'])
        self.player = pygame.sprite.GroupSingle()
        self.goal = pygame.sprite.GroupSingle()
        self.player_setup(player_layout,change_health)

        self.dust_sprite = pygame.sprite.GroupSingle()

        self.explosion_sprite = pygame.sprite.Group()

        terrain_layout = import_csv_layout(level_data['terrain'])
        self.terrain_sprite = self.create_tile_group(terrain_layout,'terrain')

        grass_layout = import_csv_layout(level_data['grass'])
        self.grass_sprite = self.create_tile_group(grass_layout,'grass')

        crates_layout = import_csv_layout(level_data['crates'])
        self.crate_sprite = self.create_tile_group(crates_layout,'crates')

        coin_layout = import_csv_layout(level_data['coins'])
        self.coin_sprite = self.create_tile_group(coin_layout,'coins')

        fg_palm_layout = import_csv_layout(level_data['fg_palms'])
        self.fg_palms_sprite = self.create_tile_group(fg_palm_layout,'fg_palms')

        bg_palm_layout = import_csv_layout(level_data['bg_palms'])
        self.bg_palms_sprite = self.create_tile_group(bg_palm_layout,'bg_palms')

        enemy_layout = import_csv_layout(level_data['enemies'])
        self.enemy_sprite = self.create_tile_group(enemy_layout,'enemies')

        constrain_layout = import_csv_layout(level_data['constrains'])
        self.constrain_sprtie = self.create_tile_group(constrain_layout,'constrains')

        self.sky = Sky(8)
        level_width = len(terrain_layout[0])*tilt_size
        self.water = Water(screen_height - 40,level_width)
        self.clouds = Cloud(400,level_width,15)

    def create_tile_group(self,layout,type):
        sprite_group = pygame.sprite.Group()

        for row_index,row in enumerate(layout):
            for col_index,value in enumerate(row) :
                if value !='-1':
                    x= col_index*tilt_size
                    y= row_index*tilt_size

                    if type == 'terrain':
                        terrain_tile_list = import_cut_graphics('../graphics/terrain/terrain_tiles.png')
                        tile_surface = terrain_tile_list[int(value)]
                        sprite = Statictile(tilt_size,x,y,tile_surface)
                    
                    if type == 'grass':
                        grass_tile_list = import_cut_graphics('../graphics/decoration/grass/grass.png')
                        tile_surface = grass_tile_list[int(value)]
                        sprite = Statictile(tilt_size,x,y,tile_surface)

                    if type == 'crates':
                        sprite = Crate(tilt_size,x,y)

                    if type == 'coins':
                        if value == '0':
                         sprite = Coin(tilt_size,x,y,'../graphics/coins/gold',5)
                        else:
                         sprite = Coin(tilt_size,x,y,'../graphics/coins/silver',1)  

                    if type == 'fg_palms':
                        if value == '1':sprite = Palm(tilt_size,x,y,'../graphics/terrain/palm_small',38)
                        if value == '2':sprite = Palm(tilt_size,x,y,'../graphics/terrain/palm_large',64)

                    if type == 'bg_palms':
                        sprite = Palm(tilt_size,x,y,'../graphics/terrain/palm_bg',64)

                    if type == 'enemies':
                        sprite = Enemy(tilt_size,x,y)
                        
                    if type == 'constrains':
                        sprite = Tile(tilt_size,x,y)

                    sprite_group.add(sprite)

        return sprite_group
    
    def enemy_collision_reverse(self):
        for enemy in self.enemy_sprite.sprites():
            if pygame.sprite.spritecollide(enemy,self.constrain_sprtie,False):
                enemy.reverse()

    def player_setup(self,layout,change_health):
        for row_index,row in enumerate(layout):
            for col_index,value in enumerate(row) :
                x= col_index*tilt_size
                y= row_index*tilt_size
                    
                if value =='0':
                    sprite = Player((x,y),self.display_surface,self.create_jump_particle,change_health )
                    self.player.add(sprite)

                if value == '1':
                    hat_surface =  pygame.image.load('../graphics/character/hat.png').convert_alpha()
                    sprite = Statictile(tilt_size,x,y,hat_surface)
                    self.goal.add(sprite)

    def create_jump_particle(self,pos):
        if self.player.sprite.facing_right :
            pos -= pygame.math.Vector2(10,5)
        else:
            pos += pygame.math.Vector2(10,-5)
        jump_particle_sprite = Particle_effect(pos,'jump')
        self.dust_sprite.add(jump_particle_sprite)

    def horizontal_movement_collision(self):
        player =self.player.sprite
        player.collision_rect.x += player.direction.x*player.speed       
        collidable_sprites =  self.terrain_sprite.sprites() + self.crate_sprite.sprites() + self.fg_palms_sprite.sprites()
        for sprite in collidable_sprites:
            if sprite.rect.colliderect(player.collision_rect):
                if player.direction.x < 0 :
                    player.collision_rect.left = sprite.rect.right
                    player.on_left = True
                    self.current_x = player.rect.left
                elif player.direction.x > 0 :
                    player.collision_rect.right = sprite.rect.left
                    player.on_right = True
                    self.current_x = player.rect.right


    def vertical_movement_collision(self):
        player =self.player.sprite
        player.apply_gravity()
        collidable_sprites =  self.terrain_sprite.sprites() + self.crate_sprite.sprites() + self.fg_palms_sprite.sprites()

        for sprite in collidable_sprites:
            if sprite.rect.colliderect(player.collision_rect):
                if player.direction.y < 0 :
                    player.collision_rect.top = sprite.rect.bottom
                    player.direction.y =0
                    player.on_celling = True
                elif player.direction.y > 0 :
                    player.collision_rect.bottom = sprite.rect.top
                    player.direction.y =0
                    player.on_ground = True

        if player.on_ground and player.direction.y < 0 or player.direction.y > 1:
            player.on_ground = False

    def scroll_x(self):
        player = self.player.sprite
        player_x = player.rect.centerx
        direction_x = player.direction.x

        if player_x < int(screen_width*25/100) and direction_x < 0:
            self.world_shift = 8
            player.speed = 0
        elif player_x > int(screen_width*75/100) and direction_x > 0 :
            self.world_shift = -8
            player.speed = 0
        else :
            self.world_shift = 0
            player.speed = 8

    def get_player_on_ground(self):
        if self.player.sprite.on_ground: 
            self.player_on_ground = True
        else:
            self.player_on_ground = False
    
    def create_land_particle(self):
        if not self.player_on_ground and self.player.sprite.on_ground and not self.dust_sprite.sprites() :
            if self.player.sprite.facing_right :
             offset = pygame.math.Vector2(10,15)
            else:
             offset = pygame.math.Vector2(-10,15)
            fall_dust_particle = Particle_effect(self.player.sprite.rect.midbottom - offset,'land')
            self.dust_sprite.add(fall_dust_particle)

    def check_death(self):
        if self.player.sprite.rect.top > screen_height:
            self.create_overworld(self.current_level,0)

    def check_win(self):
        if pygame.sprite.spritecollide(self.player.sprite,self.goal,False):
            self.create_overworld(self.current_level,self.new_max_level)

    def check_coin_collision(self):
        collided_coin_list = pygame.sprite.spritecollide(self.player.sprite,self.coin_sprite,True)
        if collided_coin_list:
            self.coin_sound.play()
            for coin in collided_coin_list:
                self.change_coins(coin.value)


    def check_enemy_collision(self):
        enemy_collision = pygame.sprite.spritecollide(self.player.sprite,self.enemy_sprite,False)
        if enemy_collision:
            for enemy in enemy_collision:
                enemy_center = enemy.rect.centery
                enemy_top = enemy.rect.top
                player_bottom = self.player.sprite.rect.bottom
                if enemy_top < player_bottom < enemy_center and self.player.sprite.direction.y >= 0:
                    self.stomp_sound.play()
                    self.player.sprite.direction.y = -15
                    explosion_sprite = Particle_effect(enemy.rect.center,'explosion')
                    self.explosion_sprite.add(explosion_sprite)
                    enemy.kill()
                else:
                    self.player.sprite.get_damage()

    def run(self):
        self.sky.draw(self.display_surface)
        self.clouds.draw(self.display_surface,self.world_shift)

        self.bg_palms_sprite.update(self.world_shift)
        self.bg_palms_sprite.draw(self.display_surface)
    
        self.fg_palms_sprite.update(self.world_shift)
        self.fg_palms_sprite.draw(self.display_surface)

        self.dust_sprite.update(self.world_shift)
        self.dust_sprite.draw(self.display_surface)

        self.grass_sprite.update(self.world_shift)
        self.grass_sprite.draw(self.display_surface)

        self.crate_sprite.draw(self.display_surface)
        self.crate_sprite.update(self.world_shift)
        
        self.coin_sprite.update(self.world_shift)
        self.coin_sprite.draw(self.display_surface)

        self.constrain_sprtie.update(self.world_shift)
        self.enemy_collision_reverse()

        self.enemy_sprite.update(self.world_shift)
        self.enemy_sprite.draw(self.display_surface)

        self.explosion_sprite.update(self.world_shift)
        self.explosion_sprite.draw(self.display_surface)

        self.terrain_sprite.update(self.world_shift)
        self.terrain_sprite.draw(self.display_surface)

        self.player.update()
        self.horizontal_movement_collision()

        self.get_player_on_ground()
        self.vertical_movement_collision()
        self.create_land_particle()

        self.scroll_x()
        self.player.draw(self.display_surface)

        self.goal.update(self.world_shift)
        self.goal.draw(self.display_surface)

        self.check_death()
        self.check_win()
        
        self.check_coin_collision()
        self.check_enemy_collision()

        self.water.draw(self.display_surface,self.world_shift)
        
        