import plotly.express as px
import pandas as pd
import geopandas as gdp
import format_file as ff

# 'Datos.json' contains all the unemployment separated by provinces
data = pd.read_json('Datos.json')

# 'ff.format_df' function cleans and formats the data for our specific porpouse
# See 'format_file.py' for details
df = ff.format_df(pd.DataFrame(data)) 

# 'spain.geojson' contains geographic boundaries (lat/lon) for Spanish provinces 
geojson = gdp.read_file('spain.geojson') 

spain_center={'lat':36.234410, 'lon':-4.884160}

# Creates a choropleth map with the given data 
# ----------
# Key parameters:
# - df: the DataFrame containing the data 
# - geojson: the GeoJSON file with province boundaries
# - featureidkey: establishes a relation between 'locations' from df and 'properties.name' from geojson
# - animation_frame: adds a time-line, based on the year in this case
# - color: colors each province based on the 'Valor' column
fig = px.choropleth_mapbox(
    df,
    geojson=geojson,
    locations='Provincia', 
    featureidkey='properties.name',
    animation_frame='Anyo',
    color='Valor',
    color_continuous_scale='brwnyl',
    range_color=[0,40],
    zoom=4,
    center=spain_center,
    mapbox_style='carto-darkmatter',
    labels={'taxa_atur': 'Taxa d\'atur'},
    title='Mapa Tasa d\'Atur per Província'
)

fig.show()
