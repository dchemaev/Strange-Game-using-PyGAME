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
LEVEL = 1

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

all_sprites = pygame.sprite.Group()  # Группа всех спрайтов
map_group = pygame.sprite.Group()  # Спрайты карты
player_group = pygame.sprite.Group()  # Спрайты персонажей
granny_group = pygame.sprite.Group()
badguy_group = pygame.sprite.Group()
horizontal_borders = pygame.sprite.Group()
vertical_borders = pygame.sprite.Group()


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


def load_level(filename):
    filename = 'data/' + filename

    with open(filename, 'r') as map_file:
        level_map = [line.strip() for line in map_file]

    max_width = max(map(len, level_map))

    return list(map(lambda x: x.ljust(max_width, '#'), level_map))


def terminate():
    pygame.quit()
    sys.exit()


tile_images = {
    'granny': load_image('granny.png'),
    'empty': load_image('grass.png'),
    'player': load_image('hero.png'),
    'badguy': load_image('badguy.png')
}


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


class Border(pygame.sprite.Sprite):
    # строго вертикальный или строго горизонтальный отрезок
    def __init__(self, x1, y1, x2, y2):
        super().__init__(all_sprites)
        if x1 == x2:  # вертикальная стенка
            self.add(vertical_borders)
            self.image = pygame.Surface([1, y2 - y1])
            self.rect = pygame.Rect(x1, y1, 1, y2 - y1)
        else:  # горизонтальная стенка
            self.add(horizontal_borders)
            self.image = pygame.Surface([x2 - x1, 1])
            self.rect = pygame.Rect(x1, y1, x2 - x1, 1)


class Camera:
    def __init__(self):
        self.dx = 0
        self.dy = 0

    def apply(self, obj):  # Перемещение любого спрайта
        obj.rect.x += self.dx
        obj.rect.y += self.dy
        """""
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
        """""
    def update(self, target):  # Перемещение персонажа
        self.dx = -(target.rect.x + target.rect.w // 2 - WIDTH // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - HEIGHT // 2)


class MainHero(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = tile_images['player']
        self.rect = self.image.get_rect().move(TILE_WIDTH * pos_x + 15,
                                               TILE_HEIGHT * pos_y + 5)


class StartScreen:
    def __init__(self):
        intro_text = ["ИГРА ГОДА!   КОРМИ ГУЛЬ БАБУЛИ", "",
                      "Правила игры:",
                      "Корми голубей семечками",
                      "Подойди ко мне для начала испытания",
                      "",
                      "",
                      "",
                      "",
                      "",
                      "",
                      "",
                      "",
                      "",
                      "",
                      "",
                      "Не попадись гопнику на глаза!"]

        fon = pygame.transform.scale(load_image('grannyFull.png'), (WIDTH, HEIGHT))
        screen.blit(fon, (0, 0))
        font = pygame.font.Font(None, 30)
        text_coord = 50
        for line in intro_text:
            string_rendered = font.render(line, 1, pygame.Color('White'))
            intro_rect = string_rendered.get_rect()
            text_coord += 10
            intro_rect.top = text_coord
            intro_rect.x = 10
            text_coord += intro_rect.height
            screen.blit(string_rendered, intro_rect)

    def run(self):
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                    return  # начинаем игру
            pygame.display.flip()
            clock.tick(FPS)


class StartScreen2:
    def __init__(self):
        intro_text = ["Здравствуй Чучмек!", "Ты захотел поиграть в игру?",
                      "Правила игры:",
                      "Корми голубей семечками",
                      "",
                      "",
                      "",
                      "",
                      "",
                      "",
                      "",
                      "",
                      "",
                      "",
                      "",
                      "Попадешься мне на глаза - получишь в жбан!",
                      "(Чтобы начать испытание, нажмите Enter)"]

        fon = pygame.transform.scale(load_image('badguyFull.png'), (WIDTH, HEIGHT))
        screen.blit(fon, (0, 0))
        font = pygame.font.Font(None, 30)
        text_coord = 50
        for line in intro_text:
            string_rendered = font.render(line, 1, pygame.Color('White'))
            intro_rect = string_rendered.get_rect()
            text_coord += 10
            intro_rect.top = text_coord
            intro_rect.x = 10
            text_coord += intro_rect.height
            screen.blit(string_rendered, intro_rect)

    def run(self):
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        return
            pygame.display.flip()
            clock.tick(FPS)


class Level:
    def __init__(self, level_name):
        all_sprites.empty()
        player_group.empty()
        if LEVEL == 1:
            self.player, self.granny, _, level_x, level_y = generate_level(load_level(level_name))
            self.camera = Camera()
        if LEVEL == 2:
            self.player, _, self.badguy, level_x, level_y = generate_level(load_level(level_name))
            self.camera = Camera()

    def run(self):
        global LEVEL
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.player.rect.x -= STEP
                        """""
                        if not pygame.sprite.spritecollideany(self.player, vertical_borders):
                            print(*vertical_borders)
                            self.player.rect.x -= STEP
                        else:
                            print(2)
                        """""
                    if event.key == pygame.K_RIGHT:
                        self.player.rect.x += STEP
                    if event.key == pygame.K_UP:
                        self.player.rect.y -= STEP
                    if event.key == pygame.K_DOWN:
                        self.player.rect.y += STEP

                elif LEVEL == 1 and pygame.sprite.collide_rect(self.player, self.granny):
                    LEVEL += 1
                    return
            self.camera.update(self.player)
            for sprite in all_sprites:
                self.camera.apply(sprite)

            screen.fill(pygame.Color("Black"))
            all_sprites.draw(screen)
            player_group.draw(screen)

            pygame.display.flip()

            clock.tick(FPS)


def main():
    running = True

    while running:
        StartScreen().run()
        Border(5, 5, WIDTH - 5, 5)
        Border(5, HEIGHT - 5, WIDTH - 5, HEIGHT - 5)
        Border(5, 5, 5, HEIGHT - 5)
        Border(WIDTH - 5, 5, WIDTH - 5, HEIGHT - 5)
        Level("levelex.txt").run()
        if LEVEL == 2:
            StartScreen2().run()
            Level("levelx2.txt").run()

    terminate()


main()
