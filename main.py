import streamlit as st
import pandas as pd
import cv2
import numpy as np
from PIL import Image

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

# Title
st.title("🎨 Color Detection App")

# Sidebar for CSV and image upload
st.sidebar.header("Upload Inputs")
uploaded_img = st.sidebar.file_uploader("Upload an image", type=["jpg", "png", "jpeg"])
color_df = load_colors("colors.csv")

if uploaded_img:
    # Display image
    file_bytes = np.asarray(bytearray(uploaded_img.read()), dtype=np.uint8)
    cv_image = cv2.imdecode(file_bytes, 1)
    cv_image_rgb = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)
    st.image(cv_image_rgb, channels="RGB", caption="Click below to pick a color")

    # Click interaction
    st.markdown("#### Click on the image to detect a color:")
    clicked = st.image(cv_image_rgb, channels="RGB", use_column_width=True)

    # Interactive pixel detection
    coords = st.session_state.get("click_coords", None)
    if coords:
        x, y = coords
        pixel = cv_image_rgb[y, x]
        r, g, b = pixel

        matched = get_closest_color(r, g, b, color_df)
        hex_val = matched['hex'] if matched is not None else '#000000'
        name = matched['color_name'] if matched is not None else 'Unknown'

        # Show results
        st.markdown("### Color Detected:")
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

        # Clear session state after displaying
        st.session_state["click_coords"] = None

    # Let user click on the image using coordinates input
    st.markdown("Click anywhere inside the image preview above to simulate picking a color (Streamlit doesn’t yet support direct pixel click natively).")
    x = st.number_input("X-coordinate", min_value=0, max_value=cv_image.shape[1] - 1, value=10)
    y = st.number_input("Y-coordinate", min_value=0, max_value=cv_image.shape[0] - 1, value=10)
    if st.button("Detect Color"):
        st.session_state["click_coords"] = (x, y)
else:
    st.info("Please upload an image to begin.")
