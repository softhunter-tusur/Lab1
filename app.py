# Импорт необходимых модулей
import cv2  # OpenCV - библиотека компьютерного зрения
import matplotlib.pyplot as plt  # Matplotlib - библиотека для визуализации данных
import numpy as np  # NumPy - библиотека для работы с массивами и математическими функциями
import seaborn as sns  # Seaborn - библиотека для визуализации статистических данных
from flask import Flask, render_template, request, redirect, flash  # Flask - фреймворк для веб-приложений на Python
from flask_wtf import FlaskForm, RecaptchaField  # Flask-WTF - расширение Flask для работы с формами
from wtforms import IntegerField, SubmitField  # WTForms - библиотека для создания веб-форм
from wtforms.validators import InputRequired, DataRequired  # Валидаторы для полей форм
from flask_wtf.file import FileField, FileAllowed  # Дополнение Flask-WTF для работы с файлами
from werkzeug.utils import secure_filename  # Извлечение безопасных имен файлов
from PIL import Image  # PIL - библиотека Python для работы с изображениями
import os  # Модуль для взаимодействия с операционной системой
import secrets  # Модуль для генерации безопасных случайных чисел и строк
import io  # Модуль для работы с потоками ввода-вывода
import shutil  # Модуль для работы с файлами и директориями

# Папка для загрузки изображений и разрешенные расширения файлов
UPLOAD_FOLDER = 'static'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Создание объекта Flask
app = Flask(__name__)

# Настройка секретного ключа и ключей Recaptcha
app.config['SECRET_KEY'] = secrets.token_hex(16)
app.config['RECAPTCHA_PUBLIC_KEY'] = '6LeelGopAAAAAO7cCVJR31xIO88iaa93naux2wt5'
app.config['RECAPTCHA_PRIVATE_KEY'] = '6LeelGopAAAAAADUupO0W_rfz6ETYCQ9qsqEKN2O'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# Определение формы для загрузки изображения
class ImageForm(FlaskForm):
    border_size = IntegerField('Введите размер рамки в пикселях', validators=[InputRequired()])
    image = FileField('Выберите изображение', validators=[DataRequired(), FileAllowed(['jpg', 'png'], 'Images only!')])
    recaptcha = RecaptchaField()
    submit = SubmitField('Отправить')


# Функция для проверки разрешенных расширений файлов
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# Функция для очистки папки static перед обработкой запроса на загрузку изображения
def clear_static_folder():
    for filename in os.listdir(app.config['UPLOAD_FOLDER']):
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(e)


# Функция для добавления рамки к изображению с использованием библиотеки PIL
def add_border_pil(image_path, border_size, border_color):
    pil_image = Image.open(image_path)
    bordered_image = Image.new("RGB", (pil_image.width + 2 * border_size, pil_image.height + 2 * border_size),
                               border_color)
    bordered_image.paste(pil_image, (border_size, border_size))
    bordered_image_np = np.array(bordered_image)
    return bordered_image_np


# Функция для построения и сохранения графика распределения цветов
def plot_color_distribution(image_path):
    image_bgr = cv2.imread(image_path)
    image_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)

    height, width, _ = image_rgb.shape
    pixels = image_rgb.reshape((height * width, 3))
    intensities = np.sum(pixels, axis=1)

    sns.kdeplot(data=intensities, fill=True, color='skyblue')
    plt.xlabel('Интенсивность цветов')
    plt.ylabel('Плотность')

    # Создаем буфер для сохранения графика
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)

    # Очистка текущего графика из памяти
    plt.clf()

    return buffer.getvalue()


# Маршрут для загрузки изображения и отображения результатов
@app.route('/', methods=['GET', 'POST'])
def index():
    form = ImageForm()

    # Очистка папки static перед обработкой запроса на загрузку изображения
    clear_static_folder()

    if form.validate_on_submit():
        if 'image' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['image']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(image_path)
            bordered_image = add_border_pil(image_path, form.border_size.data, (64, 64, 64))
            bordered_image_filename = 'bordered_' + filename
            bordered_image_path = os.path.join(app.config['UPLOAD_FOLDER'], bordered_image_filename)
            Image.fromarray(bordered_image).save(bordered_image_path)

            # Построение и сохранение графика распределения цветов
            color_distribution_data = plot_color_distribution(image_path)
            color_distribution_filename = 'color_distribution.png'
            color_distribution_path = os.path.join(app.config['UPLOAD_FOLDER'], color_distribution_filename)
            with open(color_distribution_path, 'wb') as f:
                f.write(color_distribution_data)

            return render_template('result.html', bordered_filename=bordered_image_filename,
                                   color_distribution_filename=color_distribution_filename)

    return render_template('index.html', form=form)


# Запуск приложения Flask
if __name__ == '__main__':
    app.run(debug=True)
