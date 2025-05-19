import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
from streamlit_image_coordinates import streamlit_image_coordinates
import matplotlib.pyplot as plt

# --- Load color dataset ---
@st.cache_data
def load_colors(csv_path):
    df = pd.read_csv(csv_path)
    return df

def get_closest_color_name(R, G, B, color_data):
    min_dist = float('inf')
    closest_name = None
    for _, row in color_data.iterrows():
        d = np.sqrt((R - row.R)**2 + (G - row.G)**2 + (B - row.B)**2)
        if d < min_dist:
            min_dist = d
            closest_name = row.color_name
    return closest_name

def rgb2hex(row):
    return "#{:02x}{:02x}{:02x}".format(row['R'], row['G'], row['B'])

# --- App Layout ---
st.set_page_config(page_title="🎨 Color Tools", layout="wide")
st.sidebar.title("🧭 Navigation")
page = st.sidebar.radio("Go to", ["🎯 Color Detector", "📊 Color Pie Chart"])

color_data = load_colors("colors.csv")

if page == "🎯 Color Detector":
    st.markdown("<h1 style='color:#6C63FF;'>Real-Time Color Detection</h1>", unsafe_allow_html=True)
    st.write("Upload an image and click anywhere to instantly get its color name and RGB values.")

    uploaded_file = st.file_uploader("**Upload an Image**", type=["jpg", "jpeg", "png"])
    if uploaded_file:
        try:
            image = Image.open(uploaded_file).convert("RGB")
            img_np = np.array(image)
            st.write("Click on the image to detect color:")

            col1, col2 = st.columns([2,1])
            with col1:
                result = streamlit_image_coordinates(image, key="color_picker")
            with col2:
                st.markdown("<h4 style='margin-bottom:8px;'>Detected Color</h4>", unsafe_allow_html=True)
                if result is not None:
                    x, y = int(result["x"]), int(result["y"])
                    if 0 <= x < img_np.shape[1] and 0 <= y < img_np.shape[0]:
                        R, G, B = img_np[y, x]
                        color_name = get_closest_color_name(R, G, B, color_data)
                        hex_code = '#{:02X}{:02X}{:02X}'.format(R, G, B)
                        st.markdown(f"<b>Color Name:</b> <span style='color:{hex_code}'>{color_name}</span>", unsafe_allow_html=True)
                        st.markdown(f"<b>RGB:</b> ({R}, {G}, {B})")
                        st.markdown(f"<b>HEX:</b> {hex_code}")
                        st.markdown(
                            f'<div style="width:80px;height:40px;background:rgb({R},{G},{B});border:2px solid #333;margin-top:10px;border-radius:7px"></div>',
                            unsafe_allow_html=True
                        )
                    else:
                        st.warning("Click is outside image bounds.")
                else:
                    st.info("Click on the image to detect color.")
            st.markdown("---")
            st.markdown("#### 🎞️ Preview")
            st.image(image, use_column_width=True)

        except Exception as e:
            st.error(f"Could not read the image: {e}")
    else:
        st.info("Please upload an image to begin.")

elif page == "📊 Color Pie Chart":
    st.markdown("<h1 style='color:#6C63FF;'>Color Pie Chart</h1>", unsafe_allow_html=True)
    st.write("View all colors in the dataset as a pie chart. Each slice is labeled with the color name and RGB values.")

    labels = [
        f"{row['color_name']} ({row['R']},{row['G']},{row['B']})"
        for _, row in color_data.iterrows()
    ]
    hex_colors = color_data.apply(rgb2hex, axis=1)
    sizes = [1] * len(labels)

    # Pie chart
    fig, ax = plt.subplots(figsize=(8, 8))
    wedges, texts = ax.pie(
        sizes,
        labels=None,
        colors=hex_colors,
        startangle=90,
        counterclock=False,
        wedgeprops=dict(width=0.4, edgecolor='w')
    )
    ax.set_title("Pie Chart of All Colors", fontsize=18, color="#6C63FF")
    ax.axis('equal')
    st.pyplot(fig)

    # Custom Legend
    st.markdown("#### Legend")
    for label, color in zip(labels, hex_colors):
        st.markdown(
            f"<div style='display:inline-block;width:30px;height:20px;background:{color};border-radius:4px;margin-right:8px;vertical-align:middle'></div>"
            f"<span style='vertical-align:middle;font-size:16px'>{label}</span>",
            unsafe_allow_html=True
        )
