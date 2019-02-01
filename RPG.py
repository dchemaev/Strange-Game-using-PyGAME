import os
import random
import pygame
import sys

pygame.init()

FPS = 60
WIDTH = 1920
HEIGHT = 1080
GRAVITY = 0.25
TILE_WIDTH = TILE_HEIGHT = 50

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

all_sprites = pygame.sprite.Group()


def load_image(name, color_key=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)
    image = image.convert_alpha()

    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    return image


screen_rect = (0, 0, WIDTH, HEIGHT)


class Hero(pygame.sprite.Sprite):
    pass

    def __init__(self):
        super().__init__(all_sprites)
        pass

    def update(self):
        pass


running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    all_sprites.update()
    screen.fill(pygame.Color("white"))
    all_sprites.draw(screen)

    pygame.display.flip()
    clock.tick(FPS)
pygame.quit()
