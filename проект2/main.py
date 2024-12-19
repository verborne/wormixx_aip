import time
import pygame
import os
import csv
import random
import math
import socket

# Инициализация Pygame
pygame.init()

# Константы размеров экрана
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

# Создание окна игры
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("ZOVmix")

# Частота обновления кадров
tickrate = pygame.time.Clock()
FPS = 60

# Физические константы
gravity = 0.78
bow_gravity = 2

# Параметры прокрутки
scroll_tresh = 1000

# Параметры уровня
rows = 16
cols = 150
tile_size = SCREEN_HEIGHT // rows
tile_types = 21
screen_scroll = 0
bg_scroll = 0
level = 52

# Время на ход (не используется в текущей версии)
time_to_move = 100
remaining_time = time_to_move
time_to_game = 600

# Загрузка изображений
bg_img = pygame.image.load("картиночки/бг_меню.jpg").convert_alpha()
start_img = pygame.image.load("картиночки/старт (1).png").convert_alpha()
exit_img = pygame.image.load("картиночки/выход (1).png").convert_alpha()
level1_img = pygame.image.load("картиночки/левел1.png").convert_alpha()
level2_img = pygame.image.load("картиночки/левел2.png").convert_alpha()
rifle_bullet_img = pygame.image.load("картиночки/пуля.png").convert_alpha()
rifle_bullet_img = pygame.transform.scale(rifle_bullet_img, (rifle_bullet_img.get_height() * 0.5, rifle_bullet_img.get_width() * 0.3))
levelrandom_img = pygame.image.load("картиночки/рандомлевел.png").convert_alpha()

# Оружие
pistol_img = pygame.image.load("картиночки/пистолет1.png").convert_alpha()
pistol_img = pygame.transform.scale(pistol_img, (pistol_img.get_height() * 0.2, pistol_img.get_width() * 0.115))
shotgun_img = pygame.image.load("картиночки/дробовик2.png").convert_alpha()
shotgun_img = pygame.transform.scale(shotgun_img, (shotgun_img.get_height() * 0.91, shotgun_img.get_width() * 0.3))
rifle_img = pygame.image.load("картиночки/автомат.png").convert_alpha()
rifle_img = pygame.transform.scale(rifle_img, (rifle_img.get_height() * 0.85, rifle_img.get_width() * 0.25))
minigun_img = pygame.image.load("картиночки/minigun.png").convert_alpha()
bow_img = pygame.image.load("картиночки/лук_нормальный-no-bg-preview (carve.photos).png").convert_alpha()
sniper_rifle_img = pygame.image.load("картиночки/снайперка-no-bg-preview (carve.photos).png").convert_alpha()

# Другие предметы
time_bg_img = pygame.image.load("картиночки/время_бг.png").convert_alpha()
time_bg_img = pygame.transform.scale(time_bg_img,
                                     (time_bg_img.get_height() * 1, time_bg_img.get_width() * 0.2)).convert_alpha()
pistol_bullet_img = pygame.image.load("картиночки/пуля_дробовик.png").convert_alpha()
pistol_bullet_img = pygame.transform.scale(pistol_bullet_img, (rifle_img.get_height() * 0.3, rifle_img.get_width() * 0.1))
guns_menu_img = pygame.image.load("картиночки/меню_оружия.png").convert_alpha()
guns_menu_img = pygame.transform.scale(guns_menu_img, (guns_menu_img.get_height() * 1, guns_menu_img.get_width() * 0.4))
shotgun_bullet_img = pygame.image.load("картиночки/пуля_автомат.png").convert_alpha()
shotgun_bullet_img = pygame.transform.scale(shotgun_bullet_img, (shotgun_bullet_img.get_height() * 0.2, shotgun_bullet_img.get_width() * 0.1))
minigun_bullet_img = pygame.image.load("картиночки/пуля_миниган.png").convert_alpha()
minigun_bullet_img = pygame.transform.scale(minigun_bullet_img, (minigun_bullet_img.get_height() * 0.2, minigun_bullet_img.get_width() * 0.1))
arrow_img = pygame.image.load("картиночки/стрела.png").convert_alpha()
arrow_img = pygame.transform.scale(arrow_img, (arrow_img.get_height() * 0.1, arrow_img.get_width() * 0.01))
sniper_rifle_bullet_img = pygame.image.load("картиночки/m_пуля_снайперка.png").convert_alpha()
sniper_rifle_bullet_img = pygame.transform.scale(sniper_rifle_bullet_img, (sniper_rifle_bullet_img.get_height() * 0.2, sniper_rifle_bullet_img.get_width() * 0.1))
medkit_img = pygame.image.load("картиночки/аптечка.png").convert_alpha()
medkit_img = pygame.transform.scale(medkit_img, (medkit_img.get_height() * 0.2, medkit_img.get_width() * 0.1))
grenade_img = pygame.image.load("картиночки/граната-no-bg-preview (carve.photos).png").convert_alpha()
grenade_img = pygame.transform.scale(grenade_img, (grenade_img.get_height() * 0.2, grenade_img.get_width() * 0.1))
beer_img = pygame.image.load("картиночки/пиво-no-bg-preview (carve.photos).png").convert_alpha()
beer_img = pygame.transform.scale(beer_img, (beer_img.get_height() * 0.2, beer_img.get_width() * 0.1))
font_for_time = pygame.font.Font("шрифты/Zelda DXTT (BRK) RUS by SubRaiN Regular.ttf", 82)

# Загрузка изображений тайлов
img_list = []
for x in range(tile_types):
    img = pygame.image.load(f'level_editor/img/tile/{x}.png')
    img = pygame.transform.scale(img, (tile_size, tile_size))
    img_list.append(img)

# Флаги движения
moving_left = False
moving_right = False

# Фон
bg = pygame.image.load("картиночки/бг_карта1.jpg")


# Функция для рисования фона
def draw_bg():
    ''' Отрисовывает фоновое изображение на экране.

        :returns: None
        :rtype: NoneType
        :raises AttributeError: если bg или screen не инициализированы должным образом.
        '''
    screen.blit(bg, (0, 0))

# Функция для рисования полоски здоровья
def draw_health_bar(hp, x, y, width, height):
    '''Отрисовывает индикатор здоровья на экране.

    :param hp: текущее количество здоровья (в процентах от 0 до 100)
    :type hp: float
    :param x: координата x верхнего левого угла индикатора
    :type x: int
    :param y: координата y верхнего левого угла индикатора
    :type y: int
    :param width: ширина индикатора здоровья
    :type width: int
    :param height: высота индикатора здоровья
    :type height: int
    :returns: None
    :rtype: NoneType
    :raises ValueError: если hp не находится в пределах от 0 до 100.
    '''
    ratio = hp / 100
    pygame.draw.rect(screen, (255, 0, 0), (x, y, width, height))  # Красная часть
    pygame.draw.rect(screen, (0, 255, 0), (x, y, width * ratio, height))  # Зелёная часть

#Данный класс заимствован с Youtube канала Coding with Russ
class Button():
    """
    Класс для создания интерактивной кнопки в игре.

    Атрибуты:
        x (int): Положение кнопки по оси X.
        y (int): Положение кнопки по оси Y.
        image (Surface): Изображение кнопки, которое будет отображаться на экране.
        scale (float): Масштабирование изображения кнопки.
        clicked (bool): Состояние кнопки (нажата/не нажата).

    Методы:
        __init__(self, x, y, image, scale):
            Инициализирует объект кнопки с заданным положением, изображением и масштабом.

        draw(self, surface):
            Отрисовывает кнопку на переданной поверхности и обрабатывает нажатия.
            Возвращает True, если кнопка нажата, иначе False.
    """

    def __init__(self, x, y, image, scale):
        """
        Инициализирует объект кнопки.

        Параметры:
            x (int): Положение кнопки по оси X.
            y (int): Положение кнопки по оси Y.
            image (Surface): Изображение кнопки.
            scale (float): Масштаб для изображения кнопки.
        """
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False

    def draw(self, surface):
        """
        Отрисовывает кнопку на переданной поверхности и проверяет, была ли нажата кнопка.

        Параметры:
            surface (Surface): Поверхность, на которой будет отрисована кнопка.

        Возвращает:
            bool: True, если кнопка была нажата; иначе False.
        """
        action = False

        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True

            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False

        surface.blit(self.image, (self.rect.x, self.rect.y))

        return action
#окончание заимствованной части

# Класс игрока
class Worm(pygame.sprite.Sprite):
    '''Класс, представляющий игрока в игре.

    :param skin_type: Тип скина игрока
    :type skin_type: str
    :param x: Начальная координата x игрока
    :type x: int
    :param y: Начальная координата y игрока
    :type y: int
    :param scale: Масштабирование изображения игрока
    :type scale: float
    :param speed: Скорость движения игрока
    :type speed: float
    :param hp: Количество здоровья игрока
    :type hp: int
    '''

    def __init__(self, skin_type, x, y, scale, speed, hp):
        '''Инициализирует экземпляр класса Worm.

        :param self: Экземпляр класса, который содержит атрибуты и методы игрока.
        :type self: object
        :param skin_type: Тип скина игрока.
        :param x: Начальная координата x игрока.
        :type x: int
        :param y: Начальная координата y игрока.
        :type y: int
        :param scale: Масштабирование изображения игрока.
        :type scale: float
        :param speed: Скорость движения игрока.
        :type speed: float
        :param hp: Количество здоровья игрока.
        :type hp: int
        '''
        pygame.sprite.Sprite.__init__(self)

        # Инициализация атрибутов стрельбы
        self.arrows = []  # Список стрел
        self.sniper_rifle_bullets = []  # Список пуль для снайперской винтовки
        self.shotgun_bullets = []  # Список пуль для дробовика
        self.pistol_bullets = []  # Список пуль для пистолета
        self.minigun_bullets = []  # Список пуль для минигана

        self.minigun_last_bullet_time = 0  # Время последнего выстрела минигана
        self.minigun_bullet_delay = 30  # Задержка между выстрелами минигана
        self.minigun_bullets_to_shoot = 15  # Количество пуль для выстрела миниганом
        self.minigun_shooting = False  # Флаг, указывающий на стрельбу из минигана

        self.rifle_bullets = []  # Список пуль для винтовки
        self.rifle_last_bullet_time = 0  # Время последнего выстрела винтовки
        self.rifle_bullet_delay = 200  # Задержка между выстрелами винтовки
        self.rifle_bullets_to_shoot = 3  # Количество пуль для выстрела из винтовки
        self.rifle_shooting = False  # Флаг, указывающий на стрельбу из винтовки

        # Инициализация здоровья
        self.hp = hp  # Установка начального здоровья
        self.alive = True if hp > 0 else False  # Проверка на живой статус

        # Внешний вид и характеристики
        self.skin_type = skin_type  # Установка типа скина
        self.speed = speed  # Установка скорости

        # Направление движения
        self.direction = 1  # Установить начальное направление движения

        # Вертикальная скорость
        self.vel_y = 0  # Инициализация вертикальной скорости
        self.jump = False  # Флаг, указывающий на прыжок
        self.in_air = True  # Флаг, указывающий на то, что игрок в воздухе

        # Флаг отражения по горизонтали
        self.flip = False  # Флаг, который определяет, нужно ли отразить изображение по горизонтали

        # Анимация
        self.animation_list = []  # Список анимаций
        self.frame_index = 0  # Индекс текущего кадра анимации
        self.action = 0  # Текущая анимация
        self.update_time = pygame.time.get_ticks()  # Время последнего обновления анимации

        # Перезарядка оружия
        self.last_shot_time = 0  # Время последнего выстрела
        self.cooldown = 80  # Время между выстрелами

        # Типы анимации
        animation_types = ['стойка1', "бег1", "прыжок1"]  # Названия анимаций
        picture_types = ['ст1', "бег1", "пр1"]  # Типы изображений персонажа
        picture_types_count = 0

        # Загрузка анимации
        for animation in animation_types:
            list_list = []
            num_of_frames = len(
                os.listdir(f"картиночки/персонаж{self.skin_type}/{animation}"))  # Получение количества кадров анимации
            for i in range(1, num_of_frames + 1):
                player_img = pygame.image.load(
                    f"картиночки/персонаж{self.skin_type}/{animation}/{picture_types[picture_types_count]}{i}.png")
                player_image = pygame.transform.scale(player_img, (
                    int(player_img.get_width() * scale),
                    int(player_img.get_height() * scale)))  # Масштабирование изображения
                list_list.append(player_image)
            self.animation_list.append(list_list)
            picture_types_count += 1

        # Установка начальных значений
        self.player_image = self.animation_list[self.action][self.frame_index]  # Установить текущее изображение
        self.rect = self.player_image.get_rect()  # Получить прямоугольник для изображения
        self.rect.center = (x, y)  # Установить позицию игрока
        self.width = self.player_image.get_width()  # Ширина изображения
        self.height = self.player_image.get_height()  # Высота изображения

    # Обработка движения
    def move(self, moving_left, moving_right):
        '''Перемещает игрока в зависимости от нажатых клавиш.
            Обрабатывает движение влево и вправо, а также прыжки. Проверяет столкновения с препятствиями.

            :param self: Экземпляр класса
            :type self: object
            :param moving_left: Флаг, указывающий на движение влево.
            :type moving_left: bool
            :param moving_right: Флаг, указывающий на движение вправо.
            :type moving_right: bool
            :returns: Значение смещения экрана при движении игрока.
            :rtype: int
            '''
        if not self.alive:  # Если игрок мертв, он не может двигаться
            return 0
        screen_scroll = 0
        delta_x = 0
        delta_y = 0

        if pygame.sprite.spritecollide(self, water_group, False):
            self.hp = 0
            self.alive = False

        if moving_left:
            delta_x -= self.speed
            self.flip = True
            self.direction = -1
        if moving_right:
            delta_x += self.speed
            self.flip = False
            self.direction = 1

        if self.jump and not self.in_air:
            self.vel_y = -15
            self.jump = False
            self.in_air = True

        self.vel_y += gravity
        if self.vel_y > 10:
            self.vel_y = 10
        delta_y += self.vel_y

        # Проверка столкновений с тайлами
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

        # Прокрутка экрана, если игрок достигает края
        if self.skin_type == "1":
            if self.rect.right > SCREEN_WIDTH - scroll_tresh or self.rect.left < scroll_tresh:
                self.rect.x -= delta_x
                screen_scroll = -delta_x
        return screen_scroll

    # Обновление анимации
    def update_animation(self):
        '''Обновляет текущий кадр анимации для персонажа игрока.

            :param self: Экземпляр класса
            :type self: object
            :returns: None
            :rtype: None
            :raises AttributeError: Если у объекта отсутствуют необходимые атрибуты
            :raises IndexError: если self.frame_index превышает длину текущего списка анимации.
            '''
        animation_cooldown = 80
        self.player_image = self.animation_list[self.action][self.frame_index]  # Установка текущего изображения
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        if self.frame_index >= len(self.animation_list[self.action]):
            self.frame_index = 0

    # Обновление действия (анимации)
    def update_action(self, new_action):
        '''Обновляет текущее действие игрока.

            :param self: Экземпляр класса
            :type self: object
            :param new_action: Новое действие для персонажа
            :type new_action: int
            :returns: None
            :rtype: None
            :raises AttributeError: Если у объекта отсутствуют необходимые атрибуты
            :raises TypeError: если 'new_action' не является целым числом (int).
            '''
        if new_action != self.action:
            self.action = new_action
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    # Проверка жив ли игрок
    def check_alive(self):
        """Проверяет, жив ли игрок на основе его очков здоровья.

            :param self: Экземпляр класса
            :type self: object
            :returns: None
            :rtype: None
            :raises ValueError: Если значение hp не является числом или < -1.
            """
        if self.hp <= 0:
            self.alive = False

    # Функции стрельбы из разного оружия
    def shoot_rifle(self):
        """Этот метод позволяет игроку стрелять пулями из винтовки.
            Он проверяет, жив ли игрок, находится ли винтовка в режиме стрельбы,
            есть ли оставшиеся патроны для стрельбы и прошло ли достаточно времени
            с момента последнего выстрела.

            :param self: Экземпляр класса
            :type self: object
            :returns: None
            :rtype: None
            :raises AttributeError: Если у объекта отсутствуют необходимые атрибуты.
            :raises TypeError: Если любые из атрибутов, используемых в расчетах, не имеют ожидаемых типов.
            """
        if not self.alive:  # Если игрок не жив, выход из метода
            return
        current_time = pygame.time.get_ticks()
        if self.rifle_shooting and self.rifle_bullets_to_shoot > 0 and current_time - self.rifle_last_bullet_time > self.rifle_bullet_delay:
            angle = random.uniform(-10, 10)  # Случайный угол
            bullet = Bullet_for_rifle(self.rect.x, self.rect.y, angle, self.direction)  # Создание пули
            self.rifle_bullets.append(bullet)  # Добавление пули в список
            self.rifle_last_bullet_time = current_time  # Обновление времени последнего выстрела
            self.rifle_bullets_to_shoot -= 1  # Уменьшение количества оставшихся пуль

    def update_rifle(self, target):
        """Обновляет состояние пуль в винтовке и проверяет попадание в цель, при попадании здоровье игрока уменьшается.

            :param self: Экземпляр класса
            :type self: object
            :param target: Цель(игрок), которую необходимо проверить на попадание.
            :type target: object
            :returns: None
            :rtype: None
            :raises AttributeError: Если объект target отсутствует атрибут rect или метод check_alive.
            """
        for bullet in self.rifle_bullets:
            if not bullet.move():  # Если пуля вышла за пределы, удалить ее
                self.rifle_bullets.remove(bullet)
            elif bullet.rect.colliderect(target.rect):  # Проверка на столкновение
                self.rifle_bullets.remove(bullet)  # Удаление пули
                target.hp -= 10  # Уменьшение здоровья цели
                target.check_alive()  # Проверка, жива ли цель

    def draw_rifle(self, surface):
        """Отображает патроны винтовки на заданной поверхности.

            :param self: Экземпляр класса
            :type self: object
            :param surface: Поверхность, на которой будут отображаться патроны.
            :type surface: pygame.Surface
            :returns: None
            :rtype: None
            :raises TypeError: Если surface не является экземпляром pygame.Surface.
            """
        for bullet in self.rifle_bullets:
            bullet.draw(surface)  # Рисование пули на поверхности

    def shoot_shotgun(self):
        """Метод для стрельбы из дробовика. Метод проверяет, жив ли объект (игрок). Если объект мертв, метод ничего не делает.
            В противном случае позволяет стрелять из дробовика, создавая 9 пуль с случайными углами.

            :param self: Экземпляр класса
            :type self: object
            :returns: None
            :rtype: None
            :raises AttributeError: Если объект не имеет атрибута rect или shotgun_bullets.
            """
        if not self.alive:  # Если игрок не жив, выход из метода
            return
        for _ in range(9):  # Создание 9 пуль
            angle = random.uniform(-30, 30)  # Случайный угол
            bullet = Bullet_for_shotgun(self.rect.x, self.rect.y, angle, self.direction)  # Создание пули
            self.shotgun_bullets.append(bullet)  # Добавление пули в список

    def update_shotgun(self, target):
        """Метод проходит по всем пулям, выпущенным из дробовика, проверяет столкновения с целью.

            :param self: Экземпляр класса
            :type self: object
            :param target: Цель, с которой проверяются столкновения.
            :type target: object
            :returns: None
            :rtype: None
            :raises AttributeError: Если объект target не имеет атрибутов rect, check_alive или hp.
            :raises TypeError: Если target не является объектом, который ожидается в методе.
            """
        for bullet in self.shotgun_bullets:
            if not bullet.move():  # Если пуля вышла за пределы, удалить ее
                self.shotgun_bullets.remove(bullet)
            elif bullet.rect.colliderect(target.rect):  # Проверка на столкновение
                self.shotgun_bullets.remove(bullet)  # Удаление пули
                target.hp -= 3  # Уменьшение здоровья цели
                target.check_alive()  # Проверка, жива ли цель

    def draw_shotgun(self, surface):
        """Рисует все пули дробовика на заданной поверхности.

            :param self: Экземпляр класса
            :type self: object
            :param surface: Поверхность, на которой будут рисоваться пули.
            :type surface: object
            :returns: None
            :rtype: None
            :raises AttributeError: Если объект surface не имеет метода blit, который необходим для рисования пуль.
            """
        for bullet in self.shotgun_bullets:
            bullet.draw(surface)  # Рисование пули на поверхности

    def shoot_minigun(self):
        """Метод для стрельбы из минигана. Он проверяет, жив ли игрок и если он жив,
        производит выстрел при выполнении условий.

        :param self: Экземпляр класса
        :type self: object
        :returns: None
        :rtype: None
        """
        if not self.alive:
            return
        current_time = pygame.time.get_ticks()
        if self.minigun_shooting and self.minigun_bullets_to_shoot > 0 and current_time - self.minigun_last_bullet_time > self.minigun_bullet_delay:
            angle = random.uniform(-10, 10)
            bullet = Bullet_for_minigun(self.rect.x, self.rect.y, angle, self.direction)
            self.minigun_bullets.append(bullet)
            self.minigun_last_bullet_time = current_time
            self.minigun_bullets_to_shoot -= 1

    def update_minigun(self, target):
        """Обновляет состояние пуль в минигане и проверяет попадания в цель.

        :param self: Экземпляр класса
        :type self: object
        :param target: Цель (игрок), которую необходимо проверить на попадание.
        :type target: object
        :returns: None
        :rtype: None
        """
        for bullet in self.minigun_bullets:
            if not bullet.move():
                self.minigun_bullets.remove(bullet)
            elif bullet.rect.colliderect(target.rect):
                self.minigun_bullets.remove(bullet)
                target.hp -= 10
                target.check_alive()

    def draw_minigun(self, surface):
        """Рисует все пули минигана на заданной поверхности.

        :param self: Экземпляр класса
        :type self: object
        :param surface: Поверхность, на которой будут рисоваться пули.
        :type surface: object
        :returns: None
        :rtype: None
        """
        for bullet in self.minigun_bullets:
            bullet.draw(surface)

    def shoot_pistol(self):
        """Метод для стрельбы из пистолета. Он проверяет, жив ли игрок.
        Если он жив, создается пуля с выбранным углом.

        :param self: Экземпляр класса
        :type self: object
        :returns: None
        :rtype: None
        """
        if not self.alive:
            return
        angle = random.uniform(-30, 30)
        bullet = Bullet_for_pistol(self.rect.x, self.rect.y, angle, self.direction)
        self.pistol_bullets.append(bullet)

    def update_pistol(self, target):
        """Обновляет состояние пуль из пистолета и проверяет попадания в цель.

        :param self: Экземпляр класса
        :type self: object
        :param target: Цель (игрок), которую необходимо проверить на попадание.
        :type target: object
        :returns: None
        :rtype: None
        """
        for bullet in self.pistol_bullets:
            if not bullet.move():
                self.pistol_bullets.remove(bullet)
            elif bullet.rect.colliderect(target.rect):
                self.pistol_bullets.remove(bullet)
                target.hp -= 3
                target.check_alive()

    def draw_pistol(self, surface):
        """Рисует все пули пистолета на заданной поверхности.

        :param self: Экземпляр класса
        :type self: object
        :param surface: Поверхность, на которой будут рисоваться пули.
        :type surface: object
        :returns: None
        :rtype: None
        """
        for bullet in self.pistol_bullets:
            bullet.draw(surface)

    def shoot_bow(self):
        """Метод для стрельбы из лука. Он проверяет, жив ли игрок,
        затем создает стрелу с углом, направленным по местоположению мыши.

        :param self: Экземпляр класса
        :type self: object
        :returns: None
        :rtype: None
        """
        if not self.alive:
            return
        mouse_x, mouse_y = pygame.mouse.get_pos()  # Получение позиции курсора мыши
        arrow = Arrow(self.rect.x, self.rect.y - 15, mouse_x, mouse_y, self.direction)  # Создание стрелы
        self.arrows.append(arrow)  # Добавление стрелы в список

    def update_bow(self, target):
        """Обновляет состояние стрел и проверяет попадание в цель.

        :param self: Экземпляр класса
        :type self: object
        :param target: Цель (игрок), которую необходимо проверить на попадание.
        :type target: object
        :returns: None
        :rtype: None
        """
        for arrow in self.arrows:
            if not arrow.move():
                self.arrows.remove(arrow)
            elif arrow.rect.colliderect(target.rect):
                self.arrows.remove(arrow)
                target.hp -= 15
                target.check_alive()

    def draw_bow(self, surface):
        """Рисует все стрелы из лука на заданной поверхности.

        :param self: Экземпляр класса
        :type self: object
        :param surface: Поверхность, на которой будут рисоваться стрелы.
        :type surface: object
        :returns: None
        :rtype: None
        """
        for arrow in self.arrows:
            arrow.draw(surface)  # Рисование стрелы на поверхности

    def shoot_sniper_rifle(self):
        """Метод для стрельбы из снайперской винтовки.
        Если игрок жив, создается снайперская пуля, направленная по мыши.

        :param self: Экземпляр класса
        :type self: object
        :returns: None
        :rtype: None
        """
        if not self.alive:
            return
        mouse_x, mouse_y = pygame.mouse.get_pos()  # Получение позиции курсора мыши
        bullet = Bullet_for_sniper_rifle(self.rect.x, self.rect.y + 10, mouse_x, mouse_y,
                                        self.direction)  # Создание пули
        self.sniper_rifle_bullets.append(bullet)  # Добавление пули в список

    def update_sniper_rifle(self, target):
        """Обновляет состояние пуль из снайперской винтовки и проверяет попадания в цель.

        :param self: Экземпляр класса
        :type self: object
        :param target: Цель (игрок), которую необходимо проверить на попадание.
        :type target: object
        :returns: None
        :rtype: None
        """
        for bullet in self.sniper_rifle_bullets:
            if not bullet.move():
                self.sniper_rifle_bullets.remove(bullet)
            elif bullet.rect.colliderect(target.rect):
                self.sniper_rifle_bullets.remove(bullet)
                target.hp -= 15
                target.check_alive()

    def draw_sniper_rifle(self, surface):
        """Рисует все пули из снайперской винтовки на заданной поверхности.

        :param self: Экземпляр класса
        :type self: object
        :param surface: Поверхность, на которой будут рисоваться пули.
        :type surface: object
        :returns: None
        :rtype: None
        """
        for bullet in self.sniper_rifle_bullets:
            bullet.draw(surface)

    def draw(self):
        """Рисует изображение игрока на экране с учетом возможного переворота.

            :param self: Экземпляр класса
            :type self: object
            :returns: None
            :rtype: None
            :raises AttributeError: Если self.player_image или self.rect не инициализированы должным образом.
            :raises TypeError: Если screen не является объектом, поддерживающим метод blit.
            """
        screen.blit(pygame.transform.flip(self.player_image, self.flip, False),
                    self.rect)  # Рисование изображения игрока

# Класс пули для винтовки
class Bullet_for_rifle():
    """Класс, представляющий пулю для винтовки.
       Этот класс отвечает за создание, движение и отображение пули на экране.
       """
    def __init__(self, x, y, angle, direction):
        """Инициализирует пулю.

                :param self: Экземпляр класса
                :type self: object
                :param x: Начальная координата x пули.
                :type x: float
                :param y: Начальная координата y пули.
                :type y: float
                :param angle: Угол, под которым пуля будет двигаться.
                :type angle: float
                :param direction: Направление движения (1 - вправо, -1 - влево).
                :type direction: int
                :raises ValueError: Если direction не равен 1 или -1.
                """
        self.x = x
        self.y = y

        self.speed = 15
        self.angle = angle
        self.direction = direction
        self.direction_for_blit = False
        self.rect = rifle_bullet_img.get_rect(center=(x, y))

    def move(self):
        """Двигает пулю по заданному направлению.
        Метод обновляет координаты пули в зависимости от направления и угла.
        Проверяет столкновение с препятствиями и границами экрана.

        :param self: Экземпляр класса
        :type self: object
        :returns: True, если пуля продолжает движение; False, если пуля столкнулась с препятствием или вышла за границы экрана.
        :rtype: bool
        :raises ValueError: если угол не является числом
        :raises AttributeError: Если атрибуты класса не инициализированы.
        """
        if self.direction == 1:  # Если движется вправо
            self.x += self.speed
            self.y += self.speed * math.sin(math.radians(self.angle))
        else:  # Если движется влево
            self.x -= self.speed
            self.y += self.speed * math.sin(math.radians(self.angle))

        self.rect.x = self.x
        self.rect.y = self.y

        for tile in world.obstacle_list:
            if tile[1].colliderect(self.rect):
                return False

        if self.x < 0 or self.x > SCREEN_WIDTH or self.y < 0 or self.y > SCREEN_HEIGHT:
            return False

        return True

    def draw(self, surface):
        """Отображает пулю на заданной поверхности.

                :param self: Экземпляр класса
                :type self: object
                :param surface: Поверхность, на которой будут рисоваться пули
                :type surface: object
                :returns: None
                :rtype: None
                :raises AttributeError: Если surface не является объектом pygame.Surface.
                """
        if self.direction == 1:
            self.direction_for_blit = False
        else:
            self.direction_for_blit = True

        screen.blit(pygame.transform.flip(rifle_bullet_img, self.direction_for_blit, False), (int(self.x), int(self.y)))


# Класс пули для минигана
class Bullet_for_minigun():
    """
    Класс для создания снарядов минигена.

    Атрибуты:
        x (float): Координата x снаряда.
        y (float): Координата y снаряда.
        speed (float): Скорость движения снаряда.
        angle (float): Угол, под которым снаряд уходит.
        direction (int): Направление движения снаряда (1 - вправо, -1 - влево).
        direction_for_blit (bool): Флаг, указывающий, нужно ли переворачивать изображение снаряда.
        rect (pygame.Rect): Прямоугольник, описывающий размеры и положение снаряда.

    Методы:
        move(): Обновляет положение снаряда и проверяет столкновения.
        draw(surface): Отображает снаряд на экране.
    """

    def __init__(self, x, y, angle, direction):
        """
        Инициализация снаряда.

        Параметры:
            x (float): Начальная координата x снаряда.
            y (float): Начальная координата y снаряда.
            angle (float): Угол, под которым снаряд уходит.
            direction (int): Направление движения снаряда (1 - вправо, -1 - влево).
        """
        self.x = x
        self.y = y
        self.speed = 25
        self.angle = angle
        self.direction = direction
        self.direction_for_blit = False
        self.rect = minigun_bullet_img.get_rect(center=(x, y))

    def move(self):
        """
        Обновляет положение снаряда и проверяет столкновения.

        Возвращает:
            bool: True, если снаряд движется дальше, False, если снаряд должен остановиться
                  из-за столкновения или выхода за пределы экрана.
        """
        if self.direction == 1:  # Если движется вправо
            self.x += self.speed
            self.y += self.speed * math.sin(math.radians(self.angle))
        else:  # Если движется влево
            self.x -= self.speed
            self.y += self.speed * math.sin(math.radians(self.angle))

        self.rect.x = self.x
        self.rect.y = self.y

        for tile in world.obstacle_list:
            if tile[1].colliderect(self.rect):
                return False

        if self.x < 0 or self.x > SCREEN_WIDTH or self.y < 0 or self.y > SCREEN_HEIGHT:
            return False

        return True

    def draw(self, surface):
        """
        Отображает снаряд на переданном игровом экране.

        Параметры:
            surface (pygame.Surface): Экран, на который будет нарисован снаряд.
        """
        if self.direction == 1:
            self.direction_for_blit = False
        else:
            self.direction_for_blit = True

        surface.blit(pygame.transform.flip(minigun_bullet_img, self.direction_for_blit, False), (int(self.x), int(self.y)))


# Класс дроби для дробовика
class Bullet_for_shotgun:
    """Класс, представляющий пулю для дробовика.
        Этот класс отвечает за создание, движение и отображение пули на экране
        """
    def __init__(self, x, y, angle, direction):
        """Инициализирует пулю.

        :param self: Экземпляр класса, который содержит атрибуты и методы игрока.
        :type self: object
        :param x: Начальная координата x пули.
        :type x: float
        :param y: Начальная координата y пули.
        :type y: float
        :param angle: Угол, под которым пуля будет двигаться.
        :type angle: float
        :param direction: Направление движения (1 - вправо, -1 - влево).
        :type direction: int
        :raises ValueError: Если direction не равен 1 или -1.
        """
        self.x = x + 25
        self.y = y + 5
        self.speed = 5
        self.angle = angle
        self.direction = direction
        self.direction_for_blit = False
        self.rect = shotgun_bullet_img.get_rect(center=(x, y))

    def move(self):
        """Двигает пулю по заданному направлению.
                Метод обновляет координаты пули в зависимости от направления и угла.
                Проверяет столкновение с препятствиями и границами экрана

                :param self: экземпляр класса, содержащий атрибуты direction, speed, angle и rect.
                :type self: object
                :returns: True, если пуля продолжает движение; False, если пуля столкнулась с препятствием или вышла за границы экрана.
                :rtype: bool
                :raises AttributeError: если атрибуты класса (direction, speed, angle, rect) не инициализированы.
                """
        if self.direction == 1:
            self.x += self.speed * math.cos(math.radians(self.angle))
            self.y += self.speed * math.sin(math.radians(self.angle))

        else:
            self.x -= self.speed * math.cos(math.radians(self.angle))
            self.y += self.speed * math.sin(math.radians(self.angle))
        self.rect.x = self.x
        self.rect.y = self.y

        for tile in world.obstacle_list:
            if tile[1].colliderect(self.rect):
                return False

        if self.x < 0 or self.x > SCREEN_WIDTH or self.y < 0 or self.y > SCREEN_HEIGHT:
            return False

        return True

    def draw(self, surface):
        """Отображает пулю на заданной поверхности.
                Метод использует метод blit для рисования пули на экране. Пуля может
                быть перевернута в зависимости от направления движения.

                :param self: Экземпляр класса
                :type self: object
                :param surface: Поверхность, на которой будет отображена пуля.
                :type surface: pygame.Surface
                :returns: None
                :rtype: None
                :raises AttributeError: Если surface не является объектом pygame.Surface.
                """
        if self.direction == 1:
            self.direction_for_blit = False
        else:
            self.direction_for_blit = True

        screen.blit(pygame.transform.flip(shotgun_bullet_img, self.direction_for_blit, False),
                    (int(self.x), int(self.y)))


# Класс пули для пистолета
class Bullet_for_pistol:
    """
    Класс для создания пули для пистолета.

    Атрибуты:
        x (float): Положение пули по оси X.
        y (float): Положение пули по оси Y.
        angle (float): Угол, под которым пуля будет двигаться.
        direction (int): Направление движения пули (1 для правого направления, 0 для левого).
        vy (float): Вертикальная скорость пули (по умолчанию 0).
        speed (float): Скорость движения пули (по умолчанию 5).
        direction_for_blit (bool): Переменная для управления направлением отрисовки пули.
        rect (pygame.Rect): Прямоугольник, представляющий размеры пули для коллизий.
    """

    def __init__(self, x, y, angle, direction):
        """
        Инициализирует объект пули.

        Параметры:
            x (float): Начальная позиция пули по оси X.
            y (float): Начальная позиция пули по оси Y.
            angle (float): Угол, под которым пуля будет двигаться.
            direction (int): Направление движения пули (1 или 0).
        """
        self.x = x + 25  # Смещение по X для позиции пули
        self.y = y + 5  # Смещение по Y для позиции пули
        self.vy = 0  # Изначальная вертикальная скорость
        self.speed = 5  # Задаем скорость пули
        self.angle = angle  # Угол движения пули
        self.direction = direction  # Направление полета пули: 1 (вправо) или 0 (влево)
        self.direction_for_blit = False  # Переменная для отрисовки пули в зависимости от направления
        self.rect = pistol_bullet_img.get_rect(
            center=(x, y))  # Создание прямоугольника для отрисовки пули и её коллизий

    def move(self):
        """
        Двигает пулю в зависимости от её направления.

        Возвращает:
            bool: True, если пуля продолжает движение, иначе False, если произошло столкновение или пуля вышла за границы экрана.
        """
        # Движение пули в зависимости от направления
        if self.direction == 1:
            self.x += self.speed * math.cos(math.radians(self.angle))  # Движение вправо
            self.y += self.vy  # Вертикальная зависимость

        else:
            self.x -= self.speed * math.cos(math.radians(self.angle))  # Движение влево
            self.y += self.vy  # Вертикальная зависимость

        # Обновление позиции прямоугольника для отрисовки
        self.rect.x = self.x
        self.rect.y = self.y

        # Проверка на столкновения с препятствиями
        for tile in world.obstacle_list:
            if tile[1].colliderect(self.rect):
                return False  # Если произошло столкновение, возвращаем False

        # Проверка выхода за границы экрана
        if self.x < 0 or self.x > SCREEN_WIDTH or self.y < 0 or self.y > SCREEN_HEIGHT:
            return False  # Если пуля вышла за границы, возвращаем False

        return True  # Если всё в порядке, возвращаем True

    def draw(self, surface):
        """
        Рисует пулю на экране.

        Параметры:
            surface (pygame.Surface): Поверхность, на которой будет нарисована пуля.
        """
        # Установка направления для отрисовки
        if self.direction == 1:
            self.direction_for_blit = False  # Пуля не перевернута
        else:
            self.direction_for_blit = True  # Пуля перевернута для отображения влево

        # Отрисовка пули с использованием изображения и её положения
        screen.blit(pygame.transform.flip(pistol_bullet_img, self.direction_for_blit, False),
                    (int(self.x), int(self.y)))  # В зависимости от направления отрисовка переворачивается


# Класс пивной гранаты
class Beer(pygame.sprite.Sprite):
    """
    Класс Beer представляет собой снаряд в игре, который может взрываться,
    нанося урон игроку. Он управляется гравитацией и движется в указанном направлении.
    """

    def __init__(self, x, y, direction):
        """
        Инициализация объекта Beer.

        Параметры:
        x (int): Позиция по оси X, где должен быть создан снаряд.
        y (int): Позиция по оси Y, где должен быть создан снаряд.
        direction (int): Направление движения снаряда (1 или -1).
        """
        pygame.sprite.Sprite.__init__(self)  # Инициализация родительского класса
        self.image = beer_img  # Изображение снаряда
        self.rect = self.image.get_rect()  # Получение прямоугольника для коллизий
        self.rect.center = (x, y)  # Установка центра снаряда
        self.speed = 10  # Скорость движения снаряда
        self.damage = 50  # Базовый урон снаряда
        self.chance = random.randint(0, 100)  # Рандомное число для случайного эффекта
        self.direction = direction  # Направление движения
        self.timer = 100  # Время до взрыва (в тиках)
        self.explosion_radius = 1000  # Радиус взрыва
        self.vy = -15  # Начальная вертикальная скорость (вверх)
        self.gravity = 0.7  # Значение гравитации, добавляемое к вертикальной скорости

    def update(self):
        """
        Обновляет состояние снаряда. Уменьшает таймер взрыва,
        применяет гравитацию и проверяет столкновения.
        """
        self.timer -= 1  # Уменьшение таймера
        if self.timer <= 0:
            self.explode()  # Взрыв, если таймер истек

        self.vy += self.gravity  # Применение гравитации к вертикальной скорости
        self.rect.x += self.speed * self.direction  # Обновление позиции по оси X
        self.rect.y += self.vy  # Обновление позиции по оси Y

        # Проверка столкновения с препятствиями
        for tile in world.obstacle_list:
            if tile[1].colliderect(self.rect):  # Если есть столкновение с препятствием
                self.explode()  # Взрыв при столкновении

        # Проверка на столкновение с игроками
        if self.rect.colliderect(player2.rect):  # Если снаряд пересекает игрока
            self.explode()  # Взрыв при столкновении с игроком

    def explode(self):
        """
        Обрабатывает взрыв снаряда. Наносит урон игроку и удаляет
        снаряд из игры.
        """
        self.damage_players(player2)  # Наносит урон второму игроку
        self.kill()  # Удаление снаряда после взрыва

    def damage_players(self, player):
        """
        Наносит урон указанному игроку, основываясь на расстоянии
        до него от точки взрыва.

        Параметры:
        player (Player): Игрок, которому будет нанесен урон.
        """
        if self.chance in range(0, 5):  # Проверка шанса для увеличенного урона
            self.damage = self.damage * 20000  # Увеличение урона
        else:
            self.damage = int(self.damage / self.damage)  # Установка урона в 1, если не попал
        distance = math.hypot(self.rect.centerx - player.rect.centerx,
                              self.rect.centery - player.rect.centery)  # Вычисление расстояния до игрока
        if distance <= self.explosion_radius:
            player.hp -= self.damage  # Нанесение урона игроку
            player.check_alive()  # Проверка состояния игрока после получения урона

# Класс стрелы
class Arrow:
    def __init__(self, x, y, target_x, target_y,direction):
        """
        Инициализация стрелы.

        :param x: Начальная координата по оси X.
        :param y: Начальная координата по оси Y.
        :param target_x: Координата X цели, к которой направлена стрела.
        :param target_y: Координата Y цели, к которой направлена стрела.
        :param direction: Направление полета стрелы (1 - вправо, -1 - влево).
        """
        self.x = x
        self.y = y
        self.speed = 10
        self.direction = direction
        self.direction_for_blit = False

        self.rect = arrow_img.get_rect(center=(x, y))

        # Вычисление угла к цели (курсору)
        dx = target_x - x
        dy = target_y - y
        distance = math.sqrt(dx**2 + dy**2)
        self.dx = dx / distance
        self.dy = dy / distance

    def move(self):
        """
        Обновление позиции стрелы согласно направлению и скорости.

        :return: True, если стрела еще в пределах экрана и не столкнулась с препятствием, иначе False.
        """
        self.x += self.dx * self.speed
        self.y += self.dy * self.speed + bow_gravity  # Немного падает вниз

        self.rect.x = self.x
        self.rect.y = self.y

        for tile in world.obstacle_list:
            if tile[1].colliderect(self.rect):
                return False

        if self.x < 0 or self.x > SCREEN_WIDTH or self.y < 0 or self.y > SCREEN_HEIGHT:
            return False

        return True

    def draw(self, surface):
        """
        Отрисовка стрелы на заданной поверхности.

        :param surface: Поверхность, на которой будет отрисована стрела.
        """
        if self.direction == 1:
            self.direction_for_blit = False
        else:
            self.direction_for_blit = True
        screen.blit(pygame.transform.flip(arrow_img, self.direction_for_blit, False),
                    (int(self.x), int(self.y)))


# Класс пули для снайперской винтовки
class Bullet_for_sniper_rifle:
    """
    Класс представляют пулю для снайперской винтовки.

    Атрибуты:
    - x (float): Текущая координата X пули.
    - y (float): Текущая координата Y пули.
    - target_x (float): Координата X цели, на которую нацелена пуля.
    - target_y (float): Координата Y цели, на которую нацелена пуля.
    - direction (int): Направление полета пули (1 - вправо, -1 - влево).
    - direction_for_blit (bool): Флаг, указывающий, следует ли перевернуть изображение пули.
    - speed (int): Скорость полета пули.
    - rect (pygame.Rect): Прямоугольник, который описывает область пули для коллизий.
    - dx (float): Изменение координаты X для движения пули.

    Методы:
    - move(): Обновляет позицию пули и проверяет на столкновения с препятствиями.
    - draw(surface): Отображает пулю на заданной поверхности.
    """

    def __init__(self, x, y, target_x, target_y, direction):
        """
        Инициализирует экземпляр класса Bullet_for_sniper_rifle.

        Параметры:
        - x (float): Начальная координата X пули.
        - y (float): Начальная координата Y пули.
        - target_x (float): Координата X цели, на которую будет нацелена пуля.
        - target_y (float): Координата Y цели, на которую будет нацелена пуля.
        - direction (int): Направление полета пули (1 - вправо, -1 - влево).
        """
        self.x = x
        self.y = y
        self.direction = direction
        self.direction_for_blit = False
        self.speed = 20
        self.rect = sniper_rifle_bullet_img.get_rect(center=(x, y))

        dx = target_x - x
        distance = math.sqrt(dx ** 2)
        self.dx = dx / distance

    def move(self):
        """
        Обновляет позицию пули и проверяет на столкновения.

        Возвращает:
        - bool: True, если пуля в пределах игрового окна и не столкнулась с препятствием,
                иначе False.
        """
        self.x += self.dx * self.speed

        self.rect.x = self.x
        self.rect.y = self.y

        for tile in world.obstacle_list:
            if tile[1].colliderect(self.rect):
                return False  # Пуля столкнулась с препятствием

        if self.x < 0 or self.x > SCREEN_WIDTH or self.y < 0 or self.y > SCREEN_HEIGHT:
            return False  # Пуля покинула пределы экрана

        return True  # Пуля все еще в игре

    def draw(self, surface):
        """
        Отображает пулю на заданной поверхности.

        Параметры:
        - surface (pygame.Surface): Поверхность, на которой будет нарисована пуля.
        """
        if self.direction == 1:
            self.direction_for_blit = False
        else:
            self.direction_for_blit = True
        surface.blit(pygame.transform.flip(sniper_rifle_bullet_img, self.direction_for_blit, False),
                     (int(self.x), int(self.y)))


import pygame

class Medkit(pygame.sprite.Sprite):
    """
    Класс Medkit представляет аптечку в игре.
    Она восстанавливает здоровье игрока при столкновении.
    Аптечка удаляется из игры после использования.

    Атрибуты:
        image (pygame.Surface): Изображение аптечки.
        rect (pygame.Rect): Прямоугольник, описывающий позицию и размер аптечки.
        heal_amount (int): Количество здоровья, восстанавливаемое аптечкой (по умолчанию 20).

    Методы:
        __init__(x, y): Инициализация аптечки с заданной позицией.
        update(player): Проверяет столкновение с игроком и восстанавливает здоровье.
    """

    def __init__(self, x, y):
        """
        Инициализация аптечки.

        Параметры:
            x (int): Координата по оси X, где будет расположена аптечка.
            y (int): Координата по оси Y, где будет расположена аптечка.
        """
        pygame.sprite.Sprite.__init__(self)  # Инициализация родительского класса
        self.image = medkit_img  # Загрузка изображения аптечки
        self.rect = self.image.get_rect()  # Получение прямоугольника, описывающего аптечку
        self.rect.center = (x, y)  # Установка центра аптечки в заданные координаты
        self.heal_amount = 20  # Количество восстанавливаемого здоровья

    def update(self, player):
        """
        Обновление состояния аптечки. Проверяет, сталкивается ли она с игроком.
        Если есть столкновение, восстанавливает здоровье игрока.

        Параметры:
            player (Player): Экземпляр класса игрока, который должен иметь атрибуты 'rect' и 'hp'.
        """
        if self.rect.colliderect(player.rect):  # Проверка на столкновение с игроком
            player.hp = min(player.hp + self.heal_amount, 100)  # Восстановление здоровья, ограниченное 100
            self.kill()  # Удаление аптечки из игры после использования


class Grenade(pygame.sprite.Sprite):
    """
    Класс, представляющий гранату. Наследуется от pygame.sprite.Sprite.
    Граната может двигаться в указанном направлении, иметь таймер до взрыва,
    а также наносить урон игрокам в радиусе взрыва.

    Атрибуты:
    ----------
    image : pygame.Surface
        Графическое представление гранаты.
    rect : pygame.Rect
        Прямоугольник, определяющий положение и размеры гранаты.
    speed : int
        Скорость перемещения гранаты.
    direction : int
        Направление движения гранаты (1 или -1).
    timer : int
        Время до взрыва (в тиках).
    explosion_radius : int
        Радиус взрыва гранаты.
    vy : int
        Начальная вертикальная скорость (вверх).
    gravity : float
        Значение гравитации, влияющее на вертикальную скорость.

    Методы:
    -------
    update():
        Обновляет состояние гранаты, проверяет таймер взрыва и
        обновляет позицию гранаты, а также проверяет столкновения.

    explode():
        Обрабатывает взрыв гранаты, наносит урон игрокам и удаляет гранату.

    damage_players(player):
        Наносит урон игроку, если он находится в радиусе взрыва.
    """

    def __init__(self, x, y, direction):
        """
        Инициализация гранаты.

        Параметры:
        ----------
        x : int
            Начальная позиция по оси X.
        y : int
            Начальная позиция по оси Y.
        direction : int
            Направление движения (1 - вправо, -1 - влево).
        """

        pygame.sprite.Sprite.__init__(self)
        self.image = grenade_img  # Пример: маленькая красная окружность
        # screen.blit(self.image,(5,5))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 10  # Скорость перемещения гранаты
        self.direction = direction  # Направление движения
        self.timer = 100  # Время до взрыва (в тиках)
        self.explosion_radius = 100  # Радиус взрыва
        self.vy = -15  # Начальная вертикальная скорость (вверх)
        self.gravity = 0.7  # Значение гравитации

    def update(self):
        """
        Обновляет состояние гранаты. Уменьшает таймер взрыва,
        обновляет позицию гранаты с учетом направления и гравитации,
        а также проверяет столкновения с препятствиями и игроками.
        Если таймер достигает нуля, граната взрывается.
        """

        self.timer -= 1
        if self.timer <= 0:
            self.explode()

        self.vy += self.gravity  # Применение гравитации
        self.rect.x += self.speed * self.direction  # Обновление позиции по оси X
        self.rect.y += self.vy  # Обновление позиции по оси Y

        # Проверка столкновения с препятствиями
        for tile in world.obstacle_list:
            if tile[1].colliderect(self.rect):
                self.explode()  # Взрыв при столкновении с препятствием

        # Добавьте проверку на столкновение с игроками:
        if self.rect.colliderect(player2.rect):
            self.explode()  # Взрыв при столкновении со вторым игроком

    def explode(self):
        """
        Обрабатывает взрыв гранаты. Наносит урон игрокам в радиусе взрыва
        и удаляет гранату из игры.
        """

        self.damage_players(player1)  # Проверяем первого игрока
        self.damage_players(player2)  # Проверяем второго игрока
        self.kill()  # Удаление гранаты после взрыва

    def damage_players(self, player):
        """
        Наносит урон указанному игроку, если он находится в радиусе взрыва
        гранаты.

        Параметры:
        ----------
        player : Player
            Игрок, которому будет нанесен урон.
        """

        distance = math.hypot(self.rect.centerx - player.rect.centerx,
                              self.rect.centery - player.rect.centery)
        if distance <= self.explosion_radius:
            player.hp -= 50  # Урон от гранаты
            player.check_alive()  # Проверка состояния игрока


start_button = Button(500, 300, start_img, 2)
exit_button = Button(520, 430, exit_img, 1.75)
pistol_button = Button(338, 90, pistol_img, 0.5)
shotgun_button = Button(360, 180, shotgun_img, 0.5)
rifle_button = Button(360, 290, rifle_img, 0.5)
minigun_button = Button(360, 360, minigun_img, 0.5)
bow_button = Button(417, 95, bow_img, 0.075)
sniper_rifle_button = Button(545, 415, sniper_rifle_img, 0.22)
medkit_button = Button(485, 105, medkit_img, 0.65)
grenade_button = Button(531, 89, grenade_img, 1.2)
beer_button = Button(585, 89, beer_img, 1.3)
level1_button = Button(270, 400, level1_img, 0.5)
level2_button = Button(470, 400, level2_img, 0.5)
levelrandom_button = Button(670, 400, levelrandom_img, 0.65)

bullet_group = pygame.sprite.Group()
medkit_group = pygame.sprite.Group()
grenade_group = pygame.sprite.Group()
beer_group = pygame.sprite.Group()

run = True
while run:
    player1 = Worm("1", 300, 500, 0.19, 7, 100)
    player2 = Worm("1", 600, 500, 0.19, 7, 100)

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
                    """Класс, представляющий игровой мир.
                    Этот класс отвечает за инициализацию и отрисовку
                    препятствий и декораций в игровом мире.
                    """
                    def __init__(self):
                        """Инициализирует список препятствий."""
                        self.obstacle_list = []

                    def process_data(self, data):
                        """Обрабатывает данные уровня и создает препятствия.

                        :param self: Экземпляр класса
                        :type self: object
                        :param data: Данные уровня в виде двумерного массива.
                        :type data: list of list of int
                        :raises ValueError: Если данные уровня имеют неверный формат.
                        """
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
                                    elif tile >= 11 and tile <= 14:
                                        decoration = Decoration(img, x * tile_size, y * tile_size)
                                        decoration_group.add(decoration)
                                    elif tile >= 9 and tile <= 10:
                                        water = Water(img, x * tile_size, y * tile_size)
                                        water_group.add(water)

                    def draw(self):
                        """Отрисовывает все препятствия на экране.

                        :param self: Экземпляр класса
                        :type self: object
                        :returns: None
                        :rtype: None
                        """
                        for tile in self.obstacle_list:
                            tile[1][0] += screen_scroll
                            screen.blit(tile[0], tile[1])

                class Decoration(pygame.sprite.Sprite):
                    """Класс, представляющий декорацию в игровом мире."""
                    def __init__(self, img, x, y):
                        """Инициализирует объект декорации.

                        :param self: Экземпляр класса
                        :type self: object
                        :param img: Изображение, которое будет использоваться для декорации.
                        :type img: pygame.Surface
                        :param x: Позиция по оси X для размещения декорации.
                        :type x: int
                        :param y: Позиция по оси Y для размещения декорации.
                        :type y: int

                        :raises TypeError: Если img не является экземпляром pygame.Surface.
                        """
                        pygame.sprite.Sprite.__init__(self)
                        self.image = img
                        self.rect = self.image.get_rect()
                        self.rect.midtop = (x + tile_size // 2, y + (tile_size - self.image.get_height()))

                    def update(self):
                        """Обновляет позицию декорации.

                        :param self: Экземпляр класса
                        :type self: object
                        :returns: None
                        :rtype: None
                        """
                        self.rect.x += screen_scroll

                class Water(pygame.sprite.Sprite):
                    def __init__(self, img, x, y):
                        """Инициализирует объект воды.

                        :param self: Экземпляр класса
                        :type self: object
                        :param img: Изображение воды, которое будет отображаться.
                        :type img: pygame.Surface
                        :param x: Координата по оси x для размещения объекта.
                        :type x: int
                        :param y: Координата по оси y для размещения объекта.
                        :type y: int
                        :raises ValueError: Если переданное изображение не является объектом типа pygame.Surface.
                        """
                        pygame.sprite.Sprite.__init__(self)
                        self.image = img
                        self.rect = self.image.get_rect()
                        self.rect.midtop = (x + tile_size // 2, y + (tile_size - self.image.get_height()))

                    def update(self):
                        """Обновляет позицию объекта воды, сдвигая его по оси X в соответствии с переменной screen_scroll."""
                        self.rect.x += screen_scroll

                decoration_group = pygame.sprite.Group()
                water_group = pygame.sprite.Group()

                world_data = []
                for row in range(rows):
                    r = [-1] * cols
                    world_data.append(r)

                with open(f'level{level}_data.csv', newline='') as csvfile:
                    reader = csv.reader(csvfile, delimiter=',')
                    for x, row in enumerate(reader):
                        for y, tile in enumerate(row):
                            world_data[x][y] = int(tile)

                world = World()
                world.process_data((world_data))

                run_level_menu = False
            pygame.display.update()

        start_ticks = pygame.time.get_ticks()
        shoot_count = 0
        current_weapon = "rifle"

        while run_game:
            tickrate.tick(FPS)
            draw_bg()
            world.draw()
            player1.update_animation()
            player1.draw()
            player2.update_animation()
            player2.draw()
            bullet_group.update()
            bullet_group.draw(screen)
            decoration_group.draw(screen)
            decoration_group.update()
            water_group.draw(screen)
            water_group.update()
            run_weapon_menu = True
            draw_health_bar(player1.hp, 10, 10, 200, 20)
            draw_health_bar(player2.hp, 10, 40, 200, 20)

            seconds_passed = (pygame.time.get_ticks() - start_ticks) / 1000
            remaining_time = time_to_move - seconds_passed
            screen.blit(time_bg_img, (470, -10))

            player1.shoot_rifle()
            player1.update_rifle(player2)
            player1.draw_rifle(screen)
            player1.update_shotgun(player2)
            player1.draw_shotgun(screen)
            player1.update_pistol(player2)
            player1.draw_pistol(screen)
            player1.shoot_minigun()
            player1.update_minigun(player2)
            player1.draw_minigun(screen)
            player1.update_bow(player2)
            player1.draw_bow(screen)
            player1.update_sniper_rifle(player2)
            player1.draw_sniper_rifle(screen)
            medkit_group.update(player1)
            medkit_group.draw(screen)
            grenade_group.update()
            grenade_group.draw(screen)
            beer_group.update()
            beer_group.draw(screen)

            if remaining_time > 0:
                if remaining_time >= 10:
                    remaining_time = int(remaining_time)
                    text_for_time = font_for_time.render(str(remaining_time), False, (0, 0, 0))
                    screen.blit(text_for_time, (575, 5))
                else:
                    remaining_time = int(remaining_time)
                    text_for_time = font_for_time.render(str(remaining_time), False, (0, 0, 0))
                    screen.blit(text_for_time, (609, 5))

                if shoot_count < 3 and player1.alive:
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
                            if event.key == pygame.K_SPACE and player1.rifle_bullets_to_shoot == 3 and current_weapon == "rifle":
                                player1.rifle_shooting = True
                                shoot_count += 1
                            if event.key == pygame.K_SPACE and player1.minigun_bullets_to_shoot == 15 and current_weapon == "minigun":
                                player1.minigun_shooting = True
                                shoot_count += 1
                            if event.key == pygame.K_SPACE and current_weapon == "shotgun":
                                player1.shoot_shotgun()
                                shoot_count += 1
                            if event.key == pygame.K_SPACE and current_weapon == "pistol":
                                player1.shoot_pistol()
                                shoot_count += 1
                            if event.key == pygame.K_SPACE and current_weapon == "bow":
                                player1.shoot_bow()
                                shoot_count += 1
                            if event.key == pygame.K_SPACE and current_weapon == "sniper_rifle":
                                player1.shoot_sniper_rifle()
                                shoot_count += 1
                            if event.key == pygame.K_SPACE and current_weapon == "medkit":
                                medkit = Medkit(player1.rect.centerx + 50, player1.rect.centery)
                                medkit_group.add(medkit)
                                shoot_count += 3
                            if event.key == pygame.K_SPACE and current_weapon == "grenade":  # Например, клавиша G для броска гранаты
                                grenade = Grenade(player1.rect.centerx, player1.rect.centery, player1.direction)
                                grenade_group.add(grenade)
                                shoot_count += 3
                            if event.key == pygame.K_SPACE and current_weapon == "beer":  # Например, клавиша G для броска гранаты
                                beer = Beer(player1.rect.centerx, player1.rect.centery, player1.direction)
                                beer_group.add(beer)
                                shoot_count += 1

                            if event.key == pygame.K_z:
                                player1.alive = False
                                player1.hp = 0
                            if event.key == pygame.K_e:
                                while run_weapon_menu:
                                    screen.blit(guns_menu_img, (340, 40))
                                    if pistol_button.draw(screen):
                                        current_weapon = "pistol"
                                        run_weapon_menu = False
                                    if rifle_button.draw(screen):
                                        current_weapon = "rifle"
                                        run_weapon_menu = False
                                    if shotgun_button.draw(screen):
                                        current_weapon = "shotgun"
                                        run_weapon_menu = False
                                    if minigun_button.draw(screen):
                                        current_weapon = "minigun"
                                        run_weapon_menu = False
                                    if bow_button.draw(screen):
                                        current_weapon = "bow"
                                        run_weapon_menu = False
                                    if sniper_rifle_button.draw(screen):
                                        current_weapon = "sniper_rifle"
                                        run_weapon_menu = False
                                    if medkit_button.draw(screen):
                                        current_weapon = "medkit"
                                        run_weapon_menu = False
                                    if grenade_button.draw(screen):
                                        current_weapon = "grenade"
                                        run_weapon_menu = False
                                    if beer_button.draw(screen):
                                        current_weapon = "beer"
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
                            if event.key == pygame.K_SPACE:
                                player1.rifle_shooting = False
                                player1.rifle_bullets_to_shoot = 3
                            if event.key == pygame.K_SPACE:
                                player1.minigun_shooting = False
                                player1.minigun_bullets_to_shoot = 15

                else:
                    shoot_count = 0
                    time_to_move = time_to_move
                    start_ticks = pygame.time.get_ticks()
                    text_for_time = font_for_time.render(str(remaining_time), False, (0, 0, 0))
                    screen.blit(text_for_time, (609, 5))
            else:
                text_for_time = font_for_time.render("fire", False, (0, 0, 0))
                screen.blit(text_for_time, (526, 5))
                if shoot_count == 3:
                    shoot_count = 0
                    time_to_move = time_to_move
                    start_ticks = pygame.time.get_ticks()
                    text_for_time = font_for_time.render(str(remaining_time), False, (0, 0, 0))
                    screen.blit(text_for_time, (609, 5))
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run_game = False
                        run = False
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            run_game = False
                        if event.key == pygame.K_SPACE and player1.rifle_bullets_to_shoot == 3 and current_weapon == "rifle":
                            player1.rifle_shooting = True
                            shoot_count += 1
                        if event.key == pygame.K_SPACE and player1.minigun_bullets_to_shoot == 15 and current_weapon == "minigun":
                            player1.minigun_shooting = True
                            shoot_count += 1
                        if event.key == pygame.K_SPACE and current_weapon == "shotgun":
                            player1.shoot_shotgun()
                            shoot_count += 1
                        if event.key == pygame.K_SPACE and current_weapon == "pistol":
                            player1.shoot_pistol()
                            shoot_count += 1
                        if event.key == pygame.K_SPACE and current_weapon == "bow":
                            player1.shoot_bow()
                            shoot_count += 1
                        if event.key == pygame.K_SPACE and current_weapon == "sniper_rifle":
                            player1.shoot_sniper_rifle()
                            shoot_count += 1
                        if event.key == pygame.K_SPACE and current_weapon == "medkit":
                            medkit = Medkit(player1.rect.centerx + 50, player1.rect.centery)
                            medkit_group.add(medkit)
                            shoot_count += 3
                        if event.key == pygame.K_SPACE and current_weapon == "grenade":  # Например, клавиша G для броска гранаты
                            grenade = Grenade(player1.rect.centerx, player1.rect.centery, player1.direction)
                            grenade_group.add(grenade)
                            shoot_count += 3
                        if event.key == pygame.K_SPACE and current_weapon == "beer":  # Например, клавиша G для броска гранаты
                            beer = Beer(player1.rect.centerx, player1.rect.centery, player1.direction)
                            beer_group.add(beer)
                            shoot_count += 1

                        if event.key == pygame.K_e:
                            while run_weapon_menu:
                                screen.blit(guns_menu_img, (340, 40))
                                if pistol_button.draw(screen):
                                    current_weapon = "pistol"
                                    run_weapon_menu = False
                                if rifle_button.draw(screen):
                                    current_weapon = "rifle"
                                    run_weapon_menu = False
                                if shotgun_button.draw(screen):
                                    current_weapon = "shotgun"
                                    run_weapon_menu = False
                                if bow_button.draw(screen):
                                    current_weapon = "bow"
                                    run_weapon_menu = False
                                if sniper_rifle_button.draw(screen):
                                    current_weapon = "sniper_rifle"
                                    run_weapon_menu = False
                                if medkit_button.draw(screen):
                                    current_weapon = "medkit"
                                    run_weapon_menu = False
                                if grenade_button.draw(screen):
                                    current_weapon = "grenade"
                                    run_weapon_menu = False
                                if beer_button.draw(screen):
                                    current_weapon = "beer"
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
                        if event.key == pygame.K_SPACE:
                            player1.rifle_shooting = False
                            player1.rifle_bullets_to_shoot = 3
                        if event.key == pygame.K_SPACE:
                            player1.minigun_shooting = False
                            player1.minigun_bullets_to_shoot = 15

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

            pygame.display.update()
    if exit_button.draw(screen):
        run = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()