from flask import Flask, request, render_template
import os

app = Flask(__name__)

# Установим папку для загрузки файлов
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def clear_static_folder():
    for filename in os.listdir(app.config['UPLOAD_FOLDER']):
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        os.remove(file_path)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Проверяем, был ли отправлен файл
        if 'image' not in request.files:
            return render_template('index.html', error='No file part')

        file = request.files['image']

        # Проверяем, что файл не пустой
        if file.filename == '':
            return render_template('index.html', error='No selected file')

        # Сохраняем загруженный файл
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], 'test_image.jpg'))

        # Возвращаем результат обработки
        return render_template('result.html')

    return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True)
