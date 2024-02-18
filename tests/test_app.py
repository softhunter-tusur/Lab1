import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest

from app import app


class FlaskTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def tearDown(self):
        pass

    def test_index(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Добавление рамки и построение графика распределения цветов'.encode('utf-8'), response.data)

    def test_upload_image(self):
        with open('test_image.jpg', 'rb') as f:
            response = self.app.post('/', data={'image': (f, 'test_image.jpg'), 'border_size': 10},
                                     follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Result', response.data)
            self.assertIn(b'bordered_test_image.jpg', response.data)
            self.assertIn(b'color_distribution.png', response.data)


if __name__ == '__main__':
    unittest.main()
