#
#
#
#
#
# import pygame,time, sys
# from pygame.locals import*
#
#
# def round_time(time_left) :
#
#     while time_left >= -1 :
#         total_sec = time_left
#         time_left -= 1
#         if time_left > -1:
#             text = font.render(("Time left: " + str(total_sec)), True, color)
#             screen.blit(text, (200, 200))
#             pygame.display.flip()
#             screen.fill((20, 20, 20))
#             time.sleep(1)  # making the time interval of the loop 1sec
#         else:
#             text = font.render("Time Over!!", True, color)
#             screen.blit(text, (200, 200))
#             pygame.display.flip()
#             screen.fill((20, 20, 20))
#
#
#
# pygame.init()
# screen_size = (400,400)
# screen = pygame.display.set_mode(screen_size)
# pygame.display.set_caption("timer")
# time_left = 2000 #duration of the timer in seconds
# crashed  = False
# font = pygame.font.SysFont("Somic Sans MS", 30)
# color = (255, 255, 255)
#
# while not crashed:
#     for event in pygame.event.get():
#         if event.type == QUIT:
#             crashed = True
#     total_sec = time_left
#     time_left -= 1
#     if time_left > -1:
#         text = font.render(("Time left: "+str(total_sec)), True, color)
#         screen.blit(text, (200, 200))
#         pygame.display.flip()
#         screen.fill((20,20,20))
#         time.sleep(1)#making the time interval of the loop 1sec
#     else:
#         text = font.render("Time Over!!", True, color)
#         screen.blit(text, (200, 200))
#         pygame.display.flip()
#         screen.fill((20,20,20))
#
#
#
#
# pygame.quit()
# sys.exit()





# import pygame
# import time
# from threading import Thread
#
#
# time_left=200
# pygame.init()
# run = True
# def loopA() :
#     time_left = 200
#     while run :
#         total_sec = time_left
#         time_left -= 1
#         if time_left > -1:
#             print(time_left)
#             time.sleep(1)#making the time interval of the loop 1sec
#         else:
#             print("время вышло")
#
# def loopB():
#     screen_width = 500
#     screen_height = 500
#     screen = pygame.display.set_mode((screen_width,screen_height))
#     run = True
#     while run :
#
#         screen.fill("Pink")
#
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 run = False
#         pygame.display.update()
#     pygame.quit()
#
# threadA = Thread(target = loopB)
# threadB = Thread(target = loopA)
# threadA.run()
# threadB.run()
# # Do work indepedent of loopA and loopB
# threadA.join()
# threadB.join()


import pygame
import os
import csv
import button
import random
import time
import threading


# Функция для обратного отсчета
def countdown(seconds):
    while seconds > 0:
        print(f"Обратный отсчет: {seconds} секунд")
        time.sleep(1)  # Задержка в 1 секунду
        seconds -= 1

    print("Обратный отсчет завершен!")


# Функция для создания окна Pygame
def run_pygame():
    pygame.init()

    SCREEN_WIDTH = 1280
    SCREEN_HEIGHT = 720

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("ZOVmix")

    tickrate = pygame.time.Clock()
    FPS = 60

    gravity = 0.78
    scroll_tresh = 1000
    rows = 16
    cols = 150
    tile_size = SCREEN_HEIGHT // rows
    tile_types = 21
    screen_scroll = 0
    bg_scroll = 0
    level = 52

    bg_img = pygame.image.load("../картиночки/бг_меню.jpg").convert_alpha()
    start_img = pygame.image.load("../картиночки/старт (1).png").convert_alpha()
    exit_img = pygame.image.load("../картиночки/выход (1).png").convert_alpha()
    level1_img = pygame.image.load("../картиночки/левел1.png").convert_alpha()
    level2_img = pygame.image.load("../картиночки/левел2.png").convert_alpha()
    levelrandom_img = pygame.image.load("../картиночки/рандомлевел.png").convert_alpha()
    pistol_img = pygame.image.load("../картиночки/пистолет.png").convert_alpha()

    img_list = []
    for x in range(tile_types):
        img = pygame.image.load(f'level_editor/img/tile/{x}.png')
        img = pygame.transform.scale(img, (tile_size, tile_size))
        img_list.append(img)

    # Загружаем изображения снарядов для каждого оружия
    bullet_images = {
        'pistol': pygame.image.load("../картиночки/пуля.png").convert_alpha(),
        'rifle': pygame.image.load("../картиночки/пуля_автомат.png").convert_alpha(),
        'shotgun': pygame.image.load("../картиночки/пуля_дробовик.png").convert_alpha()
    }

    moving_left = False
    moving_right = False

    bg = pygame.image.load("../картиночки/бг_карта1.jpg")

    def draw_bg():
        screen.blit(bg, (0, 0))

    class Worm(pygame.sprite.Sprite):
        def __init__(self, skin_type, x, y, scale, speed):
            pygame.sprite.Sprite.__init__(self)
            self.alive = True
            self.skin_type = skin_type
            self.speed = speed
            self.direction = 1
            self.vel_y = 0
            self.jump = False
            self.in_air = True
            self.flip = False
            self.animation_list = []
            self.frame_index = 0
            self.action = 0
            self.update_time = pygame.time.get_ticks()
            self.last_shot_time = 0
            self.cooldown = 80  # время задержки между выстрелами
            self.current_weapon = 'pistol'  # текущее оружие
            animation_types = ['стойка1', "бег1", "прыжок1"]
            picture_types = ['ст1', "бег1", "пр1"]
            picture_types_count = 0
            for animation in animation_types:
                list_list = []
                num_of_frames = len(os.listdir(f"картиночки/персонаж{self.skin_type}/{animation}"))
                for i in range(1, num_of_frames + 1):
                    player_img = pygame.image.load(
                        f"картиночки/персонаж{self.skin_type}/{animation}/{picture_types[picture_types_count]}{i}.png")
                    player_image = pygame.transform.scale(player_img, (
                    int(player_img.get_width() * scale), int(player_img.get_height() * scale)))
                    list_list.append(player_image)
                self.animation_list.append(list_list)
                picture_types_count += 1

            self.player_image = self.animation_list[self.action][self.frame_index]
            self.rect = self.player_image.get_rect()
            self.rect.center = (x, y)
            self.width = self.player_image.get_width()
            self.height = self.player_image.get_height()

        def move(self, moving_left, moving_right):
            screen_scroll = 0
            delta_x = 0
            delta_y = 0

            if moving_left:
                delta_x -= self.speed
                self.flip = True
                self.direction = -1
            if moving_right:
                delta_x += self.speed
                self.flip = False
                self.direction = 1

            if self.jump == True and self.in_air == False:
                self.vel_y = -15
                self.jump = False
                self.in_air = True

            self.vel_y += gravity
            if self.vel_y > 10:
                self.vel_y
            delta_y += self.vel_y

            for tile in world.obstacle_list:
                if tile[1].colliderect(self.rect.x + delta_x, self.rect.y, self.width, self.height):
                    delta_x = 0
                if tile[1].colliderect(self.rect.x, self.rect.y + delta_y, self.width, self.height):
                    if self.vel_y < 0:
                        self.vel_y = 0
                        delta_y = tile[1].bottom - self.rect.top
                    elif self.vel_y >= 0:
                        self.vel_y = 0
                        self.in_air = False
                        delta_y = tile[1].top - self.rect.bottom

            self.rect.x += delta_x
            self.rect.y += delta_y

            if self.skin_type == "1":
                if self.rect.right > SCREEN_WIDTH - scroll_tresh or self.rect.left < scroll_tresh:
                    self.rect.x -= delta_x
                    screen_scroll = -delta_x
            return screen_scroll

        def update_animation(self):
            animation_cooldown = 80
            self.player_image = self.animation_list[self.action][self.frame_index]
            if pygame.time.get_ticks() - self.update_time > animation_cooldown:
                self.update_time = pygame.time.get_ticks()
                self.frame_index += 1
            if self.frame_index >= len(self.animation_list[self.action]):
                self.frame_index = 0

        def update_action(self, new_action):
            if new_action != self.action:
                self.action = new_action
                self.frame_index = 0
                self.update_time = pygame.time.get_ticks()

        def shoot(self):
            current_time = pygame.time.get_ticks()
            if current_time - self.last_shot_time > self.cooldown:
                bullet_img = bullet_images[self.current_weapon]
                bullet = Bullet(self.rect.centerx, self.rect.centery, self.direction, bullet_img)
                bullet_group.add(bullet)
                self.last_shot_time = current_time

        def draw(self):
            screen.blit(pygame.transform.flip(self.player_image, self.flip, False), self.rect)

    class Bullet(pygame.sprite.Sprite):
        def __init__(self, x, y, direction, image):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.transform.scale(image, (30, 15))
            self.rect = self.image.get_rect()
            self.rect.center = (x, y)
            self.direction = direction
            self.speed = 20

        def update(self):
            self.rect.x += (self.direction * self.speed)
            if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
                self.kill()

            # Проверка коллизии с препятствиями
            for tile in world.obstacle_list:
                if tile[1].colliderect(self.rect):
                    self.kill()

    # Создаем кнопки для экранов
    start_button = button.Button(500, 300, start_img, 2)
    exit_button = button.Button(520, 430, exit_img, 1.75)
    pistol_button = button.Button(400, 400, pistol_img, 0.5)
    level1_button = button.Button(270, 400, level1_img, 0.5)
    level2_button = button.Button(470, 400, level2_img, 0.5)
    levelrandom_button = button.Button(670, 400, levelrandom_img, 0.65)

    bullet_group = pygame.sprite.Group()

    run = True
    while run:
        player1 = Worm("1", 300, 500, 0.19, 7)
        level = 52
        run_game = True
        screen.blit(bg_img, (0, 0))
        run_level_menu = True
        if start_button.draw(screen):
            screen.blit(bg_img, (0, 0))
            run_level_menu = True
            while run_level_menu:
                if level1_button.draw(screen):
                    level = 0
                elif level2_button.draw(screen):
                    level = 1
                elif levelrandom_button.draw(screen):
                    level = random.randint(0, 1)

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run_level_menu = False

                if level == 1 or level == 0:
                    class World():
                        def __init__(self):
                            self.obstacle_list = []

                        def process_data(self, data):
                            for y, row in enumerate(data):
                                for x, tile in enumerate(row):
                                    if tile >= 0:
                                        img = img_list[tile]
                                        img_rect = img.get_rect()
                                        img_rect.x = x * tile_size
                                        img_rect.y = y * tile_size
                                        tile_data = (img, img_rect)
                                        if tile >= 0 and tile <= 8 or tile == 12:
                                            self.obstacle_list.append(tile_data)
                                        elif tile >= 13 and tile <= 14 or tile == 11:
                                            decoration = Decoration(img, x * tile_size, y * tile_size)
                                            decoration_group.add(decoration)

                        def draw(self):
                            for tile in self.obstacle_list:
                                tile[1][0] += screen_scroll
                                screen.blit(tile[0], tile[1])

                    class Decoration(pygame.sprite.Sprite):
                        def __init__(self, img, x, y):
                            pygame.sprite.Sprite.__init__(self)
                            self.image = img
                            self.rect = self.image.get_rect()
                            self.rect.midtop = (x + tile_size // 2, y + (tile_size - self.image.get_height()))

                        def update(self):
                            self.rect.x += screen_scroll

                    class Water(pygame.sprite.Sprite):
                        def __init__(self, img, x, y):
                            pygame.sprite.Sprite.__init__(self)
                            self.image = img
                            self.rect = self.image.get_rect()
                            self.rect.midtop = (x + tile_size // 2, y + (tile_size - self.image.get_height()))

                        def update(self):
                            self.rect.x += screen_scroll

                    decoration_group = pygame.sprite.Group()
                    water_group = pygame.sprite.Group()

                    world_data = []
                    for row in range(rows):
                        r = [-1] * cols
                        world_data.append(r)

                    with open(f'level_editor/level{level}_data.csv', newline='') as csvfile:
                        reader = csv.reader(csvfile, delimiter=',')
                        for x, row in enumerate(reader):
                            for y, tile in enumerate(row):
                                world_data[x][y] = int(tile)

                    world = World()
                    world.process_data((world_data))

                    run_level_menu = False
                pygame.display.update()

            while run_game:
                tickrate.tick(FPS)
                draw_bg()
                world.draw()
                player1.update_animation()
                player1.draw()
                bullet_group.update()
                bullet_group.draw(screen)

                decoration_group.draw(screen)
                decoration_group.update()
                water_group.draw(screen)
                water_group.update()

                run_weapon_menu = True

                if player1.alive:
                    if player1.in_air:
                        player1.update_action(2)
                    elif moving_left or moving_right:
                        player1.update_action(1)
                    else:
                        player1.update_action(0)
                    screen_scroll = player1.move(moving_left, moving_right)

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run_game = False
                        run = False
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            run_game = False
                        if event.key == pygame.K_a:
                            moving_left = True
                        if event.key == pygame.K_d:
                            moving_right = True
                        if event.key == pygame.K_w and player1.alive:
                            player1.jump = True
                        if event.key == pygame.K_f and player1.alive:
                            player1.shoot()
                        if event.key == pygame.K_1:
                            player1.current_weapon = 'pistol'
                        if event.key == pygame.K_2:
                            player1.current_weapon = 'rifle'
                        if event.key == pygame.K_3:
                            player1.current_weapon = 'shotgun'
                        if event.key == pygame.K_e:
                            while run_weapon_menu == True:
                                pygame.draw.rect(screen, "Black", (300, 300, 600, 600))
                                if pistol_button.draw(screen):
                                    player1.current_weapon = "pistol"
                                    print("123312321")
                                    run_weapon_menu = False
                                for event in pygame.event.get():
                                    if event.type == pygame.QUIT:
                                        run_weapon_menu = False
                                pygame.display.update()

                    if event.type == pygame.KEYUP:
                        if event.key == pygame.K_a:
                            moving_left = False
                        if event.key == pygame.K_d:
                            moving_right = False
                pygame.display.update()
        if exit_button.draw(screen):
            run = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        pygame.display.update()

    pygame.quit()


# Основная функция для запуска потоков
def main():
    countdown_seconds = 10  # Установите количество секунд для обратного отсчета

    # Создаем и запускаем потоки
    countdown_thread = threading.Thread(target=countdown, args=(countdown_seconds,))
    pygame_thread = threading.Thread(target=run_pygame)

    countdown_thread.start()
    pygame_thread.start()

    # Ждем завершения потока обратного отсчета
    countdown_thread.join()

    # После завершения обратного отсчета, завершаем работу Pygame
    pygame_thread.join()


if __name__ == "__main__":
    main()
