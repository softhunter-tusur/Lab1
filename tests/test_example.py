import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from app import app


class TestExample(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_index(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        # Проверяем наличие строки "Upload Image" в ответе от сервера
        self.assertIn('Upload Image', response.data.decode('utf-8'))

    def test_upload_image(self):
        # Предполагая, что файл test_image.jpg находится в папке tests
        image_path = os.path.join(os.path.dirname(__file__), 'test_image.jpg')
        with open(image_path, 'rb') as f:
            data = {
                'border_size': 10,
                'image': (f, 'test_image.jpg')
            }
            response = self.app.post('/', data=data, content_type='multipart/form-data')
            self.assertEqual(response.status_code, 200)
            self.assertIn('Bordered Image', response.data.decode('utf-8'))
            self.assertIn('Color Distribution', response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
