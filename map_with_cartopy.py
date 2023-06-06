import os
import geopandas as gpd
import matplotlib.pyplot as plt
from cartopy.feature import ShapelyFeature
import cartopy.crs as ccrs
import matplotlib.patches as mpatches
import matplotlib.lines as mlines

def generate_handles(labels, colors, edge='k', alpha=1):
    lc=len(colors)
    handles=[]
    for i in range(len(labels)):
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

# geopandas is used to upload the files of towns, water, rivers and counties as shapefile form data_files folder

towns = gpd.read_file(os.path.abspath('data_files/Towns.shp'))
water = gpd.read_file(os.path.abspath('data_files/Water.shp'))
rivers = gpd.read_file(os.path.abspath('data_files/Rivers.shp'))
counties = gpd.read_file(os.path.abspath('data_files/Counties.shp'))

# create a figure of size 10x10 (representing the page size in inches), UTM zone for Norther Ireland
myFig = plt.figure(figsize=(10, 10))

# create a Universal Transverse Mercator reference system to transform data.
myCRS = ccrs.UTM(29)

# finally, create an axes object in the figure, using a UTM projection, where we can actually plot our data.
ax = plt.axes(projection=myCRS)

# outline of Northern Ireland using cartopy's ShapelyFeature
outline_feature = ShapelyFeature(outline['geometry'], myCRS, edgecolor='k', facecolor='w')
xmin, ymin, xmax, ymax = outline.total_bounds
ax.add_feature(outline_feature) # add the features we've created to the map.

# using the boundary of the shapefile features, zoom the map to our area of interest
ax.set_extent([xmin-5000, xmax+5000, ymin-5000, ymax+5000], crs=myCRS) # because total_bounds
# gives output as xmin, ymin, xmax, ymax,
# but set_extent takes xmin, xmax, ymin, ymax, we re-order the coordinates here.


# get the number of unique municipalities we have in the dataset
num_counties = len(counties.CountyName.unique())
print('Number of unique features: {}'.format(num_counties)) # note how we're using {} and format here!

# pick colors for the individual county boundaries - make sure to add enough for each of the counties
# to add a color, enclose the name above (e.g., violet) with single (or double) quotes: 'violet'
# remember that each colors should be separated by a comma
county_colors = ['gold','seagreen','khaki','sienna','hotpink','orange']

# get a list of unique names for the county boundaries
county_names = list(counties.CountyName.unique())
county_names.sort() # sort the counties alphabetically by name

# next, add the municipal outlines to the map using the colors that we've picked.
# here, we're iterating over the unique values in the 'CountyName' field.
# we're also setting the edge color to be black, with a line width of 0.5 pt.
# Feel free to experiment with different colors and line widths.
for ii, name in enumerate(county_names):
    feat = ShapelyFeature(counties.loc[counties['CountyName'] == name, 'geometry'], # first argument is the geometry
                          myCRS, # second argument is the CRS
                          edgecolor='k', # outline the feature in black
                          facecolor=county_colors[ii], # set the face color to the corresponding color from the list
                          linewidth=1, # set the outline width to be 1 pt
                          alpha=0.25) # set the alpha (transparency) to be 0.25 (out of 1)
    ax.add_feature(feat) # once we have created the feature, we have to add it to the map using ax.add_feature()

# here, we're setting the edge color to be the same as the face color. Feel free to change this around,
# and experiment with different line widths.
water_feat = ShapelyFeature(water['geometry'], # first argument is the geometry
                            myCRS, # second argument is the CRS
                            edgecolor='royalblue', # set the edgecolor to be mediumblue
                            facecolor='royalblue', # set the facecolor to be mediumblue
                            linewidth=1) # set the outline width to be 1 pt
ax.add_feature(water_feat) # add the collection of features to the map

river_feat = ShapelyFeature(rivers['geometry'], # first argument is the geometry
                            myCRS, # second argument is the CRS
                            edgecolor='royalblue', # set the edgecolor to be royalblue
                            linewidth=0.2) # set the linewidth to be 0.2 pt
ax.add_feature(river_feat) # add the collection of features to the map

# ShapelyFeature creates a polygon, so for point data we can just use ax.plot()
town_handle = ax.plot(towns.geometry.x, towns.geometry.y, 's', color='0.4', ms=6, transform=myCRS)

# generate a list of handles for the county datasets
# first, we add the list of names, then the list of colors, and finally we set the transparency
# (since we set it in the map)
county_handles = generate_handles(counties.CountyName.unique(), county_colors, alpha=0.25)

# note: if you change the color you use to display lakes, you'll want to change it here, too
water_handle = generate_handles(['Lakes'], ['royalblue'])

# note: if you change the color you use to display rivers, you'll want to change it here, too
river_handle = [mlines.Line2D([], [], color='royalblue')]

nice_names = [name.title() for name in county_names]

handles = county_handles + water_handle + river_handle + town_handle # use '+' to concatenate (combine) lists
labels = nice_names + ['Lakes', 'Rivers', 'Towns']

leg = ax.legend(handles, labels, title='Legend', title_fontsize=12,
                 fontsize=10, loc='upper left', frameon=True, framealpha=1)

gridlines = ax.gridlines(draw_labels=True, # draw  labels for the grid lines
                         xlocs=[-8, -7.5, -7, -6.5, -6, -5.5], # add longitude lines at 0.5 deg intervals
                         ylocs=[54, 54.5, 55, 55.5]) # add latitude lines at 0.5 deg intervals
gridlines.left_labels = False # turn off the left-side labels
gridlines.bottom_labels = False # turn off the bottom labels

for ind, row in towns.iterrows(): # towns.iterrows() returns the index and row
    x, y = row.geometry.x, row.geometry.y # get the x,y location for each town
    ax.text(x, y, row['TOWN_NAME'].title(), fontsize=7, transform=myCRS) # use plt.text to place a label at x,y

scale_bar(ax)

myFig.savefig('map.png', bbox_inches='tight', dpi=200)

#plt.show()