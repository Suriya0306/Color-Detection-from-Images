import streamlit as st
import pandas as pd
from PIL import Image
import numpy as np
from collections import Counter

st.set_page_config(page_title="Auto Color Palette Finder", layout="centered")
st.title("🎨 Auto Color Palette Finder from Image")

uploaded_file = st.file_uploader("Upload an image (jpg, jpeg, png)", type=["jpg", "jpeg", "png"])

def get_palette(image, num_colors=8):
    # Resize for speed
    small_img = image.resize((100, 100))
    arr = np.array(small_img).reshape(-1, 3)
    arr = arr[~np.all(arr == 255, axis=1)]  # Remove pure white background if present

    # Count most common colors
    colors, counts = np.unique(arr, axis=0, return_counts=True)
    top_idxs = np.argsort(-counts)[:num_colors]
    palette = colors[top_idxs]
    return palette

if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="Uploaded Image", use_column_width=True)
    num_colors = st.slider("Number of colors to extract", 2, 12, 6)
    palette = get_palette(image, num_colors=num_colors)

    st.write("**Detected Color Palette:**")
    for rgb in palette:
        hex_code = '#{:02x}{:02x}{:02x}'.format(*rgb)
        st.markdown(
            f"<div style='display:flex;align-items:center;margin-bottom:10px;'>"
            f"<div style='width:60px;height:30px;background:{hex_code};border-radius:5px;border:1px solid #aaa;margin-right:15px;'></div>"
            f"<span style='font-size:18px;color:#222;font-weight:500'>{hex_code.upper()}</span>"
            f"<span style='margin-left:15px;color:gray;'>{tuple(rgb)}</span>"
            f"</div>",
            unsafe_allow_html=True
        )
else:
    st.info("Upload an image to automatically find its prominent colors (RGB + HEX).")
