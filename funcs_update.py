import shutil

import requests
import os

def check(tensor):
    # Проверка наличия всех пяти ключевых точек
    return tensor.numel() != 0 and all(int(tensor[0][i][0]) != 0 for i in range(5))

def box(result, index):
    try:
        x1, y1 = map(int, result.keypoints[index].xy[0][4])
        x2, y2 = map(int, result.keypoints[index].xy[0][3])
        ls = [x1 - 10, y1 - (x2 - x1), x2 + 10, y2 + (x2 - x1)]
        person_id = int(result.boxes[index].id)
    except Exception as e:
        print(e)
        ls, person_id = [], 0
    return ls, person_id

def canSaveImage(new, array):
    user_imgs = [item for item in array if item['id'] == new['id']]
    if len(user_imgs) >= 10:
        return False
    if not user_imgs:
        return True
    return new['created_date'] - user_imgs[-1]['created_date'] >= 0.4





def send_zip(ids):
    for id in ids:
        print(f'Sending zip {id}')
        filename = f'screenshots/group-2_ID-{id}'
        archive_and_send(filename)

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
    parent_dir = os.path.dirname(directory_path)
    directory_name = os.path.basename(directory_path)
    archive_path = os.path.join(parent_dir, directory_name)

    if not os.path.isdir(directory_path) or not os.listdir(directory_path):
        print('Directory is empty or does not exist.')
        return
    archive_path = shutil.make_archive(archive_path, 'zip', parent_dir, directory_name)
    with open(archive_path, 'rb') as f:
        files = {'zip_file': (os.path.basename(archive_path), f)}
        response = requests.post(url, files=files)
        if response.status_code == 200:
            print("Archive successfully sent.")
            shutil.rmtree(directory_path, ignore_errors=True)
        else:
            print(f"Error sending archive. Status code: {response.status_code}")
#
#
# def archive_and_send(directory_path, photos_folder_name, url='https://face2.cake-bumer.uz/api/upload-zip'):
#     photos_path = os.path.join(directory_path, photos_folder_name)
#     if not os.path.isdir(photos_path) or not os.listdir(photos_path):
#         print('Photos directory is empty or does not exist.')
#         return
#
#     # Создаем архив, включая только папку с фотографиями
#     archive_path = shutil.make_archive(base_name=directory_path, format='zip', root_dir=directory_path, base_dir=photos_folder_name)
#
#     with open(archive_path, 'rb') as f:
#         files = {'zip_file': (os.path.basename(archive_path), f)}
#         response = requests.post(url, files=files)
#         if response.status_code == 200:
#             print("Archive successfully sent.")
#             # Возможно, вам не нужно удалять исходную папку после отправки
#             # shutil.rmtree(directory_path, ignore_errors=True)
#         else:
#             print(f"Error sending archive. Status code: {response.status_code}")