# tests/test_example.py

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
        Тест проверяет доступность главной страницы и наличие на ней элементов интерфейса .
        """
        response = self.app.get('/')  # Получаем ответ от главной страницы
        self.assertEqual(response.status_code, 200)  # Проверяем, что ответ успешен (код 200)
        self.assertIn(b'Upload Image', response.data)  # Проверяем наличие элемента "Upload Image" в ответе

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
            self.assertIn(b'Bordered Image', response.data)  # Проверяем наличие "Bordered Image" в ответе
            self.assertIn(b'Color Distribution', response.data)  # Проверяем наличие "Color Distribution" в ответе


if __name__ == '__main__':
    unittest.main()  # Запускаем тесты при запуске файла напрямую
