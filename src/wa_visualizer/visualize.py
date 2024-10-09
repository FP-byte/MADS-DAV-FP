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
from wa_visualizer.visualize_categories import *
from wa_visualizer.visualize_timeseries import *
from wa_visualizer.visualization_1 import LanguageUsageVisualization


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
        # 
        # ## Grouping by author and language
        # user_language_counts = self.df.groupby(['author', 'language']).size().unstack(fill_value=0)

        # # Combine 'NL' and 'IT' into 'Verbal'
        # user_language_counts['Verbal'] = user_language_counts[['NL', 'IT']].sum(axis=1)

        # # Drop the original NL and IT columns
        # user_language_counts.drop(['NL', 'IT'], inplace=True, axis=1)

        # # Calculate the total counts for each author
        # total_counts = user_language_counts.sum(axis=1)

        # # Calculate percentages
        # user_language_percentages = user_language_counts.div(total_counts, axis=0) * 100

        # # Print the percentage DataFrame
        # print(user_language_percentages)

        # # Plotting
        # ax = user_language_percentages.plot(kind='bar', stacked=False, figsize=(12, 8), color=self.custom_colors)
        # plt.title('Language Usage Percentage by Author')
        # plt.ylabel('Percentage (%)')
        # plt.xlabel('Author')
        # plt.xticks(rotation=45)
        # plt.legend(title='Language')

        # # Annotate each bar with the percentage
        # for p in ax.patches:
        #     ax.annotate(f'{p.get_height():.1f}%', 
        #                 (p.get_x() + p.get_width() / 2, p.get_height()), 
        #                 ha='center', va='bottom', 
        #                 fontsize=10)

        # plt.tight_layout()
        # plt.show()
  

    def visualization_week2(self):
        df, df_corona = self.prepocess_week2()
        p = self.calc_messages(df)
        p_corona = self.calc_messages(df_corona)
        self.visualize_timeseries(p, p_corona)

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

