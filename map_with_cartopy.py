import os
import geopandas as gpd
import matplotlib.pyplot as plt
from cartopy.featrue import ShapelyFeature
import cartopy.crs as ccrs
import matplotlip.patches as mpatches
import matplotlib.lines as mlines

def generate_handles(labels, color, edge='k', alpha=1):
    lc=len(colors)
    handles=[]
    for i in range(len(lables)):
        handles.append(mpatches.Rectangle((0,0),1,1,facecolor=colors[i % lc], edgecolor=edge, alpha=alpha))
        return handles