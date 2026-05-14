import cv2
from ultralytics import YOLO

model = YOLO('C:/YOLOModels/crack_detection/best.pt')

cap = cv2.VideoCapture(0)

# Set resolution higher
cap.set(3, 1280)
cap.set(4, 720)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Run YOLO with lower confidence threshold
    results = model(frame, conf=0.25)

    annotated = results[0].plot()

    cv2.imshow("Crack Detection", annotated)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()