import cv2
import numpy as np

# Load pre-trained CNN model for violence detection
# Replace 'path_to_model' with the path to your pre-trained model file
model = cv2.dnn.readNet('path_to_model', 'path_to_model_weights')

# Function to preprocess input frames for the model
def preprocess(frame):
    # Preprocess the frame (e.g., resize, normalize) based on the requirements of the model
    # Return the preprocessed frame
    return frame

# Function to detect violence in a frame
def detect_violence(frame):
    # Preprocess the frame
    preprocessed_frame = preprocess(frame)

    # Forward pass through the model to obtain predictions
    model.setInput(cv2.dnn.blobFromImage(preprocessed_frame, scalefactor=1.0, size=(300, 300), swapRB=True))
    detections = model.forward()

    # Process the detections to identify violence
    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence > 0.5:  # Adjust confidence threshold as needed
            class_id = int(detections[0, 0, i, 1])
            if class_id == 1:  # Assuming class 1 corresponds to violence (customize based on your model)
                return True
    
    return False

# Main function to process video frames and detect violence
def main():
    # Open video capture device (e.g., webcam)
    cap = cv2.VideoCapture(0)  # Change to 1 or 2 if you have multiple cameras

    while True:
        # Read a frame from the video stream
        ret, frame = cap.read()
        if not ret:
            break

        # Detect violence in the frame
        is_violence = detect_violence(frame)

        # Display result on the frame
        if is_violence:
            cv2.putText(frame, 'Violence Detected', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        else:
            cv2.putText(frame, 'No Violence', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        # Display the frame
        cv2.imshow('Violence Detection', frame)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the video capture device and close OpenCV windows
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
