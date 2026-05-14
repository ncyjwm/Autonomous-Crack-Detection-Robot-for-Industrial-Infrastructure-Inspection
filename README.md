# Autonomous Crack Detection Robot for Industrial Infrastructure Inspection

**TTTC3413 — Robot Applications**  
Universiti Kebangsaan Malaysia — Fakulti Teknologi dan Sains Maklumat  
Lecturer: Dr. Anahita Ghazvini

| No. | Name | Matric Number |
|-----|------|---------------|
| 1 | Nancy Anne | A202459 |
| 2 | Kavi Priya A/P Balasupramaniam | A202660 |

---

## Project Overview

Traditional crack inspection of pavements and industrial surfaces relies on manual visual examination by human inspectors, a method that is slow, inconsistent and hazardous. Inspectors frequently work in dangerous environments including active industrial zones, high-traffic roads and unstable floors, where environmental factors such as poor lighting and uneven surfaces further reduce detection accuracy.

This project addresses those limitations by developing a fully autonomous crack detection system that integrates deep learning, mobile robotics and simulation-based validation. The core components are:

- A YOLOv8 model trained on the UAPD Pavement Distress Dataset, capable of detecting longitudinal cracks with high precision and recall
- A real-time webcam-based inference pipeline deployed through Anaconda
- A Gazebo simulation environment featuring cracked pavement surfaces and the TurtleBot3 Waffle Pi
- A ROS 1 Noetic integration layer that connects camera perception, YOLOv8 inference and autonomous robot navigation into a unified pipeline

The system eliminates the need for continuous human involvement during inspection, reduces safety risks and provides consistent and repeatable detection results suitable for industrial deployment.

---

## Repository Structure

```
project-root/
|
|-- CrackDetection.ipynb          # Google Colab training notebook
|                                 # (data prep, XML-to-TXT conversion,
|                                 #  YOLOv8 training and evaluation)
|
|-- crackdetection.py             # ROS 1 YOLOv8 node
|                                 # (subscribes to camera topic,
|                                 #  runs inference and publishes results)
|
|-- webcam.py                     # Standalone real-time webcam detector
|                                 # (Anaconda environment, no ROS required)
|
|-- crack-detection.zip           # Trained model weights and dataset config
|   |-- best.pt                   # YOLOv8 trained weights
|   |-- data.yaml                 # Dataset class definitions and paths
|   `-- ...
|
`-- turtle_crack_ws.zip           # Complete ROS catkin workspace
    |-- build/                    # CMake build artifacts
    |-- devel/                    # Devel space (source setup.bash from here)
    |-- .catkin_workspace         # Catkin workspace marker
    `-- src/
        |-- crack_detection/      # Main ROS package
        |   |-- CMakeLists.txt
        |   |-- package.xml
        |   |-- launch/
        |   |   `-- crack_detection.launch
        |   |-- scripts/
        |   |   `-- crackdetection.py
        |   `-- models/
        |       `-- best.pt
        `-- CMakeLists.txt
```

---

## Prerequisites

### Operating System and Middleware

| Component | Version |
|-----------|---------|
| Ubuntu | 20.04 LTS |
| ROS | Noetic Ninjemys |
| Gazebo | 11 |
| Python | 3.8 or higher |

### Python Packages

| Package | Purpose |
|---------|---------|
| ultralytics | YOLOv8 model loading and inference |
| opencv-python | Image capture and frame annotation |
| torch / torchvision | Deep learning backend |
| rospy | ROS Python client library |
| numpy | Numerical operations |

### ROS Packages

```
ros-noetic-turtlebot3
ros-noetic-turtlebot3-simulations
ros-noetic-turtlebot3-gazebo
ros-noetic-rqt-image-view
python3-catkin-tools
```

---

## Installation

### Step 1 — Clone or Extract the Project

If using the zip archives directly:

```bash
unzip turtle_crack_ws.zip -d ~/
cd ~/turtle_crack_ws
```

If cloning from a repository:

```bash
git clone <repository-url> ~/turtle_crack_ws
cd ~/turtle_crack_ws
```

### Step 2 — Install ROS and TurtleBot3 Packages

```bash
sudo apt update
sudo apt install ros-noetic-turtlebot3 \
                 ros-noetic-turtlebot3-simulations \
                 ros-noetic-turtlebot3-gazebo \
                 ros-noetic-rqt-image-view \
                 python3-rosdep \
                 python3-catkin-tools
```

### Step 3 — Install Python Dependencies

```bash
pip install ultralytics opencv-python numpy torch torchvision
```

For the Anaconda environment used in webcam testing:

```bash
conda create -n crackdetect python=3.9
conda activate crackdetect
pip install ultralytics opencv-python numpy
```

### Step 4 — Extract Model Weights

```bash
unzip crack-detection.zip -d ~/crack-detection
```

Note the path to `best.pt` and update it in `crackdetection.py` and `webcam.py` if needed.

### Step 5 — Build the ROS Workspace

```bash
cd ~/turtle_crack_ws
catkin_make
source devel/setup.bash
```

Persist the environment setup in your shell profile:

```bash
echo "source ~/turtle_crack_ws/devel/setup.bash" >> ~/.bashrc
source ~/.bashrc
```

### Step 6 — Set the TurtleBot3 Model

```bash
echo "export TURTLEBOT3_MODEL=waffle_pi" >> ~/.bashrc
source ~/.bashrc
```

---

## Dataset

The model was trained on the **UAPD Pavement Distress Dataset**, a publicly available collection of labelled pavement crack images.

| Split | Images | Proportion |
|-------|--------|------------|
| Training | 820 | 80% |
| Validation | 205 | 20% |
| Total (cleaned) | 1025 | 100% |

The original dataset contained 3151 images. After removing corrupted or unsuitable samples the usable set was reduced to 1025 images. The dataset was then split with an 80:20 ratio and organised into separate folders for images, annotations and labels.

Original annotations were provided in Pascal VOC XML format. Because YOLOv8 requires TXT-format labels with normalised bounding box coordinates, a conversion script was written to automatically transform all XML files into YOLOv8-compatible TXT labels containing class ID and normalised x-center, y-center, width and height values.

Dataset source: https://github.com/tantantetetao/UAPD-Pavement-Distress-Dataset

---

## Model Training

Training was conducted in **Google Colab** using the `CrackDetection.ipynb` notebook with GPU acceleration. The model was initialised from pretrained YOLOv8s weights via transfer learning and fine-tuned on the crack dataset.

### Training Configuration

| Hyperparameter | Value |
|----------------|-------|
| Base model | YOLOv8s (pretrained on COCO) |
| Epochs | 50 |
| Image size | 512 x 512 |
| Batch size | 8 |
| Optimiser | AdamW (default) |

### Training Script (Colab)

```python
from ultralytics import YOLO

model = YOLO('yolov8s.pt')

model.train(
    data='/content/drive/MyDrive/crack-detection/data.yaml',
    epochs=50,
    imgsz=512,
    batch=8,
    project='/content/drive/MyDrive/crack-detection/crack_detection',
    name='yolov8_crack',
    exist_ok=True
)
```

### Performance Results

| Metric | Value |
|--------|-------|
| Precision at confidence 0.82 | 100% |
| Recall (true positive rate) | 80% |
| Detection confidence range (live) | 0.70 to 0.81 |

The model reaches 100% precision for all crack classes when the confidence threshold is set above approximately 0.82, confirming minimal false positives at high certainty levels. The normalised confusion matrix shows an 80% recall rate, demonstrating strong sensitivity to true crack instances which is critical for infrastructure inspection applications.

---

## Real-Time Detection via Webcam

The `webcam.py` script deploys the trained `best.pt` model for standalone real-time crack detection using a standard webcam, without requiring ROS.

### Running the Webcam Detector

Activate the Anaconda environment and run:

```bash
conda activate crackdetect
python webcam.py
```

### Script Overview

```python
import cv2
from ultralytics import YOLO

# Load the trained YOLOv8 model
model = YOLO('C:/YOLOModels/crack_detection_test/best.pt')

# Open webcam
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame")
        break

    # Run detection
    results = model(frame)

    # Annotate frame
    annotated_frame = results[0].plot()

    # Show webcam window
    cv2.imshow("Crack Detection", annotated_frame)

    # Press 'q' to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
```

Update the model path to match the location of `best.pt` on your machine. Press `q` to exit the detection window.

Live testing confirmed longitudinal crack detection with confidence scores between 0.70 and 0.75 across varying real-world lighting conditions and camera angles.

---

## ROS and Gazebo Simulation

### Launching the Gazebo World

Open a terminal and launch the custom cracked pavement simulation environment:

```bash
source ~/turtle_crack_ws/devel/setup.bash
roslaunch turtlebot3_gazebo turtlebot3_world.launch
```

The simulation world features a textured road surface with embedded crack textures, environmental obstacles including a tree and a cube and a TurtleBot3 Waffle Pi model. This setup enables safe and repeatable validation of both navigation and crack detection before any physical deployment.

### Running the YOLOv8 ROS Detection Node

In a second terminal:

```bash
source ~/turtle_crack_ws/devel/setup.bash
rosrun crack_detection crackdetection.py
```

The node subscribes to `/camera/rgb/image_raw`, runs YOLOv8 inference on each incoming frame and publishes annotated output to `/camera/yolo_image`.

### Viewing the Detection Output

In a third terminal:

```bash
rosrun rqt_image_view rqt_image_view /camera/yolo_image
```

### Controlling the Robot

Use the TurtleBot3 keyboard teleop to navigate the robot through the inspection environment:

```bash
rosrun turtlebot3_teleop turtlebot3_teleop_key
```

### Alternatively — Use the Launch File

```bash
source ~/turtle_crack_ws/devel/setup.bash
roslaunch crack_detection crack_detection.launch
```

### ROS Topics

| Topic | Message Type | Description |
|-------|-------------|-------------|
| `/camera/rgb/image_raw` | `sensor_msgs/Image` | Raw camera feed from TurtleBot3 |
| `/camera/yolo_image` | `sensor_msgs/Image` | Annotated feed with bounding boxes |
| `/cmd_vel` | `geometry_msgs/Twist` | Robot velocity commands |

---

## Results

The complete system was validated across three environments.

**Google Colab Training** — The YOLOv8 model trained for 50 epochs achieved 100% precision at a confidence threshold above 0.82 and an 80% recall rate across the validation set. Training batch samples showed the model generalising across diverse pavement conditions including road markings and vegetation.

**Anaconda Webcam Testing** — Live webcam inference confirmed robust detection of longitudinal cracks with confidence scores ranging from 0.70 to 0.75 across varying real-world lighting conditions and camera angles.

**ROS and Gazebo Simulation** — The TurtleBot3 Waffle Pi successfully navigated the simulated inspection environment while the YOLOv8 node detected and labelled pavement cracks in real time, reaching a peak detection confidence of 0.81. Annotated detections were saved to the `/detections` folder and streamed live via `rqt_image_view`.

---

## Authors

| Name | Matric Number |
|------|---------------|
| Nancy Anne | A202459 |
| Kavi Priya A/P Balasupramaniam | A202660 |

Course: TTTC3413 — Robot Applications  
Lecturer: Dr. Anahita Ghazvini  
Institution: Universiti Kebangsaan Malaysia (UKM)

---

## References

Fan, Z., W., Y. and Lu, Z. 2022. Deep learning-based crack detection for industrial surfaces. *IEEE Access* 10. https://ieeexplore.ieee.org/document/9936270

Huang, Y., L., J. and Kim, H. 2022. Autonomous mobile robot inspection system using ROS2 and deep learning. *Robotics and Autonomous Systems*. https://doi.org/10.1016/j.robot.2022.104278

Kaveh, H. and A., R. 2024. Recent advances in crack detection technologies for structures: a survey of 2022-2023 literature. *Frontiers in Built Environment* 10. https://doi.org/10.3389/fbuil.2024.1321634

Liu, Y. et al. 2023. A rapid bridge crack detection method based on deep learning. *Applied Sciences* 13(17). https://doi.org/10.3390/app13179878

Nguyen, S., D., T., T.S., Le, V.P. and Piran, M.J. 2022. Deep learning-based crack detection: a survey. *International Journal of Pavement Research and Technology*. https://doi.org/10.1007/s42947-022-00172-z

UAPD Pavement Distress Dataset. n.d. Dataset repository for pavement crack images. GitHub. https://github.com/tantantetetao/UAPD-Pavement-Distress-Dataset

Zhang, J., S., S., Song, W., Li, Y. and Teng, Q. 2024. A novel convolutional neural network for enhancing the continuity of pavement crack detection (CPCDNet). *Scientific Reports* 14. https://www.nature.com/articles/s41598-024-81119-1

Zhang, J., X., H., Li, P., Zhang, K., Hong, W. and Guo, R. 2024. A pavement crack detection method via deep learning and a binocular-vision-based unmanned aerial vehicle. *Applied Sciences* 14(5): 1778. https://doi.org/10.3390/app14051778

Zhang, Q., C., S., Wu, Y., Ji, Z., Yan, F. and Huang, S. 2024. Improved U-net network asphalt pavement crack detection method. *PLoS ONE*. https://doi.org/10.1371/journal.pone.0300679
