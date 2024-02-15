import os
import shutil
import requests


def archive_and_send(directory_path, url):
    """
    Архивирует указанную папку и отправляет архив на сервер с помощью POST-запроса.

    :param directory_path: Путь к папке, которую нужно архивировать.
    :param url: URL сервера, на который будет отправлен архив.
    """
    # Получение имени папки
    archive_name = os.path.basename(directory_path)

    # Создание архива из папки
    archive_path = shutil.make_archive(archive_name, 'zip', directory_path)

    # Отправка архива на сервер
    with open(archive_path, 'rb') as f:
        files = {'zip_file': (archive_name + '.zip', f)}
        response = requests.post(url, files=files)

        # Проверка статуса ответа
        if response.status_code == 200:
            print("Архив успешно отправлен.")
            print(response.text)

            # Удаление архива и папки после успешной отправки
            os.remove(archive_path)
            shutil.rmtree(directory_path)
        else:
            print("Ошибка при отправке. Код ответа:", response.status_code)


archive_and_send('runs/pose/track', 'https://face.cake-bumer.uz/api/upload-zip')
