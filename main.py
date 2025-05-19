import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load color dataset
@st.cache_data
def load_colors(csv_path):
    return pd.read_csv(csv_path)

def rgb2hex(row):
    return "#{:02x}{:02x}{:02x}".format(row['R'], row['G'], row['B'])

# Streamlit Layout
st.set_page_config(page_title="🎨 Enhanced Color Pie Chart", layout="wide")
color_data = load_colors("colors.csv")

st.markdown("<h1 style='color:#6C63FF;'>Color Pie Chart - Improved Design</h1>", unsafe_allow_html=True)
st.write("This updated version includes better aesthetics and readability enhancements.")

# Prepare labels and colors
labels = [f"{row['color_name']} ({row['R']},{row['G']},{row['B']})" for _, row in color_data.iterrows()]
hex_colors = color_data.apply(rgb2hex, axis=1)
sizes = [1] * len(labels)  # Equal distribution

# Pie Chart
fig, ax = plt.subplots(figsize=(8, 8))
wedges, texts, autotexts = ax.pie(
    sizes,
    labels=None,  # Removed to prevent clutter
    colors=hex_colors,
    startangle=90,
    counterclock=False,
    wedgeprops=dict(width=0.4, edgecolor='w'),
    autopct='%1.1f%%',  # Display percentage
    shadow=True  # Adds depth
)

# Customize text appearance
for text in texts + autotexts:
    text.set_fontsize(12)
    text.set_color("black")
    text.set_fontweight("bold")

ax.set_title("Enhanced Pie Chart of Colors", fontsize=18, color="#6C63FF")
ax.axis('equal')  # Ensure circular proportions

st.pyplot(fig)

# Custom Legend
st.markdown("#### Legend")
for label, color in zip(labels, hex_colors):
    st.markdown(
        f"<div style='display:inline-block;width:30px;height:20px;background:{color};border-radius:4px;margin-right:8px;vertical-align:middle'></div>"
        f"<span style='vertical-align:middle;font-size:16px'>{label}</span>",
        unsafe_allow_html=True
    )
