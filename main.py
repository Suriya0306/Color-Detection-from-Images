import streamlit as st
import pandas as pd
import cv2
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from collections import Counter

# Load color dataset
@st.cache_data
def load_colors(csv_path):
    try:
        return pd.read_csv(csv_path)
    except FileNotFoundError:
        st.error("Color dataset not found!")
        return pd.DataFrame()

def get_closest_color(r, g, b, color_df):
    min_dist = float('inf')
    closest_color = None
    for _, row in color_df.iterrows():
        dist = np.sqrt((r - row['R'])**2 + (g - row['G'])**2 + (b - row['B'])**2)
        if dist < min_dist:
            min_dist = dist
            closest_color = row
    return closest_color

def get_dominant_colors(image_rgb, color_df, top_n=10):
    pixels = image_rgb.reshape(-1, 3)
    color_names = []
    for pixel in pixels:
        r, g, b = pixel
        matched = get_closest_color(r, g, b, color_df)
        if matched is not None:
            color_names.append(matched['color_name'])
    color_count = Counter(color_names)
    return color_count.most_common(top_n)

# Title
st.title("🎨 Color Detection App with Live RGB and Pie Chart")

# Sidebar for CSV and image upload
st.sidebar.header("Upload Inputs")
uploaded_img = st.sidebar.file_uploader("Upload an image", type=["jpg", "png", "jpeg"])
color_df = load_colors("colors.csv")

if uploaded_img:
    file_bytes = np.asarray(bytearray(uploaded_img.read()), dtype=np.uint8)
    cv_image = cv2.imdecode(file_bytes, 1)
    cv_image_rgb = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)

    st.image(cv_image_rgb, channels="RGB", caption="Image Preview")

    st.markdown("### 🔍 Select Pixel Coordinates for Color Detection")
    x = st.slider("X-coordinate", 0, cv_image.shape[1] - 1, 10)
    y = st.slider("Y-coordinate", 0, cv_image.shape[0] - 1, 10)

    pixel = cv_image_rgb[y, x]
    r, g, b = int(pixel[0]), int(pixel[1]), int(pixel[2])
    matched = get_closest_color(r, g, b, color_df)

    hex_val = matched['hex'] if matched is not None else '#000000'
    name = matched['color_name'] if matched is not None else 'Unknown'

    col1, col2 = st.columns([1, 3])
    with col1:
        st.markdown(f"**{name}**")
        st.markdown(f"RGB: ({r}, {g}, {b})")
        st.markdown(f"Hex: `{hex_val}`")
    with col2:
        st.markdown(
            f"<div style='width:100%;height:80px;background:{hex_val};border:1px solid #000'></div>",
            unsafe_allow_html=True
        )

    st.markdown("---")
    st.markdown("### 📊 Color Distribution Pie Chart")

    color_distribution = get_dominant_colors(cv_image_rgb, color_df, top_n=10)
    if color_distribution:
        labels, counts = zip(*color_distribution)
        fig, ax = plt.subplots()
        ax.pie(counts, labels=labels, autopct="%1.1f%%", colors=[get_closest_color(*(np.mean(cv_image_rgb[cv_image_rgb == label], axis=0)), color_df)['hex'] if get_closest_color(*(np.mean(cv_image_rgb[cv_image_rgb == label], axis=0)), color_df) is not None else '#000000' for label in labels])
        ax.axis("equal")
        st.pyplot(fig)
    else:
        st.warning("Could not compute color distribution.")
else:
    st.info("Please upload an image to begin.")
