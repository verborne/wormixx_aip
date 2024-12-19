import math
import pygame
import random

# Инициализация Pygame
pygame.init()

# Настройки экрана
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Автомат в Pygame")
rifle_bullet_img = pygame.image.load("пуля.png").convert_alpha()

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Класс для пули
class Bullet_for_rifle:
    def __init__(self, x, y, angle):
        self.x = x
        self.y = y
        self.speed = 10
        self.angle = angle

    def move(self):
        # Движение пули
        self.x += self.speed * math.cos(math.radians(self.angle))
        self.y += self.speed * math.sin(math.radians(self.angle))

    def draw(self, surface):
        screen.blit(rifle_bullet_img,(int(self.x), int(self.y)))

# Класс для автомата
class AutomaticRifle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.bullets = []
        self.last_bullet_time = 0
        self.bullet_delay = 200  # Задержка между пулями (в миллисекундах)
        self.bullets_to_shoot = 3
        self.shooting = False

    def shoot(self):
        current_time = pygame.time.get_ticks()
        if self.shooting and self.bullets_to_shoot > 0 and current_time - self.last_bullet_time > self.bullet_delay:
            # Создание пули с разбросом
            angle = random.uniform(-10, 10)  # Угол разброса
            bullet = Bullet_for_rifle(self.x + 25, self.y + 5, angle)  # Смещение для центра
            self.bullets.append(bullet)
            self.last_bullet_time = current_time  # Обновляем время последней пули
            self.bullets_to_shoot -= 1  # Уменьшаем количество оставшихся пуль

    def update(self):
        # Обновляем позиции пуль
        for bullet in self.bullets:
            bullet.move()

    def draw(self, surface):
        # Рисуем автомат (например, как прямоугольник)
        pygame.draw.rect(surface, BLACK, (self.x, self.y, 50, 10))
        for bullet in self.bullets:
            bullet.draw(surface)

# Основной игровой цикл
def main():
    clock = pygame.time.Clock()
    rifle = AutomaticRifle(400, 300)
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:  # Проверяем нажатие клавиши
                if event.key == pygame.K_SPACE and rifle.bullets_to_shoot == 3:  # Проверяем, что можно стрелять
                    rifle.shooting = True  # Начинаем стрельбу

            if event.type == pygame.KEYUP:  # Проверяем отпускание клавиши
                if event.key == pygame.K_SPACE:
                    rifle.shooting = False  # Останавливаем стрельбу
                    rifle.bullets_to_shoot = 3  # Сбросить количество пуль

        rifle.shoot()  # Проверяем возможность стрельбы
        rifle.update()

        screen.fill(WHITE)
        rifle.draw(screen)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()

