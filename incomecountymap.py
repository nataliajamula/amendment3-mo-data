import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import matplotlib.colors as mcolors

# Load the shapefile (replace with your actual file path)
shapefile_path = './shapefiles/ne_10m_admin_2_counties/ne_10m_admin_2_counties.shp'
gdf = gpd.read_file(shapefile_path)

missouri = gdf[gdf['ISO_3166_2'] == 'US-29']

#get income data
income_clean = pd.read_csv("./data/income_clean.csv")
incomeData = pd.DataFrame(income_clean)

# Normalize the values to [0, 1] for the colormap
norm = mcolors.Normalize(vmin=incomeData['Annual_Wage'].min(), vmax=incomeData['Annual_Wage'].max())

# Define a colormap (shades of blue)
cmap = plt.cm.Reds

# Create a dictionary to map county names to their values
county_value_map = dict(zip(incomeData['County'], incomeData['Annual_Wage']))

# Add a 'value' column to the GeoDataFrame by matching county names
missouri['Annual_Wage'] = missouri['NAME_VI'].map(county_value_map)

# Assign colors based on the normalized values
missouri['color'] = missouri['Annual_Wage'].apply(lambda x: cmap(norm(x)) if not np.isnan(x) else (1, 1, 1, 0))

# Plot the shape of Missouri with the heatmap
fig, ax = plt.subplots(figsize=(10, 8))
missouri.plot(ax=ax, color=missouri['color'], edgecolor='black')

# Add a colorbar
sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
sm.set_array([])  # Required for adding colorbar
cbar = plt.colorbar(sm, ax=ax)
cbar.set_label('Value')

ax.set_title('Missouri Income by County', fontsize=16)

plt.show()

