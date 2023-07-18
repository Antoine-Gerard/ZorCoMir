from . import *
import geopandas as gpd
import numpy as np

class GeoJson:
    def __init__(self, department) -> None:
        self.store_columns = [
            'Épicerie',
            'Hypermarché',
            'Supermarché',
            'Supérette',
            'Boulangerie',
            'Boucherie charcuterie'
        ]

        self.set_leading_zero(department)

        self.gdf = gpd.read_file(self.department_to_json()[department])
        self.centroid = self.gdf.dissolve().centroid

        if self.leading_zero:
            self.gdf['code_'] = self.gdf['code'].apply(lambda s: s[1:])

    def department_to_json(self):
        return {
            'Ariège': folder.joinpath('data/ariege.geojson')
        }

    def set_leading_zero(self, department):
        if department in ['Ariège']:
            self.leading_zero = True
        else:
            self.leading_zero = False

    def compute_lat_long(self):
        centroid = self.gdf.centroid
        self.gdf['lat'] = centroid.apply(lambda p: p.y)
        self.gdf['lon'] = centroid.apply(lambda p: p.x)

    def add_data(self, dataframe):
        # Zorcomir column
        left_on = 'code_' if self.leading_zero else 'code'
        self.gdf = self.gdf.merge(dataframe,
                                  left_on  = left_on,
                                  right_on ="Code commune")
        # Put nan where is not ZorCoMir
        self.gdf.loc[self.gdf['ZorCoMir'].str.contains('NC -'), self.store_columns] = np.nan
        self.gdf.loc[self.gdf['ZorCoMir'].str.contains('NC -'), 'Population' ] = np.nan

    def sum(self, columns = [], name = ''):
        self.gdf[name] = self.gdf[columns].sum(axis = 1, min_count = 1)