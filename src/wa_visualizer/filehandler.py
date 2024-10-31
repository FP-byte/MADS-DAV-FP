import pandas as pd
from loguru import logger
from pathlib import Path
from wa_visualizer.settings import (Config, Folders)

class FileHandler():
    data : pd.DataFrame
    datafile: Path

    def __init__(self, folders: Folders, config: Config):
        self.folders = folders
        self.data = self.load_data()
        self.config = config

    def load_data(self):
              
        return pd.read_parquet(self.folders.datafile)

    def save_data(self) -> None:
        """
        save dataframe
        """        
        
        try:
            self.data.to_csv(self.folders.csv, index=False)
            self.data.to_parquet(self.folders.datafile, index=False)
            logger.success(f"Data processing completed and saved to:")
            logger.success(f"-{self.folders.datafile}")
            logger.success(f"-{self.folders.csv}")
        except Exception as e:
            logger.warning(f'Problem with saving: {e}')
