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

# --- App Layout ---
st.set_page_config(page_title="Color Tools", layout="centered")
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Color Detector", "Color Pie Chart"])

color_data = load_colors("colors.csv")

if page == "Color Detector":
    st.title("🎨 Real-Time Color Detection App")
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
    if uploaded_file:
        try:
            image = Image.open(uploaded_file).convert("RGB")
            img_np = np.array(image)
            st.write("Move your mouse over the image to detect color (click to get coordinates):")
            result = streamlit_image_coordinates(image, key="color_picker")
            if result is not None:
                x, y = int(result["x"]), int(result["y"])
                if 0 <= x < img_np.shape[1] and 0 <= y < img_np.shape[0]:
                    R, G, B = img_np[y, x]
                    color_name = get_closest_color_name(R, G, B, color_data)
                    st.markdown(f"**Color Name:** {color_name}")
                    st.markdown(f"**RGB:** ({R}, {G}, {B})")
                    st.markdown(
                        f'<div style="width:80px;height:40px;background:rgb({R},{G},{B});border:2px solid #333;margin-top:10px"></div>',
                        unsafe_allow_html=True
                    )
                else:
                    st.warning("Click is outside image bounds.")
        except Exception as e:
            st.error(f"Could not read the image: {e}")
    else:
        st.info("Please upload an image to begin.")

elif page == "Color Pie Chart":
    st.title("🎨 Color Dataset Pie Chart with RGB Values")
    # Prepare data for the pie chart
    labels = [
        f"{row['color_name']} ({row['R']},{row['G']},{row['B']})"
        for _, row in color_data.iterrows()
    ]

    # Convert RGB to hex for matplotlib
    def rgb2hex(row):
        return "#{:02x}{:02x}{:02x}".format(row['R'], row['G'], row['B'])
    colors = color_data.apply(rgb2hex, axis=1)

    # Equal-sized slices (1 for each color)
    sizes = [1] * len(labels)

    # Plot pie chart
    fig, ax = plt.subplots(figsize=(9, 9))
    wedges, texts = ax.pie(
        sizes, labels=labels, colors=colors, startangle=90, counterclock=False,
        wedgeprops=dict(width=0.4, edgecolor='w')
    )
    ax.set_title("Pie Chart of All Colors with Names and RGB Values")
    st.pyplot(fig)
