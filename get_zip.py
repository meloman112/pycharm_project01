

url = 'https://face.cake-bumer.uz/api/get-zip'

import requests
from io import BytesIO
import zipfile

# URL ZIP-файла

# Отправка GET-запроса
response = requests.get(url)

# Проверка на успешный ответ
if response.status_code == 200:
    # Открытие полученного ZIP-файла в памяти
    zip_file = zipfile.ZipFile(BytesIO(response.content))

    # Извлечение содержимого ZIP-файла в директорию
    zip_file.extractall(path='zips/')  # Укажите свой путь для извлечения
    print("Файл успешно сохранён и извлечён.")
else:
    print("Ошибка при загрузке файла. Код ответа:", response.status_code)
