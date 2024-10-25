
import seaborn as sns
import matplotlib.pyplot as plt
from pathlib import Path
import pandas as pd
from wa_visualizer.basic_plots import BasicBarPlot
from wa_visualizer.settings import Config
from loguru import logger


class LanguageUsagePlot(BasicBarPlot):
    def __init__(self, config:Config,  title: str, ylabel: str, xlabel: str, filename:str):
        super().__init__(self, title, xlabel, ylabel)  # Initialize base class
        self.config = config
        self.filename = filename

    def __call__(self, data):
        self.create_plot(data)

    def create_plot(self, data: pd.DataFrame):
        # Plotting
        ax = data.plot(kind='bar', stacked=False, figsize=(12, 8), color=self.config.custom_colors)
        plt.title(self.title)
        plt.ylabel(self.ylabel)
        plt.xlabel(self.xlabel)
        plt.xticks(rotation=45)
        plt.legend(title='Communication type', bbox_to_anchor=(1.05, 1), loc='upper left')

        # Annotate each bar with the percentage
        for p in ax.patches:
            ax.annotate(f'{p.get_height():.1f}%', 
                        (p.get_x() + p.get_width() / 2, p.get_height()), 
                        ha='center', va='bottom', 
                        fontsize=10)

        # Save the plot

        filepath = self.config.img_dir / Path(self.filename)
        plt.savefig(filename, bbox_inches='tight', transparent=False)
        logger.info(f"Saving file to {filepath}")
        self.show_plot()
        plt.close()

# class LanguageUsagePlot(BasicBarPlot):
#     # Les 1: comparing categories

#     def __init__(self, user_language_percentages:pd.DataFrame, title:str, ylabel:str xlable:str):
#         self.user_language_percentages = user_language_percentages  # Initialize with the data for visualization
#         self.settings = settings

#     def __call__(self):
#         self.create_plot()

#     def create_plot(self):
#         # Plotting
#         ax = self.user_language_percentages.plot(kind='bar', stacked=False, figsize=(12, 8), color=self.settings.custom_colors)
#         plt.title("Voices in Numbers: in Whatsapp ")
#         plt.ylabel('Percentage')
#         plt.xlabel('Author')
#         plt.xticks(rotation=45)
#         plt.legend(title='Communication type')

#         # Annotate each bar with the percentage
#         for p in ax.patches:
#             ax.annotate(f'{p.get_height():.1f}%', 
#                         (p.get_x() + p.get_width() / 2, p.get_height()), 
#                         ha='center', va='bottom', 
#                         fontsize=10)
#         filename = self.settings.img_dir / Path("1_categories_visualization.png")
#         plt.savefig(filename, bbox_inches='tight', transparent=False)
#         plt.show()
#         plt.close()
