import streamlit as st
import cv2
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image
from collections import Counter

# Load CSV dataset
@st.cache_data
def load_colors(csv_path="data/colors.csv"):
    return pd.read_csv(csv_path)

def get_color_name(rgb, color_data):
    color_data["distance"] = np.linalg.norm(color_data[["r", "g", "b"]].values - np.array(rgb), axis=1)
    return color_data.loc[color_data["distance"].idxmin(), "color_name"]

def get_dominant_colors(image_array, top_n=5):
    pixels = image_array.reshape(-1, image_array.shape[-1])
    counter = Counter([tuple(p) for p in pixels])
    most_common_colors = counter.most_common(top_n)
    return most_common_colors

# Streamlit UI
st.title("Color Detection & Pie Chart Visualization")
color_data = load_colors()

# Upload Image
uploaded_file = st.file_uploader("Upload an Image", type=["jpg", "png", "jpeg"])
if uploaded_file:
    image = Image.open(uploaded_file)
    img_array = np.array(image)
    st.image(image, caption="Uploaded Image", use_column_width=True)

    # Select pixel coordinates
    x = st.number_input("X-coordinate", min_value=0, max_value=img_array.shape[1]-1, value=0)
    y = st.number_input("Y-coordinate", min_value=0, max_value=img_array.shape[0]-1, value=0)

    if st.button("Detect Color"):
        rgb_value = img_array[y, x]
        hex_code = f"#{rgb_value[0]:02x}{rgb_value[1]:02x}{rgb_value[2]:02x}"
        color_name = get_color_name(rgb_value, color_data)

        st.write(f"**Detected Color:** {color_name}")
        st.write(f"**RGB:** {rgb_value}")
        st.write(f"**HEX:** {hex_code}")
        st.color_picker("Color Preview", hex_code)

        st.markdown(f'<div style="width:100px;height:50px;background-color:{hex_code};border:1px solid #000"></div>', unsafe_allow_html=True)

    # Pie Chart for Dominant Colors
    if st.button("Show Color Distribution"):
        top_colors = get_dominant_colors(img_array)
        labels, values = zip(*top_colors)
        hex_colors = [f"#{r:02x}{g:02x}{b:02x}" for r, g, b in labels]

        fig, ax = plt.subplots()
        ax.pie(values, labels=hex_colors, colors=hex_colors, autopct="%1.1f%%")
        ax.axis("equal")
        st.pyplot(fig)
