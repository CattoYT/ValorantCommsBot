import ultralytics
import numpy as np
from detectors import capture_screenshot
from PIL import Image
import cv2


def overlayCensor(img):
    img_np = np.array(img)
    height, width, _ = img_np.shape
    box_coords = (width - 70, 93, width - 30, 400)  # (x_min, y_min, x_max, y_max)

    # Set the specified area to black
    img_np[box_coords[1]:box_coords[3], box_coords[0]:box_coords[2]] = [0, 0, 0]

    return img_np


def yoloV8Detection():
    import logging
    import os
    modelPath = "keremberke.pt"
    model = ultralytics.YOLO(modelPath)

    # converts the model to engine if it isn't already

    if modelPath[-2:] == "pt":
        try:

            model = ultralytics.YOLO(modelPath[:-3] + ".engine")
            pass
        except:
            if input("Do you want to convert this model to "
                     "TensorRT for faster inference? (y/n): ").lower() == "y": # btw this might not actually be faster :3
                model.export(dynamic=True, format="engine", simplify=True)
                os.remove(modelPath[:-3] + ".onnx")
                model = ultralytics.YOLO(modelPath[:-3] + ".engine")
    cooldown = 0

    # logging.getLogger('ultralytics').setLevel(logging.WARNING)
    while True:
        screenshot = capture_screenshot()
        img = overlayCensor(screenshot)
        results = model(img, conf=0.70, device="0")

        # Convert PIL image to OpenCV format

        img_cv2 = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        detections = results[0].boxes
        class_ids = detections.cls.cpu().numpy() if detections.cls is not None else []  # thanks copilot
        detected = 0
        for i, class_id in enumerate(class_ids):
            print(class_id)
            if class_id == 1.0:  # check if the class id is actually an enemy
                detected += 1
                # Get bounding box coordinates
            x_min, y_min, x_max, y_max = detections.xyxy[i].cpu().numpy()
            # Draw bounding box on the image
            cv2.rectangle(img_cv2, (int(x_min), int(y_min)), (int(x_max), int(y_max)), (0, 255, 0), 2)
            cv2.putText(img_cv2, f'Class: {int(class_id)}', (int(x_min), int(y_min) - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

        # class id 1 is enemy
        # class id 3 is ally i think

        print(f"Detected {detected} enemies")

        # Display the image with bounding boxes
        cv2.imshow("YOLOv8 Detection", img_cv2)

        # Break the loop if the user presses 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()

yoloV8Detection()
