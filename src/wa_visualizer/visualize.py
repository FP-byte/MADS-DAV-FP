import datetime
from pathlib import Path
import tomllib
from loguru import logger
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import click
import numpy as np
from wa_visualizer.data_cleaning import DataCleaner
from wa_visualizer.data_processing import Preprocessor
from wa_visualizer.settings import (BaseRegexes, Folders, Config, BaseStrings, keywordsFilter, extraRegexes, basicConfig)
from wa_visualizer.filehandler import FileHandler
from wa_visualizer.visual_1_3 import BarPlotVisualizer
from wa_visualizer.visual_2 import TimeSeriesPlotVisualizer
from wa_visualizer.visual_4 import RelationshipsPlotVisualizer
from wa_visualizer.visual_5 import TSNEPlotVisualizer
import sys

def run_visualization_pipeline(folders, week, all=False):
    """
    Runs a series of visualizations based on the specified week or for all weeks, processing and visualizing data 
    step-by-step. This function uses a pipeline approach to process data and generate various types of plots for 
    each week of the data.

    Args:
        folders (list): List of folder paths containing the data to be processed.
        week (str): The specific week for which to generate the visualization. Can be '1', '2', '3', '4', '5' or 
                    'all' to visualize plots for all weeks.
        all (bool, optional): If True, generates visualizations for all weeks. Default is False, meaning only 
                               the visualization for the specified week is created.
    
    This function supports visualizing the following plots:
        - Week 1: Bar plots showing basic distribution of data.
        - Week 2: Time series plots showing changes over time.
        - Week 3: Bar plots comparing different categories.
        - Week 4: Relationship plots exploring correlations between different variables.
        - Week 5: t-SNE plots showing high-dimensional data reduced to 2D space.
    """
    # Start preprocessor for week visualization
    preprocessor = Preprocessor(folders, basicConfig, keywordsFilter)
    # Initialize plot visualizer object
    bar_plot_visualizer = False

    # Visualize plot for week 1 or all weeks
    if week.lower() == "1" or all:
        print("Visualizing plot for week 1")
        if not bar_plot_visualizer:
            bar_plot_visualizer = BarPlotVisualizer(preprocessor)
        bar_plot_visualizer.visualization_week1()

    # Visualize plot for week 2 or all weeks
    if week.lower() == "2" or all:
        print("Visualizing plot for week 2")
        time_series_plot_visualizer = TimeSeriesPlotVisualizer(preprocessor)
        time_series_plot_visualizer.visualization_week2()

    # Visualize plot for week 3 or all weeks
    if week.lower() == "3" or all:
        print("Visualizing plot for week 3")
        if not bar_plot_visualizer:
            bar_plot_visualizer = BarPlotVisualizer(preprocessor)
        bar_plot_visualizer.visualization_week3()

    # Visualize plot for week 4 or all weeks
    if week.lower() == "4" or all:
        print("Visualizing plot for week 4")
        relationships_plot_visualizer = RelationshipsPlotVisualizer(preprocessor)
        relationships_plot_visualizer.visualization_week4()

    # Visualize plot for week 5 or all weeks
    if week.lower() == "5" or all:
        print("Visualizing plot for week 5")
        relationships_plot_visualizer = TSNEPlotVisualizer(preprocessor)
        relationships_plot_visualizer.visualization_week5()


@click.command()
@click.option("--week", default="1", help="Week number: input 1 to 5")
@click.option("--all", is_flag=True, help="Generate all visualizations")
def main(week, all):
    """
    Main function to execute data visualization for specified week.

    Args:
        week (str): The week number (1 to 7) to visualize.
        all (bool): Flag to indicate whether to generate all visualizations.
    
    Raises:
        ValueError: If the specified week number is not between 1 and 5.
        FileNotFoundError: If the specified file is not found
        General Error: for all other cases
    """
    #start logger
    logger.remove()
    logger.add('./logs/logfile.log' , rotation="1 week", level="DEBUG")
    logger.add(sys.stderr, level="INFO")
    
    possible_options = ["all", '1', '2', '3', '4', '5']
    if week not in possible_options:
        raise ValueError('Must be a number between 1 and 7')

    configfile = Path("./config.toml").resolve()
    # read configuration file
    with open("config.toml", "rb") as f:
        config = tomllib.load(f)
        raw = Path(config["raw"]) # path to raw
        processed = Path(config["processed"]) #path to processed
        csv = Path(config["csv"]) # csv filename 
        datafile = Path(config["current"]) # datafile name

    # read raw source datafiles
    rawdatafile = (Path(".") / raw / config["current"]).resolve()
    csvraw = (Path(".") / raw / config["csv"]).resolve()

    # processed datafiles paths
    datafile = (Path(".") / processed / config["current"]).resolve()
    csv_datafile = (Path(".") / processed / config["csv"]).resolve()

    # Define folder paths
    folders = Folders(
            raw=raw,
            processed=processed,
            datafile = datafile,
            rawdatafile = rawdatafile,
            csvraw =csvraw,            
            csv=csv_datafile    
        )

    # check raw datafile existance
    if not raw.exists() and not csv_raw.exists():
        # Data files does not exist.
        logger.warning("Datafile or csv file does not exists. Please check your path in the config.toml file.")
    
    # do cleaning step once, if processed files do not exist
    if not datafile.exists() or not csv_datafile.exists():
       
        # Datafile or csv doesn't exist, so we need to run the cleaning step.
        try:
            # Instantiate the data cleaner
            cleandata = DataCleaner(folders, extraRegexes, basicConfig, True)
            # Run clean and save data to processed folder
            cleandata()
            # run visualizations
            run_visualization_pipeline(folders, week, all)
        except FileNotFoundError as e:
            # Specific exception if the file is not found
            logger.error(f"File not found during data cleaning: {e}")
        except ValueError as e:
            # Specific exception for value errors (e.g., wrong data format)
            logger.error(f"Value error during data cleaning: {e}")
        except Exception as e:
            # Generic exception handler for any other unexpected issues
            logger.error(f"An unexpected error occurred during data cleaning: {e}")

    else:
        # Data files exist, no need to clean. Proceed with the next steps.
        logger.info("Source datafile and csv file exists. Proceeding with visualization processing.")
        run_visualization_pipeline(folders, week, all)
    
    
if __name__ == "__main__":   
    main("2", all)
