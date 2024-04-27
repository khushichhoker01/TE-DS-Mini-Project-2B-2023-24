import streamlit as st
import cv2
from PIL import Image
import numpy as np
import torch
import yaml
import clip
import matplotlib.pyplot as plt


class Model:
    def _init_(self, settings_path: str = './settings.yaml'):
        with open(settings_path, "r") as file:
            self.settings = yaml.safe_load(file)

        self.device = self.settings['model2-settings']['device']
        self.model2_name = self.settings['model2-settings']['model2-name']
        self.threshold = self.settings['model2-settings']['prediction-threshold']
        self.model2, self.preprocess = clip.load(self.model2_name, device=self.device)
        self.labels = self.settings['label-settings']['labels']
        self.labels_ = []
        for label in self.labels:
            text = 'a photo of ' + label  # will increase model's accuracy
            self.labels_.append(text)

        self.text_features = self.vectorize_text(self.labels_)
        self.default_label = self.settings['label-settings']['default-label']

    @torch.no_grad()
    def transform_image(self, image: np.ndarray):
        pil_image = Image.fromarray(image).convert('RGB')
        tf_image = self.preprocess(pil_image).unsqueeze(0).to(self.device)
        return tf_image

    @torch.no_grad()
    def tokenize(self, text: list):
        text = clip.tokenize(text).to(self.device)
        return text

    @torch.no_grad()
    def vectorize_text(self, text: list):
        tokens = self.tokenize(text=text)
        text_features = self.model2.encode_text(tokens)
        return text_features

    @torch.no_grad()
    def predict_(self, text_features: torch.Tensor,
                 image_features: torch.Tensor):
        # Pick the top 5 most similar labels for the image
        image_features /= image_features.norm(dim=-1, keepdim=True)
        text_features /= text_features.norm(dim=-1, keepdim=True)
        similarity = image_features @ text_features.T
        values, indices = similarity[0].topk(1)
        return values, indices

    @torch.no_grad()
    def predict(self, image: np.array) -> dict:
        tf_image = self.transform_image(image)
        image_features = self.model2.encode_image(tf_image)
        values, indices = self.predict_(text_features=self.text_features,
                                        image_features=image_features)
        label_index = indices[0].cpu().item()
        label_text = self.default_label
        model2_confidence = abs(values[0].cpu().item())
        if model2_confidence >= self.threshold:
            label_text = self.labels[label_index]

        prediction = {
            'label': label_text,
            'confidence': model2_confidence
        }

        return prediction

    @staticmethod
    def plot_image(image: np.array, title_text: str):
        plt.figure(figsize=[13, 13])
        plt.title(title_text)
        plt.axis('off')
        if len(image.shape) == 3:
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        plt.imshow(image)


def predict_on_video(video_path):
    model2 = Model()
    cap = cv2.VideoCapture(video_path)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Predict on each frame
        prediction = model2.predict(frame)

        # Display the frame with prediction
        model2.plot_image(frame, f'Prediction: {prediction["label"]} (Confidence: {prediction["confidence"]:.2f})')
        st.pyplot()

    cap.release()


def main():
    st.title("Video Violence Detection")
    uploaded_file = st.file_uploader("Upload a video file", type=["mp4"])

    if uploaded_file is not None:
        predict_on_video(uploaded_file)


if __name__ == "_main_":
    main('./data/video.mp4')