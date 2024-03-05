import cv2
import datetime


def record_video(camera_url, duration_in_minutes=10, save_path='video.avi'):
    # Захват видео с первой подключенной камеры
    cap = cv2.VideoCapture(camera_url)

    # Определение кодека и создание объекта VideoWriter
    fourcc = cv2.VideoWriter.fourcc(*'XVID')
    out = cv2.VideoWriter(save_path, fourcc, 20.0, (1280, 720))

    start_time = datetime.datetime.now()
    while True:
        ret, frame = cap.read()
        if ret:
            out.write(frame)
            #cv2.imshow('frame', frame)

            # Закрыть окно по нажатию 'q'
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

            # Остановить запись после заданной длительности
            if (datetime.datetime.now() - start_time).seconds > duration_in_minutes * 60:
                break
        else:
            break

    # Освобождение захвата и закрытие окон
    cap.release()
    out.release()
    cv2.destroyAllWindows()
if __name__ == '__main__':

    USERNAME = 'admin'
    PASSWORD = 'Babur2001'
    camera_url = f'rtsp://{USERNAME}:{PASSWORD}@192.168.0.119:554/Streaming/Channels/101'

    record_video(camera_url, 1, 'output_video_h264.avi')
