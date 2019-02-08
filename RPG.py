import os
import random
import pygame
import sys

pygame.init()
pygame.key.set_repeat(1, 10)

FPS = 60
STEP = 7
WIDTH = 600
HEIGHT = 600
TILE_WIDTH = TILE_HEIGHT = 50

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

all_sprites = pygame.sprite.Group()  # Группа всех спрайтов
map_group = pygame.sprite.Group()  # Спрайты карты
player_group = pygame.sprite.Group()  # Спрайты персонажей
granny_group = pygame.sprite.Group()
badguy_group = pygame.sprite.Group()


def load_image(name, color_key=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)
    # image = image.convert_alpha()

    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    return image


tile_images = {
    'granny': load_image('granny.png'),
    'empty': load_image('grass.png'),
    'player': load_image('hero.jpg'),
    'badguy': load_image('badguy.png')
}


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


def generate_level(level):
    new_player = None
    main_granny = None
    bad_guy = None
    x, y = None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.' or level[y][x] == "#":
                Tile('empty', x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                new_player = MainHero(x, y)
            elif level[y][x] == '$':
                Tile('empty', x, y)
                main_granny = Granny(x, y)
            elif level[y][x] == '%':
                Tile('empty', x, y)
                bad_guy = BadGuy(x, y)

    return new_player, main_granny, bad_guy, x, y


class Granny(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(granny_group, all_sprites)
        self.image = tile_images["granny"]
        self.rect = self.image.get_rect().move(TILE_WIDTH * pos_x,
                                               TILE_HEIGHT * pos_y)


class BadGuy(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(badguy_group, all_sprites)
        self.image = tile_images["badguy"]
        self.rect = self.image.get_rect().move(TILE_WIDTH * pos_x,
                                               TILE_HEIGHT * pos_y)


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


def clear():
    global all_sprites, map_group, player_group, granny_group
    all_sprites = pygame.sprite.Group()
    map_group = pygame.sprite.Group()  # Спрайты карты
    player_group = pygame.sprite.Group()  # Спрайты персонажей
    granny_group = pygame.sprite.Group()


class MainHero(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = tile_images['player']
        self.rect = self.image.get_rect().move(TILE_WIDTH * pos_x + 15,
                                               TILE_HEIGHT * pos_y + 5)


class Camera:
    # зададим начальный сдвиг камеры и размер поля для возможности реализации циклического сдвига
    def __init__(self, field_size):
        self.dx = 0
        self.dy = 0
        self.field_size = field_size

    # сдвинуть объект obj на смещение камеры
    def apply(self, obj):
        obj.rect.x += self.dx
        # вычислим координату клитки, если она уехала влево за границу экрана
        if obj.rect.x < -obj.rect.width:
            obj.rect.x += (self.field_size[0] + 1) * obj.rect.width
        # вычислим координату клитки, если она уехала вправо за границу экрана
        if obj.rect.x >= (self.field_size[0]) * obj.rect.width:
            obj.rect.x += -obj.rect.width * (1 + self.field_size[0])
        obj.rect.y += self.dy
        # вычислим координату клитки, если она уехала вверх за границу экрана
        if obj.rect.y < -obj.rect.height:
            obj.rect.y += (self.field_size[1] + 1) * obj.rect.height
        # вычислим координату клитки, если она уехала вниз за границу экрана
        if obj.rect.y >= (self.field_size[1]) * obj.rect.height:
            obj.rect.y += -obj.rect.height * (1 + self.field_size[1])

    # позиционировать камеру на объекте target
    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - WIDTH // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - HEIGHT // 2)


start_screen()
level = load_level('levelex.txt')
player, granny, _, level_x, level_y = generate_level(level)
LEVEL = 1
camera = Camera((level_x, level_y))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.rect.x -= STEP
            if event.key == pygame.K_RIGHT:
                player.rect.x += STEP
            if event.key == pygame.K_UP:
                player.rect.y -= STEP
            if event.key == pygame.K_DOWN:
                player.rect.y += STEP
    if LEVEL == 1 and pygame.sprite.collide_rect(player, granny):
        clear()
        LEVEL += 1
        player, _, bad_guy, level_x, level_y = generate_level(load_level("levelx2.txt"))
    camera.update(player)
    all_sprites.update()
    screen.fill(pygame.Color("white"))
    map_group.draw(screen)
    granny_group.draw(screen)
    player_group.draw(screen)
    for sprite in all_sprites:
        camera.apply(sprite)

    pygame.display.flip()
    clock.tick(FPS)
terminate()
