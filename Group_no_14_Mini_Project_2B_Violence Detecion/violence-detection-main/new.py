import cv2

# Initialize video capture
cap = cv2.VideoCapture(0)

# Initialize background subtractor
fgbg = cv2.createBackgroundSubtractorMOG2()

while cap.isOpened():
    # Read frame from camera
    ret, frame = cap.read()
    if not ret:
        break

    # Apply background subtraction
    fgmask = fgbg.apply(frame)

    # Find contours
    contours, _ = cv2.findContours(fgmask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Filter contours based on area
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > 1000:  # Adjust the threshold based on your environment
            # Draw rectangle around the detected region
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # Display the frame
    cv2.imshow('Punch Detection', frame)

    # Break the loop if 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture object
cap.release()
cv2.destroyAllWindows()
