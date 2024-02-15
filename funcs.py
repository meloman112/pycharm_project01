import random as rd
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
    id = int(result.boxes[index].id)
    return ls, id


def canSaveImage(new, array):
    userExists = False
    for i in range(len(array)-1, 0, -1):
        if array[i]['id'] == new['id']:
            countImgs = 0
            for item in array:
                if item['id'] == new['id']:
                    countImgs += 1
            if countImgs >= 10:
                return False
            userExists = True
            diffTime = new['created_date'] - array[i]['created_date']
            if diffTime >= 1:
                return True
            return False
    if not userExists: return True
    return True


def send_zip(ids):
    for id in ids:
        filename = f'screenshots/ID-{id}'
        zip_path = f'zips/ID-{id}'
        if os.path.exists(filename) and len(os.listdir(filename)) > 0:
            zip_folder(filename, zip_path)
            url = 'https://face.cake-bumer.uz/api/upload-zip'  # Замените на URL вашего сервера
            file_path = zip_path  # Укажите путь к файлу, который хотите отправить
            with open(file_path, 'rb') as file:
                files = {'zip_file': file}
                response = requests.post(url, files=files)
            print(response.text)  # Выводим ответ сервера




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

