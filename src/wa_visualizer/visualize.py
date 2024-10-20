import datetime
from pathlib import Path
import tomllib
from loguru import logger
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import click

from wa_visualizer.data_processing import Preprocess
from wa_visualizer.base_visualization import BaseVisualization

from wa_visualizer.visualization_2 import TimeSeriesVisualization
from wa_visualizer.visualization_1 import LanguageUsageVisualization
from wa_visualizer.visualization_3 import StackPlotVisualization
from wa_visualizer.visualization_4 import RelationshipsVisualization
import logging

# Set up the logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Visualizer(Preprocess):
    def __init__(self, datafile):
       # self.datafile=datafile
       super().__init__(datafile)

    
    def visualization_week1(self):
        self.prepocess_week1()
        self.custom_colors = ['#FF9999', '#66B3FF', '#99FF99']
        visualization1 = LanguageUsageVisualization(self.df)
        visualization1.create_plot()
        visualization1.show()

  

    def visualization_week2(self):
        df_corona, df = self.prepocess_week2()
        p = self.calc_messages(df)
        p_corona = self.calc_messages(df_corona)
        visualization2 = TimeSeriesVisualization(p, p_corona)
        visualization2.create_plot()
        visualization2.show()

        

    def visualization_week3(self):
       
        df_counts = self.preprocess_week3()
        # Create the visualization instance
        visualization3 = StackPlotVisualization(df_counts)
        visualization3.create_plot()
        visualization3.show()


    def visualization_week4(self):
        df = self.df
        visualization4 = RelationshipsVisualization(df)
        visualization4.create_plot()
        visualization4.show()     

@click.command()
@click.option("--week", default="1", help="Week number: input 1 to 7")
@click.option("--all", default=False, help="All visualizations")
def main(week, all):
    possible_options = ["all", '1', '2', '3', '4', '5', '6', '7']
    if week not in possible_options:
        raise ValueError('Must be a number between 1 and 7')

    configfile = Path("./config.toml").resolve()

    with configfile.open("rb") as f:
         config = tomllib.load(f)

    datafile = (Path(".") / Path(config["processed"]) / config["current"]).resolve()

    if not datafile.exists():
        logger.warning("Datafile does not exist.")
    else:
        visualizer = Visualizer(datafile)

        if week.lower()=="1" or all:
            print("week 1")
            visualizer.visualization_week1()

        if week.lower()=="2" or all:
            print("week 2")
            visualizer.visualization_week2()

        if week.lower()=="3" or all:
            print("week 3")
            visualizer.visualization_week3()

        if week.lower()=="4" or all:
            print("week 4")
            visualizer.visualization_week4()
        

if __name__ == "__main__":   

        main(week, all)

