from csv import reader
from os import walk, sep
import pygame
import re

def natural_key(string_):
    return [int(s) if s.isdigit() else s for s in re.split(r'(\d+)', string_)]


def import_folder(path):
    surface_list = []
    for _, __, image_files in walk(path):
        sorted_files = sorted(image_files, key=natural_key)
        for image in sorted_files:
            full_path = path + '/' + image
            image_surf = pygame.image.load(full_path).convert_alpha()
            surface_list.append(image_surf)

    return surface_list


def import_cut_graphics(path):
    surface = pygame.image.load(path).convert_alpha()
    tile_num_x = int(surface.get_size()[0] / 64)
    tile_num_y = int(surface.get_size()[1] / 64)

    cut_tiles = []
    for row in range(tile_num_y):
        for col in range(tile_num_x):
            x = col * 64
            y = row * 6
            new_surf = pygame.Surface(
                (64, 64), flags=pygame.SRCALPHA)
            new_surf.blit(surface, (0, 0), pygame.Rect(
                x, y, 64, 64))
            cut_tiles.append(new_surf)

    return cut_tiles


def scale_images(images: list, size: tuple):
    """ returns scaled image assets """
    scaled_images = []
    for image in images:
        scaled_images.append(pygame.transform.scale(image, size))
    return scaled_images


_text_library = {}
def draw_text(surf, text, pos, size=30, color=(255,255,255), bg_color=None):
    global _text_library
    text_surf = _text_library.get(f"{text}{color}{size}")
    if text_surf is None:
        font = pygame.font.Font('font/minotaur.ttf', size)
        text_surf = font.render(text, True, color, bg_color)
        _text_library[f"{text}{color}{size}"] = text_surf
    x, y = pos
    surf.blit(text_surf, (x - (text_surf.get_width() // 2), y - (text_surf.get_height() // 2)))

_image_library = {}
def get_image(path):
    global _image_library
    image = _image_library.get(path)
    if image == None:
        canonicalized_path = path.replace('/', sep).replace('\\', sep)
        image = pygame.image.load(canonicalized_path)
        _image_library[path] = image
    return image