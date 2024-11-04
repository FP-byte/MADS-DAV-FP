import datetime
from pathlib import Path
import tomllib
from loguru import logger
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import click
import numpy as np

from wa_visualizer.data_processing import Preprocessor
from wa_visualizer.settings import (BaseRegexes, Folders, Config, BaseStrings, keywordsFilter, extraRegexes, basicConfig)
from wa_visualizer.filehandler import FileHandler
from wa_visualizer.visual_1_3 import BarPlotVisualizer
from wa_visualizer.visual_2 import TimeSeriesPlotVisualizer
from wa_visualizer.visual_4 import RelationshipsPlotVisualizer
from wa_visualizer.visual_5 import TSNEPlotVisualizer
import sys

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
    """
    possible_options = ["all", '1', '2', '3', '4', '5']
    if week not in possible_options:
        raise ValueError('Must be a number between 1 and 7')

    configfile = Path("./config.toml").resolve()
    # read configuration file
    with open("config.toml", "rb") as f:
        config = tomllib.load(f)
        raw = Path(config["raw"])
        processed = Path(config["processed"])
        csv = Path(config["csv"])
        current = Path(config["current"])
    # read source datafiles
    datafile = (Path(".") / processed / config["current"]).resolve()
    csv = (Path(".") / processed / config["csv"]).resolve() 

    if not datafile.exists() or not csv.exists():
        logger.warning("Datafile or csv file does not exist.")
    else:
        #define folders paths
        folders = Folders(
            raw=raw,
            processed=processed,
            datafile=datafile,
            current=current,
            csv=csv    
        )
        #instantiate preprocessor
        preprocessor = Preprocessor(folders, extraRegexes, basicConfig, keywordsFilter)
        #run preprocessor
        preprocessor()
        #start logger
        logger.remove()
        logger.add('./logs/logfile.log' , rotation="1 week", level="DEBUG")
        logger.add(sys.stderr, level="INFO")
        bar_plot_visualizer = False

        if week.lower() == "1" or all:
            print("visualize plot for week 1")
            if not bar_plot_visualizer:
                bar_plot_visualizer = BarPlotVisualizer(preprocessor)
            bar_plot_visualizer.visualization_week1()

        if week.lower() == "2" or all:
            print("visualize plot for week 2")
            time_series_plot_visualizer = TimeSeriesPlotVisualizer(preprocessor)
            time_series_plot_visualizer.visualization_week2()

        if week.lower() == "3" or all:
            print("visualize plot for week 3")
            if not bar_plot_visualizer:
                bar_plot_visualizer = BarPlotVisualizer(preprocessor)
            bar_plot_visualizer.visualization_week3()

        if week.lower() == "4" or all:
            print("visualize plot for week 4")
            relationships_plot_visualizer = RelationshipsPlotVisualizer(preprocessor)
            relationships_plot_visualizer.visualization_week4()

        if week.lower() == "5" or all:
            print("visualize plot for week 5")
            relationships_plot_visualizer = TSNEPlotVisualizer(preprocessor)
            relationships_plot_visualizer.visualization_week5()

if __name__ == "__main__":   
    main("2", all)
