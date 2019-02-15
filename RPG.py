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

BLACK = [0, 0, 0]
WHITE = [255, 255, 255]

GRAVITY = 0.25
STAR_WIDTH = STAR_HEIGHT = 50

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

all_sprites = pygame.sprite.Group()  # Группа всех спрайтов
map_group = pygame.sprite.Group()  # Спрайты карты
player_group = pygame.sprite.Group()  # Спрайты персонажей
granny_group = pygame.sprite.Group()
badguy_group = pygame.sprite.Group()
horizontal_borders = pygame.sprite.Group()
vertical_borders = pygame.sprite.Group()
pigeon_group = pygame.sprite.Group()


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


def generate_level(level):
    new_player = None
    main_granny = None
    pigeon = None
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
            elif level[y][x] == '*':
                Tile('empty', x, y)
            elif level[y][x] == '3':
                Tile('empty', x, y)
                pigeon = Pigeon(x, y)
            elif level[y][x] == '%':
                Tile('empty', x, y)
                bad_guy = BadGuy(x, y)

    return new_player, main_granny, bad_guy, pigeon, x, y


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
    'badguy': load_image('badguy.png'),
    "pigeon": load_image("pigeon.png")
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


class Pigeon(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(pigeon_group, all_sprites)
        self.image = tile_images["pigeon"]
        self.rect = self.image.get_rect().move(TILE_WIDTH * pos_y,
                                               TILE_HEIGHT * pos_x)


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

        # Loop until the user clicks the close button.
        done = False
        snow_list = []
        while not done:

            for event in pygame.event.get():  # User did something
                if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:  # If user clicked close
                    done = True  # Flag that we are done so we exit this loop
                if event.type == pygame.QUIT:  # If user clicked close
                    done = True  # Flag that we are done so we exit this loop

            # Set the screen background
            fon = pygame.transform.scale(load_image('grannyFull.png'), (WIDTH, HEIGHT))
            screen.blit(fon, (0, 0))
            font = pygame.font.Font(None, 30)
            text_coord = 50

            for i in range(1):
                x = random.randrange(0, 600)
                y = random.randrange(0, 900)
                snow_list.append([x, y])
            # Loop 50 times and add a snow flake in a random x,y position

            for line in intro_text:
                string_rendered = font.render(line, 1, pygame.Color('White'))
                intro_rect = string_rendered.get_rect()
                text_coord += 10
                intro_rect.top = text_coord
                intro_rect.x = 10
                text_coord += intro_rect.height
                screen.blit(string_rendered, intro_rect)

            # Process each snow flake in the list
            for i in range(len(snow_list)):

                # Draw the snow flake
                pygame.draw.circle(screen, WHITE, snow_list[i], 2)

                # Move the snow flake down one pixel
                snow_list[i][1] += 1

                # If the snow flake has moved off the bottom of the screen
                if snow_list[i][1] > 600:
                    # Reset it just above the top
                    y = random.randrange(-50, -10)
                    snow_list[i][1] = y
                    # Give it a new x position
                    x = random.randrange(0, 700)
                    snow_list[i][0] = x

            # Go ahead and update the screen with what we've drawn.
            pygame.display.flip()
            clock.tick(FPS)

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

        done = False
        snow_list = []
        while not done:

            for event in pygame.event.get():  # User did something
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:  # If user clicked close
                        done = True  # Flag that we are done so we exit this loop
                if event.type == pygame.QUIT:  # If user clicked close
                    done = True  # Flag that we are done so we exit this loop

            # Set the screen background
            fon = pygame.transform.scale(load_image('badguyFull.png'), (WIDTH, HEIGHT))
            screen.blit(fon, (0, 0))
            font = pygame.font.Font(None, 30)
            text_coord = 50

            for i in range(1):
                x = random.randrange(0, 600)
                y = random.randrange(0, 900)
                snow_list.append([x, y])
            # Loop 50 times and add a snow flake in a random x,y position

            for line in intro_text:
                string_rendered = font.render(line, 1, pygame.Color('White'))
                intro_rect = string_rendered.get_rect()
                text_coord += 10
                intro_rect.top = text_coord
                intro_rect.x = 10
                text_coord += intro_rect.height
                screen.blit(string_rendered, intro_rect)

            # Process each snow flake in the list
            for i in range(len(snow_list)):

                # Draw the snow flake
                pygame.draw.circle(screen, WHITE, snow_list[i], 2)

                # Move the snow flake down one pixel
                snow_list[i][1] += 1

                # If the snow flake has moved off the bottom of the screen
                if snow_list[i][1] > 600:
                    # Reset it just above the top
                    y = random.randrange(-50, -10)
                    snow_list[i][1] = y
                    # Give it a new x position
                    x = random.randrange(0, 700)
                    snow_list[i][0] = x

            # Go ahead and update the screen with what we've drawn.
            pygame.display.flip()
            clock.tick(FPS)

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


class Level:
    def __init__(self, level_name):
        all_sprites.empty()
        player_group.empty()
        if LEVEL == 1:
            self.player, self.granny, _, _, level_x, level_y = generate_level(load_level(level_name))
        if LEVEL == 2:
            self.player, _, self.badguy, self.pigeon, level_x, level_y = generate_level(load_level(level_name))

    def run(self):
        global LEVEL
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT and self.player.rect.x > 0:
                        self.player.rect.x -= STEP
                    if event.key == pygame.K_RIGHT and self.player.rect.x < 550:
                        self.player.rect.x += STEP
                    if event.key == pygame.K_UP and self.player.rect.y > 5:
                        self.player.rect.y -= STEP
                    if event.key == pygame.K_DOWN and self.player.rect.y < 545:
                        self.player.rect.y += STEP
                    if event.key == pygame.K_SPACE and LEVEL == 2:
                        pos = [self.player.rect.x, self.player.rect.y]
                        create_particles(pos)

                elif LEVEL == 1 and pygame.sprite.collide_rect(self.player, self.granny):
                    LEVEL += 1
                    StartScreen2().run()
                    Level("levelx2.txt").run()
                    """""
                    if LEVEL == 2 and pygame.sprite.collide_rect(self.player, self.pigeon):
                        LEVEL += 1
                        return
                    """""
            screen.fill(pygame.Color("Black"))
            all_sprites.draw(screen)
            player_group.draw(screen)

            pygame.display.flip()

            clock.tick(FPS)


class Particle(pygame.sprite.Sprite):
    star = [load_image("star.png")]
    for scale in (5, 10, 20):
        star.append(pygame.transform.scale(star[0], (scale, scale)))  # Изменяем размер с учетом перовй частицы

    def __init__(self, pos, dx, dy):
        super().__init__(all_sprites)
        self.image = random.choice(self.star)
        self.rect = self.image.get_rect()

        self.velocity = [dx, dy]
        self.rect.x, self.rect.y = pos

        self.gravity = GRAVITY

    def update(self, *args):
        self.velocity[1] += self.gravity

        self.rect.x += 5
        self.rect.y += 10

        if not self.rect.colliderect(screen):  # Удаление частиц, вышедших за предели окна
            self.kill()
        if not self.rect.colliderect(Pigeon):  # Удаление частиц, вышедших за предели окна
            self.kill()


def create_particles(position):
    count = 20
    speed = range(-5, 6)
    for _ in range(count):
        Particle(position, random.choice(speed), random.choice(speed))


def main():
    global LEVEL, player, pigeon
    running = True

    while running:
        StartScreen().run()
        Border(5, 5, WIDTH - 5, 5)
        Border(5, HEIGHT - 5, WIDTH - 5, HEIGHT - 5)
        Border(5, 5, 5, HEIGHT - 5)
        Border(WIDTH - 5, 5, WIDTH - 5, HEIGHT - 5)
        Level("levelex.txt").run()
    terminate()


main()
