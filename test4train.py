from ultralytics import YOLO

model = YOLO(model='yolov8n-pose.pt')







# Export the model to TensorRT format
model.export(format='engine')  # creates 'yolov8n.engine'

# Load the exported TensorRT model
tensorrt_model = YOLO('yolov8n.engine')

results = tensorrt_model(source=0, show=True)