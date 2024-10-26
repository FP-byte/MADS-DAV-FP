import numpy as np
import pandas as pd
from pathlib import Path
import seaborn as sns
import matplotlib.pyplot as plt
from wa_visualizer.settings import Config
from wa_visualizer.basic_plots import BasicPlot

class RelationshipsPlot(BasicPlot):
    """
    Facegrid regression plot class

    Args:
        BasicPlot (_type_): _description_
    """    
    def __init__(self, config: Config, title_fig: str, xlabel: str, ylabel: str, filename: str, show_legend: bool = False):
        super().__init__(config, title_fig, xlabel, ylabel, filename, show_legend)  # Initialize basicPlot superclass
        #custom colors
        self.color_palette = {'With Emoji': 'salmon', 'Without Emoji': 'blue'}

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
        g = sns.FacetGrid(data, col='emoji_status', hue='emoji_status', height=5, aspect=1.5, palette=self.color_palette)

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

        # Finally, show the plot
        plt.show()
        self.save()

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





    

    
