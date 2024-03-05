from datetime import datetime
import cv2
import os
from ultralytics import YOLO
import time
from funcs_update import check, box, canSaveImage, check_ids, send_zip
import threading
import torch

class VideoProcessor:
    def __init__(self, camera_url, group, model_path='yolov8n-pose.pt'):
        self.camera_url = camera_url
        self.model = YOLO("yolov8n-pose.engine")  # Предварительно загруженная модель
        self.users = []
        self.group = f'group-{group}_ID'
        self.ids_dict = {}

    def process_video(self):
        cap = cv2.VideoCapture(self.camera_url)
        if not cap.isOpened():
            print("Не удалось подключиться к камере.")
            return

        os.makedirs('screenshots', exist_ok=True)
        number = 0

        try:
            while True:
                start_time = time.time()
                ret, frame = cap.read()
                if not ret:
                    print("Не удалось получить кадр.")
                    break

                frame = cv2.resize(frame, (1280, 720))
                results = self.model.track(source=frame, conf=0.55, persist=True, show=True)
                self.handle_results(frame, results, number)
                number += 1

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

                print(f"Frame Processing Time: {(time.time() - start_time) * 1000} ms")
        finally:
            cap.release()

    def handle_results(self, frame, results, number):
        for result in results:
            keypoints_object = result.keypoints
            person_count = keypoints_object.shape[0]
            for i in range(person_count):
                if check(keypoints_object[i].xy):
                    ls, person_id = box(result, i)
                    if not ls:
                        continue
                    new_user = {'id': person_id, 'created_date': time.time()}
                    if canSaveImage(new_user, self.users):
                        self.users.append(new_user)
                        self.save_screenshot(frame, ls, person_id, number)

            if torch.is_tensor(result.boxes.id):
                ids = [int(a) for a in result.boxes.id.tolist()]
            else:
                ids = []
            no_active_ids, self.ids_dict = check_ids(ids, self.ids_dict)
            threading.Thread(target=send_zip, args=(no_active_ids,)).start()

    def save_screenshot(self, frame, ls, person_id, number):
        screenshot = frame[ls[1]:ls[3], ls[0]:ls[2]]
        now = datetime.now()
        filename = f'screenshots/group-2_ID-{person_id}/{number}_{now.strftime("%Y-%m-%d-%H-%M-%S")}.jpg'
        if screenshot.size > 0:
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            cv2.imwrite(filename, screenshot)
        else:
            print(f"Пустой скриншот для ID-{person_id}, не сохранено.")

if __name__ == "__main__":
    USERNAME = 'admin'
    PASSWORD = 'Babur2001'
    camera_url = f'rtsp://{USERNAME}:{PASSWORD}@192.168.0.119:554/Streaming/Channels/101'
    video_url = 'videos/D06_20240228084525.mp4'
    group = 1
    processor = VideoProcessor(camera_url=camera_url, group=group)
    while True:
        processor.process_video()
