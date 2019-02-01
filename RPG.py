import os
import random
import pygame
import sys

pygame.init()

FPS = 60
WIDTH = 800
HEIGHT = 700
TILE_WIDTH = TILE_HEIGHT = 50

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

all_sprites = pygame.sprite.Group()  # Группа всех спрайтов
map_group = pygame.sprite.Group()  # Спрайты карты
player_group = pygame.sprite.Group()  # Спрайты персонажей


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


tile_images = {
    'granny': load_image('granny.png'),
    'empty': load_image('grass.png'),
    'player': load_image('hero.jpg'),
    # 'badguy': load_image('mario.png')
}


def generate_level(level):
    new_player = None
    main_granny = None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '$':
                Tile('granny', x, y)
                main_granny = Granny(x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                new_player = MainHero(x, y)

    return new_player, main_granny


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(map_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(TILE_WIDTH * pos_x,
                                               TILE_HEIGHT * pos_y)


def load_level(filename):
    filename = 'data/' + filename

    with open(filename, 'r') as map_file:
        level_map = [line.strip() for line in map_file]

    max_width = max(map(len, level_map))

    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    intro_text = ["ИГРА ГОДА!   КОРМИ ГУЛЬ БАБУЛИ", "",
                  "Правила игры:",
                  "Корми голубей семечками",
                  "",
                  "Не попадись гопнику на глаза!"]

    fon = pygame.transform.scale(load_image('grannyFull.jfif'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('Brown'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(FPS)


class MainHero(pygame.sprite.Sprite):
    pass


class Granny(pygame.sprite.Sprite):
    pass

start_screen()

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
    map_group.draw(screen)
    player_group.draw(screen)

    pygame.display.flip()
    clock.tick(FPS)
terminate()
