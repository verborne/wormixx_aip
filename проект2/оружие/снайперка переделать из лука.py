import pygame
import random
import math
# Инициализация Pygame
pygame.init()

# Настройки экрана
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Пистолет в Pygame")

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Класс для пули
class Bullet:
    def __init__(self, x, y, angle):
        self.x = x
        self.y = y
        self.speed = 25
        self.angle = angle

    def move(self):
        # Движение пули
        self.x += self.speed * math.cos(math.radians(self.angle))
        self.y += self.speed * math.sin(math.radians(self.angle))

    def draw(self, surface):
        pygame.draw.circle(surface, BLACK, (int(self.x), int(self.y)), 8)

# Класс для пистолета
class Sniper_rifle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.bullets = []
        self.can_shoot = True  # Переменная для отслеживания возможности стрельбы
        self.reload_time = 700  # Время перезарядки (в миллисекундах)
        self.last_shot_time = 0

    def shoot(self):
        current_time = pygame.time.get_ticks()
        if self.can_shoot:  # Проверяем, можем ли мы стрелять
            angle = random.uniform(0, 0)  # Угол разброса
            bullet = Bullet(self.x + 25, self.y + 5, angle)  # Смещение для центра
            self.bullets.append(bullet)
            self.can_shoot = False  # Блокируем возможность стрельбы
            self.last_shot_time = current_time  # Обновляем время последнего выстрела

    def update(self):
        # Обновляем позиции пуль
        for bullet in self.bullets:
            bullet.move()

        # Проверяем, прошло ли время перезарядки
        if not self.can_shoot:
            current_time = pygame.time.get_ticks()
            if current_time - self.last_shot_time >= self.reload_time:
                self.can_shoot = True  # Разрешаем стрелять снова

    def draw(self, surface):
        # Рисуем пистолет (например, как прямоугольник)
        pygame.draw.rect(surface, BLACK, (self.x, self.y, 50, 10))
        for bullet in self.bullets:
            bullet.draw(surface)

# Основной игровой цикл
def main():
    clock = pygame.time.Clock()
    pistol = Sniper_rifle(400, 300)
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:  # Если нажата клавиша пробела
            pistol.shoot()  # Проверяем возможность стрельбы

        pistol.update()

        screen.fill(WHITE)
        pistol.draw(screen)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
