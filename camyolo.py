from datetime import datetime
import cv2
import os
from ultralytics import YOLO
import time
from funcs import check, box, canSaveImage, check_ids, send_zip
import threading



number = 0

# Load a model
model = YOLO('yolov8n-pose.pt')  # load a pretrained model (recommended for training)

# Учетные данные для доступа к каsмере
username = 'admin'
password = 'Babur2001'

camera_url = f'rtsp://{username}:{password}@192.168.0.119:554/Streaming/Channels/101'

video_url = '4784598_Camden_High Street_Street_3840x2160.mp4'

# Инициализация видеопотока
cap = cv2.VideoCapture(camera_url)


# Создаем папку для сохранения скриншотов
os.makedirs('screenshots', exist_ok=True)
users =[]
ids_dict = dict()
# Проверка успешности подключения к камере
if not cap.isOpened():
    print("Не удалось подключиться к камере.")
else:
    # Отображение видеопотока
    while True:

        ret, frame = cap.read()
        if not ret:
            print("Не удалось получить кадр.")
            break

        frame = cv2.resize(frame, (1280, 720))

        # Ваши операции с каждым кадром (например, отображение)
        #cv2.imshow('Camera Feed', frame)
        results = model.track(source=frame, conf=0.5, persist=True)

        for result in results:
            keypoints_object = result.keypoints
            person_count = keypoints_object.shape[0]
            for i in range(person_count):
                if check(keypoints_object[i].xy):
                    ls, id = (box(result, i))
                    new = {'id': id, 'created_date': time.time()}
                    if canSaveImage(new, users):
                        users.append(new)
                    # if ids.get(id):
                    #     if ids[id] > 10:
                    #         continue
                    #     ids[id] += 1
                        screenshot = frame[ls[1]:ls[3], ls[0]:ls[2]]
                        # Получаем текущее время
                        now = datetime.now()
                        filename = f'screenshots/ID-{id}/{number}_{now.strftime("%Y-%m-%d-%H-%M-%S")}.jpg'
                        # Сохраняем скриншот
                        cv2.imwrite(filename, screenshot)
                        number += 1
                    else:

                        os.makedirs(f'screenshots/ID-{id}', exist_ok=True)
            ids = [int(a) for a in (result.boxes.id)]
            no_active_ids, ids_dict = check_ids(ids, ids_dict)
            # тут я хочу не дожидаться выполнения функции
            thread = threading.Thread(target=send_zip, args=(no_active_ids,))
            thread.start()
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()