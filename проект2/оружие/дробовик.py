import pygame
import random
import math

# Инициализация Pygame
pygame.init()

# Настройки экрана
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Дробовик")
shotgun_bullet_img = pygame.image.load("пуля_автомат.png").convert_alpha()
# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Класс для дробовика
class Shotgun:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.bullets = []

    def shoot(self):
        # Создание нескольких пуль (например, 5)
        for _ in range(9):
            angle = random.uniform(-30, 30)  # Угол разброса
            bullet = Bullet(self.x, self.y, angle)
            self.bullets.append(bullet)

    def update(self):
        for bullet in self.bullets:
            bullet.move()

    def draw(self, surface):
        # Здесь можно нарисовать дробовик (например, как прямоугольник)
        pygame.draw.rect(surface, BLACK, (self.x, self.y, 50, 10))
        for bullet in self.bullets:
            bullet.draw(surface)

# Класс для пули
class Bullet:
    def __init__(self, x, y, angle):
        self.x = x + 25  # Смещение для центра дробовика
        self.y = y + 5
        self.speed = 5
        self.angle = angle

    def move(self):
        # Движение пули
        self.x += self.speed * math.cos(math.radians(self.angle))
        self.y += self.speed * math.sin(math.radians(self.angle))

    def draw(self, surface):

        screen.blit(shotgun_bullet_img,(int(self.x), int(self.y)))

# Основной игровой цикл

clock = pygame.time.Clock()
shotgun = Shotgun(400, 300)
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:  # Выстрел при нажатии пробела
                shotgun.shoot()

    screen.fill(WHITE)
    shotgun.update()
    shotgun.draw(screen)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
