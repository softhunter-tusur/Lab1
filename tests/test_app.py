import os
import unittest
from flask import Flask
from werkzeug.datastructures import FileStorage

class FlaskTestCase(unittest.TestCase):

    def setUp(self):
        # Создаем экземпляр приложения Flask для тестирования
        self.app = Flask(__name__)
        # Включаем режим тестирования
        self.app.config['TESTING'] = True

    def tearDown(self):
        pass

    def test_upload_image(self):
        # Определяем путь к тестовому изображению
        test_image_path = os.path.join(os.path.dirname(__file__), 'test_image.jpg')

        # Открываем файл с изображением
        with open(test_image_path, 'rb') as f:
            # Создаем объект FileStorage, представляющий загружаемый файл
            file_storage = FileStorage(f)

            # Отправляем POST-запрос на сервер с загружаемым файлом и другими данными
            with self.app.test_client() as client:
                response = client.post('/', data={'image': file_storage, 'border_size': 10},
                                       follow_redirects=True)

                # Проверяем код ответа
                self.assertEqual(response.status_code, 200)
                # Проверяем, что в ответе есть ожидаемый текст "Result"
                self.assertIn(b'Result', response.data)

if __name__ == '__main__':
    unittest.main()
