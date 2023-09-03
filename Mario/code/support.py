import pygame
from csv import reader
from settings import tilt_size
from os import walk

def import_folder(path):
    surface_list = []
    for _,__,image_files in walk(path):
        for image in image_files:
            full_path = path +'/'+ image
            image_surf = pygame.image.load(full_path).convert_alpha()
            surface_list.append(image_surf)
    #print(surface_list)
    return surface_list

def import_csv_layout(path):
    terrain_map = []
    with open(path) as map :
        level = reader(map,delimiter = ',')
        for row in level:
            terrain_map.append(list(row))
        
        return terrain_map
    
def import_cut_graphics(path):
    surface = pygame.image.load(path).convert_alpha()
    tile_num_x = int(surface.get_size()[0] / tilt_size)
    tile_num_y = int(surface.get_size()[1] / tilt_size)

    cut_tiles = []
    for row in range(tile_num_y):
        for col in range(tile_num_x):
            x = col*tilt_size 
            y = row*tilt_size
            new_surface = pygame.Surface((tilt_size,tilt_size),flags = pygame.SRCALPHA)
            new_surface.blit(surface,(0,0),pygame.Rect(x,y,tilt_size,tilt_size))
            cut_tiles.append(new_surface)
        
    return cut_tiles