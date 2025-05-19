import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# --- Load color dataset ---
@st.cache_data
def load_colors(csv_path):
    df = pd.read_csv(csv_path)
    return df

def rgb2hex(row):
    return "#{:02x}{:02x}{:02x}".format(row['R'], row['G'], row['B'])

# --- App Layout ---
st.set_page_config(page_title="🎨 Color Pie Chart", layout="centered")
st.title("🎨 Color Dataset Pie Chart with RGB Values")

# File uploader
csv_file = st.file_uploader("Upload your colors.csv", type=["csv"])

if csv_file:
    try:
        color_data = load_colors(csv_file)

        # Prepare data for the pie chart
        labels = [
            f"{row['color_name']} ({row['R']},{row['G']},{row['B']})"
            for _, row in color_data.iterrows()
        ]
        hex_colors = color_data.apply(rgb2hex, axis=1)
        sizes = [1] * len(labels)
        explode = [0.03] * len(labels)  # Slightly separate each slice

        # Pie chart with improved visuals
        fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(aspect="equal"))
        wedges, _ = ax.pie(
            sizes,
            labels=None,
            colors=hex_colors,
            startangle=90,
            counterclock=False,
            wedgeprops=dict(width=0.4, edgecolor='w'),
            explode=explode
        )
        ax.set_title("Pie Chart of All Colors with Names and RGB Values", fontsize=20, color="#6C63FF", pad=20)

        # Annotate each slice with a colored bullet and label
        for i, (wedge, label) in enumerate(zip(wedges, labels)):
            angle = (wedge.theta2 + wedge.theta1) / 2.
            x = np.cos(np.deg2rad(angle))
            y = np.sin(np.deg2rad(angle))
            ha = 'left' if x > 0 else 'right'
            ax.annotate(
                f"● {label}",
                xy=(x * 1.1, y * 1.1), xytext=(x * 1.25, y * 1.25),
                color=hex_colors.iloc[i],
                fontsize=12,
                ha=ha, va='center',
                fontweight='bold',
                bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="none", alpha=0.85),
                arrowprops=dict(arrowstyle="-", color=hex_colors.iloc[i], lw=2, alpha=0.7)
            )

        ax.axis('equal')

        st.pyplot(fig)
        st.success("Pie chart generated from your uploaded colors.csv!")

    except Exception as e:
        st.error(f"Error loading or processing CSV: {e}")

    with st.expander("See the raw color data"):
        st.dataframe(color_data)
else:
    st.info("Please upload a colors.csv file with columns: color_name, R, G, B")
