import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest  # Импортируем модуль для создания тестовых кейсов
from app import app  # Импортируем экземпляр приложения Flask


class TestExample(unittest.TestCase):  # Создаем класс для тестирования

    def setUp(self):
        """
        Метод setUp вызывается перед выполнением каждого тестового кейса.
        Здесь мы настраиваем тестовое окружение.
        """
        self.app = app.test_client()  # Создаем клиент для тестирования приложения
        self.app.testing = True  # Устанавливаем флаг тестирования для приложения

    def tearDown(self):
        """
        Метод tearDown вызывается после выполнения каждого тестового кейса.
        Здесь мы можем провести очистку после выполнения теста, если это необходимо.
        """
        pass

    def test_index(self):
        """
        Тест проверяет доступность главной страницы и наличие на ней элементов интерфейса.
        """
        response = self.app.get('/')  # Получаем ответ от главной страницы
        self.assertEqual(response.status_code, 200)  # Проверяем, что ответ успешен (код 200)
        self.assertIn('Upload Image',
                      response.data.decode('utf-8'))  # Проверяем наличие элемента "Upload Image" в ответе

    def test_upload_image(self):
        """
        Тест проверяет корректную загрузку изображения на сервер.
        """
        with open('test_image.jpg', 'rb') as f:
            # Создаем данные для отправки POST-запроса с изображением
            data = {
                'border_size': 10,  # Размер рамки
                'image': (f, 'test_image.jpg')  # Изображение
            }
            # Отправляем POST-запрос на главную страницу с данными
            response = self.app.post('/', data=data, content_type='multipart/form-data')
            self.assertEqual(response.status_code, 200)  # Проверяем, что ответ успешен (код 200)
            self.assertIn('Bordered Image',
                          response.data.decode('utf-8'))  # Проверяем наличие "Bordered Image" в ответе
            self.assertIn('Color Distribution',
                          response.data.decode('utf-8'))  # Проверяем наличие "Color Distribution" в ответе


if __name__ == '__main__':
    unittest.main()  # Запускаем тесты при запуске файла напрямую
