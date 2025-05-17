import streamlit as st
import pandas as pd
import cv2
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter

# Load and process color dataset
@st.cache_data
def load_colors(csv_file):
    try:
        df = pd.read_csv(csv_file)

        if "Dec.Code" not in df.columns or "Color.Name" not in df.columns or "Hex.Code" not in df.columns:
            st.error("CSV must include 'Color.Name', 'Hex.Code', and 'Dec.Code' columns.")
            return pd.DataFrame()

        # Extract R, G, B from Dec.Code (format: 'R,G,B')
        rgb = df["Dec.Code"].str.split(",", expand=True).astype(int)
        df["R"] = rgb[0]
        df["G"] = rgb[1]
        df["B"] = rgb[2]
        df["color_name"] = df["Color.Name"]
        df["hex"] = df["Hex.Code"]

        return df[["color_name", "hex", "R", "G", "B"]]
    except Exception as e:
        st.error(f"Error loading CSV: {e}")
        return pd.DataFrame()

# Color matching
def get_closest_color(r, g, b, color_df):
    min_dist = float('inf')
    closest_color = None
    for _, row in color_df.iterrows():
        dist = np.sqrt((r - row['R'])**2 + (g - row['G'])**2 + (b - row['B'])**2)
        if dist < min_dist:
            min_dist = dist
            closest_color = row
    return closest_color

# Dominant color analysis
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

# Streamlit UI
st.title("🎨 Color Detection App (Custom CSV Format)")

st.sidebar.header("Upload Files")
uploaded_img = st.sidebar.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
uploaded_csv = st.sidebar.file_uploader("Upload color CSV", type=["csv"])

if uploaded_csv:
    color_df = load_colors(uploaded_csv)
    if color_df.empty:
        st.stop()
else:
    st.warning("Please upload a color dataset with 'Color.Name', 'Hex.Code', 'Dec.Code'")
    st.stop()

if uploaded_img:
    file_bytes = np.asarray(bytearray(uploaded_img.read()), dtype=np.uint8)
    cv_image = cv2.imdecode(file_bytes, 1)
    cv_image_rgb = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)

    st.image(cv_image_rgb, channels="RGB", caption="Uploaded Image", use_container_width=True)

    st.markdown("### 🖱️ Select a pixel")
    x = st.slider("X-coordinate", 0, cv_image.shape[1] - 1, 10)
    y = st.slider("Y-coordinate", 0, cv_image.shape[0] - 1, 10)

    marked_img = cv_image_rgb.copy()
    cv2.circle(marked_img, (x, y), radius=6, color=(0, 0, 255), thickness=-1)
    st.image(marked_img, channels="RGB", caption=f"Selected pixel: ({x},{y})", use_container_width=True)

    r, g, b = cv_image_rgb[y, x]
    matched = get_closest_color(r, g, b, color_df)

    if matched is not None:
        st.markdown("### 🎯 Matched Color")
        col1, col2 = st.columns([1, 3])
        with col1:
            st.write(f"**{matched['color_name']}**")
            st.write(f"RGB: ({r}, {g}, {b})")
            st.code(matched['hex'])
        with col2:
            st.markdown(
                f"<div style='width:100%;height:80px;background:{matched['hex']};border:1px solid #000'></div>",
                unsafe_allow_html=True
            )
    else:
        st.warning("No matching color found.")

    st.markdown("### 📊 Dominant Colors")
    color_dist = get_dominant_colors(cv_image_rgb, color_df)
    if color_dist:
        labels, counts = zip(*color_dist)
        fig, ax = plt.subplots()
        ax.pie(counts, labels=labels, autopct='%1.1f%%', startangle=140)
        ax.axis('equal')
        st.pyplot(fig)
else:
    st.info("Upload an image to begin.")
