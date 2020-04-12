from bokeh.palettes import brewer, magma
from bokeh.models import GeoJSONDataSource, LinearColorMapper, ColorBar, Slider, HoverTool, Column
from bokeh.plotting import figure
from bokeh.io import show, output_file, curdoc
from bokeh.layouts import widgetbox, row, column
import pandas as pd
import geopandas as gpd
import json

# goal of file is to visualize data gotten from the previous files,
# starting in storeGameData and ending in getPercents,
# in the form of a map


def getYearData(df, year):
    # converts year data into usable json to be displayed
    dfYear = df[df['year'] == int(year)]
    merged = gdf.merge(dfYear, left_on='country_code',
                       right_on='country', how='left')
    merged.fillna('O', inplace=True)
    merged_json = json.loads(merged.to_json())
    json_data = json.dumps(merged_json)
    return(json_data)


# gets shape/geometry of map found in the ne mapData files
shapefile = './mapData/ne_110m_admin_0_countries.shp'

# column names in files, being renamed
gdf = gpd.read_file(shapefile)[['ADMIN', 'ADM0_A3', 'geometry']]
gdf.columns = ['country', 'country_code', 'geometry']

# getting rid of Antarctica which is huge and never has games made anyways
gdf = gdf.drop(gdf.index[159])

# reads country data and converts it into a panda array
datafile = './mapData/countries.json'
df = pd.read_json(datafile)


# input GeoJSON source (my data) that contains features for plotting.
json_data = getYearData(df, '2011')
geosource = GeoJSONDataSource(geojson=json_data)

# setting the color palette to visualize amount of games
palette = magma(256)
palette = palette[::-1]
color_mapper = LinearColorMapper(
    palette=palette, low=0, high=35, nan_color="white")

# define custom tick labels for color bar on bottom
tick_labels = {'0': '0%', '5': '5%', '10': '10%', '15': '15%',
               '20': '20%', '25': '25%', '30': '30%', '35': '35%', '40': '>40%'}
color_bar = ColorBar(color_mapper=color_mapper, label_standoff=8, width=500, height=20,
                     border_line_color=None, location=(0, 0), orientation='horizontal', major_label_overrides=tick_labels)

# hover tool that allows you to switch between years
hover = HoverTool(
    tooltips=[('Country/region', '@country_x'), ('Percentage', '@count' + '%')])

# creates figure
p = figure(title='Percentage of Popular Games Coming From Countries in 2011',
           plot_height=600, plot_width=950, toolbar_location=None, tools=[hover])
p.xgrid.grid_line_color = None
p.ygrid.grid_line_color = None


# add patch renderer to figure
p.patches('xs', 'ys', source=geosource, fill_color={'field': 'count', 'transform': color_mapper},
          line_color='black', line_width=0.25, fill_alpha=1)

# adding color bar below map
p.add_layout(color_bar, 'below')

# updates the map with a new year determined by the slider


def updateplot(attr, old, new):
    year = slider.value
    newData = getYearData(df, year)
    geosource.geojson = newData
    p.title.text = 'Percentage of Popular Games Coming From Countries in % d' % year


slider = Slider(title='Year', start=2011, end=2019, step=1, value=2011)
slider.on_change('value', updateplot)

layout = column(p, slider)

# display figure with bokeh

curdoc().add_root(layout)
show(layout)
