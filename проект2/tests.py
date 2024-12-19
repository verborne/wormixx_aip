import pygame
import unittest
from unittest import mock
from main import Button


class TestButton(unittest.TestCase):
    def setUp(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1280, 720))
        self.image = pygame.Surface((100, 50))  # Создаем временное изображение для кнопки
        self.button = Button(100, 100, self.image, 1)

    def tearDown(self):
        pygame.quit()

    # Тестирование конструктора __init__
    def test_button_initialization(self):
        # Положительный тест 1
        self.assertEqual(self.button.rect.topleft, (100, 100))  # Проверка позиции кнопки
        self.assertFalse(self.button.clicked)

        # Положительный тест 2
        self.assertEqual(self.button.image.get_size(), (100, 50))  # Проверка размера кнопки

    def test_button_initialization_negative(self):
        # Отрицательный тест
        with self.assertRaises(TypeError):
            Button(100, 100, "not an image", 1)  # Передача неверного типа изображения

    # Тестирование метода draw
    def test_button_draw(self):
        # Положительный тест 1
        with mock.patch('pygame.mouse.get_pos', return_value=(150, 120)), \
                mock.patch('pygame.mouse.get_pressed', return_value=(1, 0, 0)), \
                mock.patch('pygame.display.update') as mock_update:
            result = self.button.draw(self.screen)
            self.assertTrue(result)
            self.assertTrue(self.button.clicked)  # Проверяем, что кнопка теперь считается нажатой

        # Положительный тест 2
        with mock.patch('pygame.mouse.get_pos', return_value=(150, 120)), \
                mock.patch('pygame.mouse.get_pressed', return_value=(0, 0, 0)):
            result = self.button.draw(self.screen)
            self.assertFalse(result)  # Проверяем, что кнопка не была нажата

    def test_button_draw_negative(self):
        # Отрицательный тест
        with mock.patch('pygame.mouse.get_pos', return_value=(150, 120)), \
                mock.patch('pygame.mouse.get_pressed', return_value=(1, 0, 0)):
            # Вызываем draw несколько раз, чтобы убедиться, что состояние кнопки не изменится
            self.button.draw(self.screen)

            # Убедимся, что кнопку нельзя нажать ещё раз
            self.button.clicked = True
            result = self.button.draw(self.screen)
            self.assertFalse(result)


if __name__ == '__main__':
    unittest.main()