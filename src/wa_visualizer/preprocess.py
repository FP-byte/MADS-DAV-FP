import datetime
from pathlib import Path
import tomllib
from loguru import logger
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import click

from wa_visualizer.basis import DataObject
from wa_visualizer.visualize import Visualizer



class Preprocess(DataObject):
    def __init__(self, datafile):
       # self.datafile=datafile
        super().__init__(datafile)
        print(self)
 

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

