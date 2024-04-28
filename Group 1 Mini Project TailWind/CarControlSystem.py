import cv2
import serial
import tensorflow_hub as hub
import numpy as np

# Load TensorFlow Hub model
model = hub.load('https://tfhub.dev/tensorflow/ssd_mobilenet_v2/fpnlite_320x320/1')

# Set up the video capture
cap = cv2.VideoCapture(0)

# Set up serial communication
ser = serial.Serial('COM5', 9600)  # Update COM port as necessary

def detect_and_classify(frame):
    input_tensor = np.expand_dims(frame, 0)
    detector_output = model(input_tensor)
    class_ids = detector_output['detection_classes'][0].numpy().astype(int)
    scores = detector_output['detection_scores'][0].numpy()
    boxes = detector_output['detection_boxes'][0].numpy()
    return boxes, class_ids, scores

def get_sensor_data():
    if ser.in_waiting > 0:
        line = ser.readline().decode('utf-8').rstrip()
        if line and all(char.isdigit() or char == ',' for char in line):
            front_distance, rear_distance = map(int, line.split(','))
            return front_distance, rear_distance
    return None, None



def main():
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Failed to grab frame")
                break
            
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            boxes, classes, scores = detect_and_classify(frame_rgb)

            # Threshold for detection
            threshold = 0.5
            for score, cls in zip(scores, classes):
                if score > threshold:
                    if cls == 1:  # Assuming class 1=person
                        print("Detected pedestrian: Stopping the car.")
                        break
                    elif cls == 10:  # Assuming class 10=traffic light
                        print("Detected traffic signal: Taking appropriate action.")
                        # Add logic to interpret traffic signal color and take action
                        break

            front_distance, rear_distance = get_sensor_data()
            if front_distance is not None and front_distance < 50:
                print("Object detected within 50cm at front: Stopping the car.")
            if rear_distance is not None and rear_distance < 50:
                print("Object detected within 50cm at rear: Stopping the car.")

            # Display frame in a window
            cv2.imshow("Camera Recording", frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    finally:
        cap.release()
        cv2.destroyAllWindows()
        ser.close()

if __name__ == '__main__':
    main()

