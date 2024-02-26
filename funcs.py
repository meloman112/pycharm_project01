import random as rd
import shutil

import requests
import zipfile
import os

# функция проверияет 5 точек на лице если есть все возращает тру
# принимает keypoint каждого xy
def check(tensor):
    if tensor.numel() != 0:
        tensor = tensor[0]
        # print(tensor.shape)
        for i in range(5):
            if int(tensor[i][0]) == 0:
                return False
        return True
    else:
        return False


# принимает resoult.boxes и индекс каждого возращает бок ввиде списка
def box(result, index):
    x1, y1 = [int(a) for a in (result.keypoints[index].xy[0][4])]
    x2, y2 = [int(a) for a in (result.keypoints[index].xy[0][3])]
    x0, y0 = x1, y1 - x2 + x1
    x3, y3 = x2, y2 + x2 - x1
    ls = [x0-10, y0, x3+10, y3]
    #ls = [int(a) for a in (result.boxes[index].xyxy[0])]
    try:
        id = int(result.boxes[index].id)
    except Exception as e:
        print(e)
        id = 0
    return ls, id


def canSaveImage(new, array):
    userExists = False
    for i in range(len(array)-1, 0, -1):
        if array[i]['id'] == new['id']:
            countImgs = 0
            for item in array:
                if item['id'] == new['id']:
                    countImgs += 1
            if countImgs >= 25:
                return False
            userExists = True
            diffTime = new['created_date'] - array[i]['created_date']
            if diffTime >= 0.4:
                return True
            return False
    if not userExists: return True
    return True


def send_zip(ids):
    for id in ids:
        print(f' -----------------------------------------------------------------------------------Sending zip {ids} -----------------------------------------------------------------------------------')
        filename = f'screenshots/group-2_ID-{id}'
        #zip_path = f'zips/group-2_ID-{id}'
        archive_and_send(filename)



def zip_folder(folder_path, zip_path):
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(folder_path):
            for file in files:
                absolute_path = os.path.join(root, file)
                relative_path = os.path.relpath(absolute_path, folder_path)
                zipf.write(absolute_path, relative_path)
        os.rmdir(folder_path)
    return True


def check_ids(ids, ids_dict):
    new_dict = dict()
    no_active_ids = []
    for id in ids:
        new_dict[id] = 0
    for key, val in ids_dict.items():
        if key not in ids and val < 70:
            new_dict[key] = val+1
        elif val >= 70:
            no_active_ids.append(key)
    return no_active_ids, new_dict



def archive_and_send(directory_path, url='https://face2.cake-bumer.uz/api/upload-zip'):
    """
    Архивирует указанную папку и отправляет архив на сервер с помощью POST-запроса.

    :param directory_path: Путь к папке, которую нужно архивировать.
    :param url: URL сервера, на который будет отправлен архив.
    """
    if not os.path.exists(directory_path):
        print('--------------------------------------------not directory-------------------------------------------------------------------')
        return

    if not os.listdir(directory_path):
        print("Папка пуста. Удаляю...---------------------------------------------------delete---------------------------------------------------------------------------------------------------------")
        os.rmdir(directory_path)
        return

    # Получение родительского каталога и имени папки
    parent_dir = os.path.dirname(directory_path)
    directory_name = os.path.basename(directory_path)
    print('-----------------------------------------------------------------------------------------------1------------------------------------------------------------------------------------')

    # Путь, где будет создан архив (без указания расширения .zip, т.к. make_archive его добавит)
    archive_path = os.path.join(parent_dir, directory_name)

    # Создание архива из папки
    archive_path = shutil.make_archive(archive_path, 'zip', parent_dir, directory_name)
    print('-----------------------------------------------------------------------------------------------2------------------------------------------------------------------------------------')
    # Отправка архива на сервер
    with open(archive_path, 'rb') as f:
        files = {'zip_file': (os.path.basename(archive_path), f)}
        response = requests.post(url, files=files)

        # Проверка статуса ответа
        if response.status_code == 200:
            print("Архив успешно отправлен.------------------------------------------------------------------------------------------------------------------------------------------------------------")
            print(response.text)
            # Удаление архива и папки после успешной отправки
            #os.remove(archive_path)
            shutil.rmtree(directory_path)
        else:
            print("Ошибка при отправке. Код ответа:", response.status_code)
