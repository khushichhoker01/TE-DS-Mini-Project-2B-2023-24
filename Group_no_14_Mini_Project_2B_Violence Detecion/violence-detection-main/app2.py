import os
import tempfile
import cv2
import numpy as np
import streamlit as st
from PIL import Image

@st.cache(allow_output_mutation=True)
def get_predictor_model():
    from model2 import Model
    model = Model()
    return model

header = st.container()
model2 = get_predictor_model()

with header:
    st.title('Hello!')
    st.text('Using this app you can classify whether there is a fight on a street, fire, car crash, or everything is okay.')

uploaded_file = st.file_uploader("Or choose an image or video...", type=["jpg", "png", "jpeg", "mp4","avi"])
if uploaded_file is not None:
    # Save the uploaded file to a temporary file
    temp_file = tempfile.NamedTemporaryFile(delete=False)
    temp_file.write(uploaded_file.read())
    temp_file.close()

    # Open the temporary file with OpenCV
    video = cv2.VideoCapture(temp_file.name)

    # Read and display the video frames
    while True:
        ret, frame = video.read()
        if not ret:
            break
        st.image(frame, channels="BGR")

    # Release the video capture object
    video.release()

    # Clean up the temporary file
    os.unlink(temp_file.name)
    #  temp_file = tempfile.NamedTemporaryFile(delete=False)
    #  temp_file.write(uploaded_file.read())
    #  temp_file.close()

    # # Open the temporary file with OpenCV
    #  video = cv2.VideoCapture(temp_file.name)

    # # Read and display the video frames
    #  while True:
    #     ret, frame = video.read()
    #     if not ret:
    #         break
    #     st.image(frame, channels="BGR")

    # # Clean up the temporary file
    #     os.unlink(temp_file.name)
    # file_type = uploaded_file.name.split('.')[-1].lower()
    # file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    # frame = cv2.imdecode(file_bytes, 1)
    # st.image(frame, channels="BGR")
    # if file_type in ['jpg', 'jpeg', 'png']:
    #     image = Image.open(uploaded_file).convert('RGB')
    #     image = np.array(image)
    #     label_text = model2.predict(image=image)['label'].title()
    #     st.write(f'Predicted label is: **{label_text}**')
    #     st.write('Original Image')
    #     st.image(image, use_column_width=True)
    # elif file_type == 'mp4':
    #     video = cv2.VideoCapture(uploaded_file)
    #     while video.isOpened():
    #         ret, frame = video.read()
           
