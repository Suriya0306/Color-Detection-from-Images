pip install webcolors
import csv
import matplotlib.colors as mcolors

# Use CSS4 named colors from matplotlib
colors = mcolors.CSS4_COLORS  # name: hex

with open('colors.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['color_name', 'hex', 'R', 'G', 'B'])

    for name, hex_val in colors.items():
        r, g, b = [int(c * 255) for c in mcolors.to_rgb(hex_val)]
        writer.writerow([name, hex_val, r, g, b])

print("✅ Successfully created colors.csv from matplotlib CSS4_COLORS!")
