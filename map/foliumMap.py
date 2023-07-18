import folium
import branca.colormap as cmp
from folium.plugins import StripePattern, CirclePattern

class foliumMap:
    def __init__(self, centroid, zoom_start = 9) -> None:
        self.map = folium.Map(location = centroid,
                              zoom_start = zoom_start)

    def add_geojson(self, geojson):
        folium.GeoJson(geojson,).add_to(self.map)

    def add_choropleth(self, geo_data, key, columns):
        folium.Choropleth(geo_data = geo_data,
                          name = 'Nombre de commerces',
                          data = geo_data,
                          key_on = 'feature.properties.{}'.format(key),
                          columns = columns,
                          fill_color = 'YlOrRd',
                          nan_fill_color = 'purple').add_to(self.map)

    def linear_colormap(self, vmax):
        return cmp.LinearColormap(['blue', 'yellow', 'red'],
                                  vmin = 0,
                                  vmax = vmax)

    def step_colormap(self, n_step):
        colors = ["#e78ac3",
                  "#8da0cb",
                  "#fc8d62",
                  "#66c2a5",
                  "#ffff33",
                  "#ff7f00",
                  "#984ea3",
                  "#4daf4a",
                  "#377eb8",
                  "#ff2d00"]

        vmax = n_step * 100
        return cmp.StepColormap(colors,
                                index = list(range(0, vmax, 100)),
                                vmin = 0,
                                vmax = vmax)

    def color_data(self, cmp, geo_data, column):
        style_function = lambda feature: {
            'fillColor': cmp(feature['properties'][column]),
            'fillOpacity': 0.8,
            'color': 'black'
        }

        folium.GeoJson(geo_data[~geo_data[column].isna()],
                       style_function = style_function)\
              .add_to(self.map)
        cmp.add_to(self.map)

    def fill_nan(self, geo_data, column, color = '#000'):
        style_function = lambda feature: {
            'fillColor': color,
            'fillOpacity': 0.8,
            'color': 'black'
        }

        folium.GeoJson(geo_data[geo_data[column].isna()],
                       style_function = style_function)\
              .add_to(self.map)

    def highlight_text(self, geo_data, fields, aliases):
        style_function = lambda x: {'fillColor': '#000',
                                     'color':'#000000',
                                     'fillOpacity': 0 }
        folium.GeoJson(geo_data,
                       control = False,
                       style_function = style_function,
                       tooltip = folium.features.GeoJsonTooltip(
                       fields = fields,
                       aliases = aliases,
                       style=("background-color: white; \
                              color: #333333; \
                              font-family: arial; \
                              font-size: 12px; \
                              padding: 10px;"))).add_to(self.map)

    def stripe_stores(self, geo_data, column = 'stores'):
        colors = {
            0: 'green',
            1: 'yellow',
            2: 'red'
        }

        sp = lambda feature: {
            "fillPattern": StripePattern(angle = 45,
                                         color = colors[feature['properties'][column]],
                                         opacity = 1 ),
            'color': 'black',
            'fillOpacity': 0.75,
        }


        folium.GeoJson(geo_data[~geo_data[column].isna()], control = True, style_function= sp )\
              .add_to(self.map)