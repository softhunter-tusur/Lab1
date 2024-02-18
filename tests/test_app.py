import unittest
from app import app  #  имя вашего приложения или модуля

class FlaskTest(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def tearDown(self):
        pass

    def test_result(self):
        tester = app.test_client(self)
        with open('tests/test_image.jpg', 'rb') as img_file:
            response = tester.post('/', data={'image': img_file}, follow_redirects=True)
            # Проверяем, что в ответе есть ожидаемый текст
            self.assertIn('Добавление рамки и построение графика распределения цветов', response.data.decode('utf-8'))

if __name__ == '__main__':
    unittest.main()
