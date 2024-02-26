from datetime import datetime
import cv2
import os
from ultralytics import YOLO
import time
from funcs import check, box, canSaveImage, check_ids, send_zip
import threading



number = 0

# Load a model
model = YOLO('yolov8n-pose.torchscript')  # load a pretrained model (recommended for training)

username = 'admin'
password = 'Babur2001'

camera_url = f'rtsp://{username}:{password}@192.168.0.119:554/Streaming/Channels/101'

video_url = 'videos/2_Obama.mp4'

# Инициализация видеопотока
cap = cv2.VideoCapture(video_url)


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
        results = model.track(source=frame, conf=0.5, persist=True, show=True)

        for result in results:
            check_person = False
            keypoints_object = result.keypoints
            person_count = keypoints_object.shape[0]
            for i in range(person_count):
                if check(keypoints_object[i].xy):
                    check_person = True
                    ls, id = (box(result, i))
                    new = {'id': id, 'created_date': time.time()}
                    if canSaveImage(new, users):
                        users.append(new)

                        screenshot = frame[ls[1]:ls[3], ls[0]:ls[2]]
                        now = datetime.now()
                        filename = f'screenshots/ID-{id}/{number}_{now.strftime("%Y-%m-%d-%H-%M-%S")}.jpg'
                        if screenshot.size > 0:
                            directory = os.path.dirname(filename)
                            if not os.path.exists(directory):
                                os.makedirs(directory, exist_ok=True)
                            cv2.imwrite(filename, screenshot)
                        else:
                            print(f"Пустой скриншот для ID-{id}, не сохранено.")

                        #cv2.imwrite(filename, screenshot)
                        number += 1
                    else:

                        os.makedirs(f'screenshots/ID-{id}', exist_ok=True)
            if check_person:
                ids = [int(a) for a in (result.boxes.id)]
                no_active_ids, ids_dict = check_ids(ids, ids_dict)
                thread = threading.Thread(target=send_zip, args=(no_active_ids,))
                thread.start()
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()