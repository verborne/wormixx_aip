

import pygame
import math

# Инициализация Pygame
pygame.init()

# Настройки экрана
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Лук в Pygame с гравитацией и временем зажатия")

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

# Константы
GRAVITY = 0.2  # Ускорение свободного падения
MAX_SPEED = 20  # Максимальная скорость стрелы


# Класс для стрелы
class Arrow:
    def __init__(self, x, y, angle, speed):
        self.x = x
        self.y = y
        self.angle = angle
        self.speed = speed
        self.vy = 0  # Вертикальная скорость
        self.alive = True

    def update(self):
        # Обновляем горизонтальную и вертикальную позицию стрелы
        self.x += self.speed * math.cos(math.radians(self.angle))
        self.vy += GRAVITY  # Увеличиваем вертикальную скорость под воздействием гравитации
        self.y += self.vy  # Обновляем вертикальную позицию стрелы

        # Проверяем, вышла ли стрела за пределы экрана
        if self.x < 0 or self.x > WIDTH or self.y > HEIGHT:
            self.alive = False

    def draw(self, surface):
        # Отрисовываем стрелу
        arrow_length = 20
        end_x = self.x + arrow_length * math.cos(math.radians(self.angle))
        end_y = self.y + arrow_length * math.sin(math.radians(self.angle))
        pygame.draw.line(surface, GREEN, (self.x, self.y), (end_x, end_y), 3)


# Класс для лука
class Bow:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.arrows = []
        self.shooting = False
        self.shoot_start_time = 0

    def shoot(self, angle, speed):
        # Создаем стрелу и добавляем ее в список
        arrow = Arrow(self.x, self.y, angle, speed)
        self.arrows.append(arrow)

    def update(self):
        # Обновляем стрелы
        self.arrows = [arrow for arrow in self.arrows if arrow.alive]
        for arrow in self.arrows:
            arrow.update()

    def draw(self, surface):
        # Отрисовываем лук (просто линия для примера)
        pygame.draw.line(surface, BLACK, (self.x, self.y), pygame.mouse.get_pos(), 5)

        # Отрисовываем стрелы
        for arrow in self.arrows:
            arrow.draw(surface)


# Основной игровой цикл
def main():
    clock = pygame.time.Clock()
    running = True
    bow = Bow(WIDTH // 2, HEIGHT // 2)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:  # Начинаем стрелять при нажатии пробела
                    bow.shooting = True
                    bow.shoot_start_time = pygame.time.get_ticks()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:  # Заканчиваем стрелять при отпускании пробела
                    bow.shooting = False
                    shoot_duration = pygame.time.get_ticks() - bow.shoot_start_time
                    speed = min(MAX_SPEED, shoot_duration / 10)  # Максимальная скорость стрелы
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    angle = math.degrees(math.atan2(mouse_y - bow.y, mouse_x - bow.x))
                    bow.shoot(angle, speed)

        # Обновляем состояние лука и стрел
        bow.update()

        # Отрисовка
        screen.fill(WHITE)
        bow.draw(screen)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
