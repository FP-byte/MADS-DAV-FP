import pandas as pd
from loguru import logger
from pathlib import Path
from wa_visualizer.settings import (Config, Folders)

class FileHandler():
    """
    A class for handling data file operations including loading and saving data.

    Attributes:
        data (pd.DataFrame): The DataFrame containing the loaded data.
        datafile (Path): The path to the data file.

    Args:
        folders (Folders): An instance of the Folders class containing paths for data storage.
        config (Config): An instance of the Config class containing configuration settings.
    """
    data: pd.DataFrame
    datafile: Path

    def __init__(self, folders: Folders, config: Config):
        """
        Initializes the FileHandler with folder paths and configuration settings.

        Args:
            folders (Folders): An instance of the Folders class.
            config (Config): An instance of the Config class.
        """
        self.folders = folders
        self.data = self.load_data()
        self.config = config

    def load_data(self) -> pd.DataFrame:
        """
        Loads data from a parquet file into a DataFrame.

        Returns:
            pd.DataFrame: The DataFrame containing the loaded data.
        """
        return pd.read_parquet(self.folders.datafile)

    def save_data(self) -> None:
        """
        Saves the current DataFrame to CSV and parquet formats.

        This method attempts to save the DataFrame and logs the outcome. 
        If an error occurs during the saving process, a warning is logged.
        """
        try:
            self.data.to_csv(self.folders.csv, index=False)
            self.data.to_parquet(self.folders.datafile, index=False)
            logger.success(f"Data processing completed and saved to:")
            logger.success(f"- {self.folders.datafile}")
            logger.success(f"- {self.folders.csv}")
        except Exception as e:
            logger.warning(f'Problem with saving: {e}')

