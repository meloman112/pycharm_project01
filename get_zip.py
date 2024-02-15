import requests
import zipfile
import io

def download_and_extract_zip(url, extract_to='extracted_folder'):
    """
    Скачивает ZIP-файл по указанному URL и разархивирует его в указанную директорию.

    :param url: URL ZIP-файла для скачивания.
    :param extract_to: Путь к директории, куда будет извлечено содержимое архива.
    """
    # Скачивание файла
    response = requests.get(url)
    if response.status_code == 200:
        # Открытие ZIP-файла непосредственно из памяти, без сохранения на диск
        zip_file = zipfile.ZipFile(io.BytesIO(response.content))
        # Разархивация
        zip_file.extractall(extract_to)
        print(f"Архив успешно скачан и извлечен в {extract_to}.")
    else:
        print(f"Ошибка при скачивании файла. Код ответа: {response.status_code}")

download_and_extract_zip('https://face.cake-bumer.uz/api/get_zip', extract_to='runs/pose/track')