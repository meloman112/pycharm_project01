from datetime import datetime
from ultralytics import YOLO
import cv2
import os
from ultralytics import YOLO
import time
from funcs import check, box
from random import randint

number = 0

# Load a model
model = YOLO('yolov8n-pose.pt')  # load a pretrained model (recommended for training)

# Учетные данные для доступа к каsмере
username = 'admin'
password = 'Babur2001'

camera_url = 'http://192.168.0.107:4747/video'

video_url = '4784598_Camden_High Street_Street_3840x2160.mp4'

# Инициализация видеопотока
cap = cv2.VideoCapture(camera_url)


# Создаем папку для сохранения скриншотов
os.makedirs('screenshots', exist_ok=True)

ids = dict()
# Проверка успешности подключения к камере
if not cap.isOpened():
    print("Не удалось подключиться к камере.")
else:
    # Отображение видеопотока
    while True:
        start_time = time.time()

        ret, frame = cap.read()
        if not ret:
            print("Не удалось получить кадр.")
            break

        frame = cv2.resize(frame, (1280, 720))

        # Ваши операции с каждым кадром (например, отображение)
        #cv2.imshow('Camera Feed', frame)
        results = model.track(source=frame, conf=0.6, persist=True)

        for result in results:
            keypoints_object = result.keypoints
            person_count = keypoints_object.shape[0]
            for i in range(person_count):
                if check(keypoints_object[i].xy):

                    ls, id = (box(result, i))
                    if ids.get(id):
                        if ids[id] > 10:
                            continue
                        ids[id] += 1
                    else:
                        ids[id] = 1
                    screenshot = frame[ls[1]:ls[3], ls[0]:ls[2]]
                    # Получаем текущее время
                    now = datetime.now()
                    filename = f'screenshots/{number}-{id}-{now.strftime("%Y-%m-%d_%H-%M-%S")}.jpg'
                    # Сохраняем скриншот
                    cv2.imwrite(filename, screenshot)
                    print(ids)
                    number += 1
        end_time = time.time()
        print(f'FPS: {1000//(1000*(end_time - start_time))}')
        # Прерывание цикла при нажатии клавиши 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Освобождение ресурсов
    cap.release()
    cv2.destroyAllWindows()