import pandas as pd
from loguru import logger
from pathlib import Path
from wa_visualizer.settings import (Settings, Folders)

class FileHandler():
    data : pd.DataFrame
    datafile: Path

    def __init__(self, folders: Folders, settings: Settings):
        self.folders = folders
        self.data = self.load_data()

    def load_data(self):       
        return pd.read_parquet(self.folders.datafile)

    
#class Regex:


"""
@dataclass
class Config:
    input_file: str = "filename.csv"
    timestamp_format: str = ""
    outputfile: str 

class FileHandler:
    def __init__(slef, config: Config):
        self.config = config

    def load_csv()"""