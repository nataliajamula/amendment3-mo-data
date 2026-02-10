import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import matplotlib.colors as mcolors

# Load the shapefile (replace with your actual file path)
shapefile_path = './moShape.shp'
missouri = gpd.read_file(shapefile_path)
print(len(missouri))

abortion_csv = pd.read_csv("./abortion.csv")
abortData = pd.DataFrame(abortion_csv)

# Normalize the values to [0, 1] for the colormap
norm = mcolors.Normalize(vmin=abortData['% Yes'].min(), vmax=abortData['% Yes'].max())

# Define a colormap (shades of blue)
cmap = plt.cm.Blues

# Create a dictionary to map county names to their values
county_value_map = dict(zip(abortData['County'], abortData['% Yes']))

# Add a 'value' column to the GeoDataFrame by matching county names
missouri['% Yes'] = missouri['NAME'].map(county_value_map)

# Assign colors based on the normalized values
missouri['color'] = missouri['% Yes'].apply(lambda x: cmap(norm(x)) if not np.isnan(x) else (1, 1, 1, 0))

# Plot the shape of Missouri with the heatmap
fig, ax = plt.subplots(figsize=(10, 8))
missouri.plot(ax=ax, color=missouri['color'], edgecolor='black')

# Add a colorbar
sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
sm.set_array([])  # Required for adding colorbar
cbar = plt.colorbar(sm, ax=ax)
cbar.set_label('Value')

ax.set_title('Missouri Heatmap by County', fontsize=16)

plt.show()
