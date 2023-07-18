import streamlit as st
from streamlit_folium import st_folium, folium_static
from folium.features import DivIcon
import branca.colormap as cm
import numpy as np

from map.foliumMap import foliumMap
from reader.geojson import GeoJson

from components.select import *
from reader.xlsx import Excel

# Sidebar
st.set_page_config(layout='wide')

stores = []
department = None
with st.sidebar:
    department = select_box('Département',
                            ['Ariège'])

    if department is not None:
        sheet = Excel(department).sheet
        geojson = GeoJson(department)
        geojson.add_data(sheet)


    stores = st.multiselect('Commerces', geojson.store_columns)


if department is not None:


    geojson.compute_lat_long()

    map = foliumMap([geojson.centroid.y[0], geojson.centroid.x[0]])
    pop_max = geojson.gdf['Population'].max()
    n_step = round(pop_max/100)

    linear_cmp = map.step_colormap(n_step)


    # If chosen stores
    if len(stores) > 0:
        geojson.sum(stores, name = 'stores')
        map.color_data(linear_cmp, geojson.gdf, 'Population')
        map.fill_nan(geojson.gdf, 'Population')
        map.stripe_stores(geojson.gdf)

        map.highlight_text(geojson.gdf,
                          ['nom', 'Population', 'stores'],
                          ['Ville: ', 'Population: ', 'Nombre de commerces: '])

        #map.add_choropleth(geojson.gdf, 'code_', ['code_', 'Population \n municipale \n 2019'])
        st.date = folium_static(map.map, width = 1000)

    # Merge A
# if sheet_name is not None:


#     if len(stores) > 0:
#         ariege['stores'] = ariege[stores].sum(axis=1, min_count=1)


#         folium.Choropleth(geo_data=ariege,
#                           name= 'Choropleth',
#                           data=ariege,
#                           columns=['code_', 'stores'],
#                           key_on="feature.properties.code_",
#                           fill_color='YlOrRd',
#                           nan_fill_color='purple').add_to(m)

#         style_function = lambda x: {'fillColor': '#000',
#                                     'color':'#000000',
#                                     'fillOpacity': 0.1,
#                                     'weight': 0.1}
#         highlight_function = lambda x: {'fillColor': '#000000',
#                                         'color':'#000000',
#                                         'fillOpacity': 0.50,
#                                         'weight': 0.1}

#         folium.features.GeoJson(ariege,
#                                 style_function=style_function,
#                                 control=False,
#                                 highlight_function=highlight_function,
#                                 tooltip=folium.features.GeoJsonTooltip(
#                                 fields=['nom','stores'],
#                                 aliases=['Ville: ','Nombre de magasins: '],
#                                 style=("background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;"))).add_to(m)


#         st_date = st_folium(m, width=1500)