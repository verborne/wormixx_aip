import pygame
import sys

# Инициализация Pygame
pygame.init()

# Установка параметров окна
screen = pygame.display.set_mode((400, 300))
pygame.display.set_caption("Обратный отсчет")

# Установка начального времени
countdown_time = 10  # Время обратного отсчета в секундах
start_ticks = pygame.time.get_ticks()  # Получаем текущее время

# Основной цикл
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Вычисляем оставшееся время
    seconds_passed = (pygame.time.get_ticks() - start_ticks) / 1000  # Переводим в секунды
    remaining_time = countdown_time - seconds_passed


    # Если время истекло, выводим сообщение
    if remaining_time <= 0:

        countdown_time = 10
        print(remaining_time)

    else:
        print(f"Осталось времени: {int(remaining_time)}")

    # Обновляем экран
    screen.fill((0, 0, 0))  # Очищаем экран
    font = pygame.font.Font(None, 74)
    text = font.render(str(int(remaining_time)), True, (255, 255, 255))
    screen.blit(text, (150, 100))
    pygame.display.flip()  # Обновляем экран

    # Задержка, чтобы не перегружать процессор
      # Задержка в 1 секунду

pygame.quit()


countdown_time = 10  # Время обратного отсчета в секундах
start_ticks = pygame.time.get_ticks()  # Получаем текущее время
seconds_passed = (pygame.time.get_ticks() - start_ticks) / 1000  # Переводим в секунды
remaining_time = countdown_time - seconds_passed  #оставшееся время
