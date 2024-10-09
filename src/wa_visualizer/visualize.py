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
from wa_visualizer.visualize_relationships import *
from wa_visualizer.visualization_2 import TimeSeriesVisualization
from wa_visualizer.visualization_1 import LanguageUsageVisualization
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
        visualization = TimeSeriesVisualization(p, p_corona)
        visualization.create_plot()
        visualization.show()
        

    def visualization_week3(self):
       

        plt.figure(figsize=(12, 6))
        # Define custom colors
        colors = [  'red', 'gray', 'darkgray', 'lightgray', ]

        plt.stackplot(df_counts.index, df_counts.T, colors=colors, labels=df_counts.columns, alpha=0.6)
        plt.title("Feeding the Dialogue: How Hunger Fuels Food Conversations")
        plt.xlabel('Hour of Day')
        plt.ylabel('Number of messages about topic')
        plt.xticks(df_counts.index, rotation=45)
        # Add a legend with a title
        plt.legend(loc='upper left', title='Topics')
        plt.grid()
        plt.show()

    def visualization_week4(self):
        df = self.df
        return visualization_relationships(df)
        


@click.command()
@click.option("--week", default="1", help="Week number: input 1 to 7")
@click.option("--all", default="all", help="All visualizations")
def main(week, all): 
    possible_options = ['1', '2', '3', '4']
    if week not in possible_options:
        raise ValueError('Must be a number between 1 and 7')

    configfile = Path("./config.toml").resolve()
    print(configfile)

    with configfile.open("rb") as f:
         config = tomllib.load(f)

    datafile = (Path(".") / Path(config["processed"]) / config["current"]).resolve()

    

    if not datafile.exists():
        logger.warning("Datafile does not exist.")
    else:
        visualizer = Visualizer(datafile)

        if week.lower()=="1" or all:
            visualizer.visualization_week1()
        if week.lower()=="2" or all:
            visualizer.visualization_week2()

        if week.lower()=="3" or all:
            visualizer.visualization_week3()

        if week.lower()=="4" or all:
            visualizer.visualization_week4()
        

if __name__ == "__main__":   

        main(week, all)

