from datetime import datetime
import cv2
import os
from ultralytics import YOLO
import time
from funcs import check, box, canSaveImage, check_ids, send_zip
import threading



number = 0

# Load a model
# model = YOLO('yolov8n-pose.torchscript')  # load a pretrained model (recommended for training)

username = 'admin'
password = 'Babur2001'

camera_url = f'rtsp://{username}:{password}@192.168.0.119:554/Streaming/Channels/101'

video_url = 'videos/2_Obama.mp4'

from ultralytics import SAM

# Load the model
model = SAM('mobile_sam.pt')

# Predict a segment based on a point prompt
model.predict(video_url, points=[900, 370], labels=[1], show=True)