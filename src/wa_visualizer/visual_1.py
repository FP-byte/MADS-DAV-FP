
import numpy as np
import pandas as pd
from pathlib import Path
import seaborn as sns
import matplotlib.pyplot as plt
from wa_visualizer.settings import Config
from wa_visualizer.basic_plots import BasicPlot
from wa_visualizer.data_processing import Preprocessor
from loguru import logger

class BarPlot(BasicPlot):
    def __init__(self, config: Config, title_fig: str, ylabel: str, xlabel: str, filename: str, legend_title: str = ""):
        super().__init__(config, title_fig, xlabel, ylabel, filename)
        self.legend_title = legend_title
        

    def __call__(self, data, stacked: bool):
        self.plot(data, stacked)
        self.save()
        self.show_plot()
        

    def plot(self, data: pd.DataFrame, stacked: bool = False):
        # Plotting
        ax = data.plot(kind='bar', stacked=stacked, figsize=(10, 8), color=self.custom_colors)
        # Annotate each bar with the percentage
        # if not stacked:
        #     for p in ax.patches:
        #         ax.annotate(f'{p.get_height():.1f}%', 
        #                             (p.get_x() + p.get_width() / 2, p.get_height()), 
        #                             ha='center', va='bottom', 
        #                             fontsize=10)

        plt.title(self.title_fig)
        plt.ylabel(self.ylabel)
        plt.xlabel(self.xlabel)
        plt.xticks(rotation=45)
        plt.legend(title=self.legend_title, bbox_to_anchor=(1.05, 1), loc='upper left')


class BarPlotVisualizer(Preprocessor):
    """
    Visualizes data using bar plots.

    Args:
        preprocessor (Preprocessor): Class responsible for preprocessing steps.
    """
    def __init__(self, preprocessor: Preprocessor):
        self.config = preprocessor.config
        self.preprocessor = preprocessor

    def visualization_week1(self):
        plot = BarPlot(
            title_fig="Tekst overwinning: Een Foto is Geen Duizend Woorden Waard",
            ylabel="Percentage van berichten",
            xlabel="Auteur",
            filename="1_categories_visualization.png",
            config=self.config
        )
        plot.custom_colors = ["lightgray",'salmon']
        processed_data = self.preprocessor.preprocess_week1()
        plot(processed_data, False)

    def visualization_week3(self):
        plot = BarPlot(
            title_fig="Kom je naar huis? Tiener appjes van 's ochtens vroeg tot Diep in de Nacht",
            #Kom naar huis! Diep in de nacht Chats met pubers
            ylabel="% van Totaal berichten",
            xlabel="Hour of the Day",
            filename="3_distribution_visualization.png",
            config=self.config,
            legend_title='Onderwerpen',

        )
        plot.custom_colors = self.config.color_palette
        df_counts_normalized = self.preprocessor.preprocess_week3()
        plot(df_counts_normalized, True)
