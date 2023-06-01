import os
import geopandas as gpd
import matplotlib.pyplot as plt
from cartopy.feature import ShapelyFeature
import cartopy.crs as ccrs
import matplotlib.patches as mpatches
import matplotlib.lines as mlines

def generate_handles(labels, color, edge='k', alpha=1):
    lc=len(colors)
    handles=[]
    for i in range(len(lables)):
        handles.append(mpatches.Rectangle((0,0),1,1,facecolor=colors[i % lc], edgecolor=edge, alpha=alpha))
        return handles

def scale_bar(ax, location=(0.92, 0.95)):
    x0, x1, y0, y1=ax.get_extent()
    sbx=x0+(1-y0)*location[0]
    sby=y0+(y1-y0)*location[1]

    ax.plot([sbx, sbx - 20000], [sby, sby], color='k', linewidth=9, transform=ax.projection)
    ax.plot([sbx, sbx - 10000], [sby, sby], color='k', linewidth=6, transform=ax.projection)
    ax.plot([sbx - 10000, sbx - 20000], [sby, sby], color='w', linewidth=6, transform=ax.projection)

    ax.text(sbx, sby - 4500, '20 km', transform=ax.projection, fontsize=8)
    ax.text(sbx - 12500, sby - 4500, '10 km', transform=ax.projection, fontsize=8)
    ax.text(sbx - 24500, sby - 4500, '0 km', transform=ax.projection, fontsize=8)


outline = gpd.read_file(os.path.abspath('data_files/NI_outline.shp'))
