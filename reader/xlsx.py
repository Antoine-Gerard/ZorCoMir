from . import *
import pandas as pd

class Excel:
    def __init__(self, department) -> None:
        self.xlsx = pd.ExcelFile(self.department_to_xlsx()[department], engine = 'openpyxl')
        self.sheet = self.open_sheet(department)

    def open_sheet(self, sheet_name):
        return self.xlsx.parse(sheet_name, converters = {'Code commune': str})\
                        .rename(columns = {
                            'zone de revitalisation des commerces en milieu rural - ZoRCoMiR': 'ZorCoMir',
                            'Population \n municipale \n 2019': 'Population'
                        })

    def department_to_xlsx(self):
        return {
            'Ariège': folder.joinpath('data/Ariege.xlsx')
        }