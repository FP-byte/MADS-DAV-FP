import pandas as pd
from loguru import logger


class DataObject:
    def __init__(self, datafile):
        self.datafile = datafile
        self.df = self.load_data()

    def load_data(self):
        
        return pd.read_parquet(self.datafile)


    
