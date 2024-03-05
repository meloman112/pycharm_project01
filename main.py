import subprocess
import threading
import time

from camyolo2 import VideoProcessor
# Количество экземпляров скрипта, которое вы хотите запустить
num_instances = 7

# Список для хранения объектов процессов
processes = ['videos/D06_20240228081038.mp4', 'videos/D06_20240228084525.mp4', 'videos/D06_20240228091825.mp4', 'videos/D06_20240228095215.mp4', 'videos/D06_20240228140410.mp4', 'videos/D06_20240229083303.mp4']
def multiprocess_video(camera_url, group):
    print(camera_url, group)
    start_time = time.time()
    pr_video = VideoProcessor(camera_url=camera_url, group=group)
    pr_video.process_video()
    end_time = time.time()
    return end_time - start_time

times_processes = []
# Ожидаем завершения всех процессов
for indx, process in enumerate(processes):
    time = threading.Thread(target=multiprocess_video, args=(process, indx)).start()
    times_processes.append(time)
print(times_processes)



