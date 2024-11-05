import numpy as np
import pandas as pd
from pathlib import Path
import seaborn as sns
import matplotlib.pyplot as plt
from wa_visualizer.settings import Config
from wa_visualizer.basic_plots import BasicPlot
from wa_visualizer.data_processing import Preprocessor
from loguru import logger

class FacetGridPlot(BasicPlot):
    """
    Facegrid regression plot class

    Args:
        BasicPlot (_type_): _description_
    """    
    def __init__(self, config: Config, title_fig: str, xlabel: str, ylabel: str, filename: str, show_legend: bool = False):
        super().__init__(config, title_fig, xlabel, ylabel, filename, show_legend)  # Initialize basicPlot superclass
        #custom colors
        self.color_palette = {'With Emoji': 'salmon', 'Without Emoji': '#444'}

    def __call__(self, data: pd.DataFrame, x: str, y: str, **kwargs):
        self.create_plot(data, x, y, **kwargs)  # Pass additional kwargs to create_plot

    def create_plot(self, data: pd.DataFrame, x: str, y: str, **kwargs):
        """
        Create a FacetGrid with two scatterplot an a custom colour palette
        Args:
            data (pd.DataFrame): data
            x (str):column name to plot on x-axis
            y (str):column name to plot on y-axis 
        """        
        g = sns.FacetGrid(data, col=self.config.emoji_status_col, hue=self.config.emoji_status_col, height=5, aspect=1.5, palette=self.color_palette)

        # Map the regression plot using the plot method from the RegPlot class
        g.map_dataframe(self.plot, x, y, scatter_size=60)

        # Set a main title above the grid
        g.fig.suptitle(self.title_fig, fontsize=16)

        # Set titles for each subplot correctly
        g.set_titles(col_template="Messages {col_name}")  # Customize if needed

        # Set axis labels
        g.set_axis_labels(self.xlabel, self.ylabel)

        # Adjust layout to avoid overlap with the main title
        plt.subplots_adjust(top=0.85)

        # Save the plot
        self.save()

        # Finally, show the plot
        self.show_plot()  # Show the plot with the legend setting
        

    def plot(self, x: str, y: str, scatter_size: int, label: str = None, **kwargs):
        """
        Create a regression plot on each facet.

        Args:
            x (str):column name to plot on x-axis
            y (str):column name to plot on y-axis 
            scatter_size (int): size of dots
            label (str, optional): label, defaults to None.
        """        
        
        sns.regplot(x=x, y=y, marker='o', scatter_kws={'s': scatter_size}, label=label, **kwargs)
        plt.grid(False)

class RelationshipsPlotVisualizer(Preprocessor):
    """
    Visualizes relationships in data, specifically focusing on the relationship between age and message length 
    (in terms of log-transformed values) and the impact of emojis on communication efficiency.

    Args:
        preprocessor (Preprocessor): Class responsible for preprocessing steps such as cleaning, transforming,
                                      and preparing the data for visualization.
    """
    def __init__(self, preprocessor: Preprocessor):
        """
        Initializes the RelationshipsPlotVisualizer with the provided preprocessor.

        Args:
            preprocessor (Preprocessor): An instance of the Preprocessor class to handle data preprocessing.
        """
        self.config = preprocessor.config
        self.preprocessor = preprocessor

    def visualization_week4(self):
        """
        Creates a relationships plot for the week 4 data that visualizes how age correlates with the average 
        length of messages (in logarithmic scale), highlighting the trend that adults save time typing by using emojis.

        This method processes the week 4 data, specifically focusing on the age and message length, and then 
        generates a scatter plot to visualize the relationship.

        The plot is saved as '4_relationships_visualization.png'.

        """
        plot = FacetGridPlot(
            config=self.config,
            title_fig="Langzame vingers in een snelle wereld: volwassenen en hun emoji-tijdwinst",
            xlabel='Leeftijd',
            ylabel='Gemiddelde van de logaritme van Berichtlengte',
            filename='4_relationships_visualization.png',
        )

        # Preprocess the data for week 4 (average log-transformed message length)
        avg_log_df = self.preprocessor.preprocess_week4()

        # Create the plot using the preprocessed data
        plot(avg_log_df, self.config.age_col, self.config.log_length_col, scatter_size=60)

        