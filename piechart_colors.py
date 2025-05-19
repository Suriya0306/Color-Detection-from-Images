import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load color dataset
@st.cache_data
def load_colors(csv_path):
    df = pd.read_csv(csv_path)
    return df

st.set_page_config(page_title="Color Pie Chart", layout="centered")
st.title("🎨 Color Dataset Pie Chart")

color_data = load_colors("colors.csv")

# Prepare data for the pie chart
labels = color_data['color_name']
# Convert RGB to hex for matplotlib
def rgb2hex(row):
    return "#{:02x}{:02x}{:02x}".format(row['R'], row['G'], row['B'])
colors = color_data.apply(rgb2hex, axis=1)

# Plot pie chart
fig, ax = plt.subplots(figsize=(8, 8))
ax.pie([1]*len(labels), labels=labels, colors=colors, startangle=90, counterclock=False, wedgeprops=dict(width=0.5))
ax.set_title("Pie Chart of All Colors in Dataset")

st.pyplot(fig)
