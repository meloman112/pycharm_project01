import os
import shutil
import requests

def archive_and_send(directory_path, url='https://face.cake-bumer.uz/api/upload-zip'):
    """
    Архивирует указанную папку и отправляет архив на сервер с помощью POST-запроса.

    :param directory_path: Путь к папке, которую нужно архивировать.
    :param url: URL сервера, на который будет отправлен архив.
    """
    # Проверка на пустоту папки
    if not os.listdir(directory_path):
        print("Папка пуста. Удаляю...")
        os.rmdir(directory_path)
        return

    # Получение родительского каталога и имени папки
    parent_dir = os.path.dirname(directory_path)
    directory_name = os.path.basename(directory_path)

    # Путь, где будет создан архив (без указания расширения .zip, т.к. make_archive его добавит)
    archive_path = os.path.join(parent_dir, directory_name)

    # Создание архива из папки
    archive_path = shutil.make_archive(archive_path, 'zip', parent_dir, directory_name)

    print(archive_path)

archive_and_send('screenshots/ID-85')