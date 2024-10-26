import matplotlib.pyplot as plt
from wa_visualizer.base_dataobj import FileHandler
import pandas as pd
from wa_visualizer.settings import Config
from pathlib import Path
from loguru import logger
import seaborn as sns

class BasicPlot:
    """
    A base class for creating basic plots using Matplotlib and Seaborn.

    This class provides common functionalities for initializing plot parameters,
    including titles, labels, and saving plots. It serves as a foundation for
    more specific plot types by encapsulating shared behaviors.

    Attributes:
    config (Config): Configuration object containing settings for the plot.
    title (str): Title of the plot.
    xlabel (str): Label for the x-axis.
    ylabel (str): Label for the y-axis.
    filename (str): Filename for saving the plot.
    show_legend (bool): Flag indicating whether to display the legend.

    Methods:
    __call__(data, *args, **kwargs): Creates the plot with the provided data.
    show_plot(): Displays the plot with the configured settings.
    save(): Saves the plot to the specified filename.
    plot(data, *args, **kwargs): Defines how to create the plot, empty in the basicPlot class.
    """    
    def __init__(self, config: Config, title_fig: str, xlabel: str, ylabel: str, filename: str, figsize=(12, 8), show_legend: bool = True, legend_title:str=""):
        self.config = config
        self.title_fig = title_fig
        self.xlabel = xlabel
        self.ylabel = ylabel
        self.filename = filename
        self.show_legend = show_legend
        self.legend_title = legend_title
    
    def plot(self, data: pd.DataFrame):
        #to define for each plot
        pass

    def show_plot(self):
        plt.title(self.title_fig)
        plt.xlabel(self.xlabel)
        plt.ylabel(self.ylabel)
        plt.tight_layout()
        if self.show_legend:
            plt.legend(title=self.legend_title, bbox_to_anchor=(1.0, 1), loc='upper left')
        plt.show()

    def save(self):
        filepath = self.config.img_dir / Path(self.filename)
        plt.savefig(filepath, bbox_inches='tight', transparent=False)
        plt.close()  # Close the figure to free up memory

class BasicScatterPlot(BasicPlot):
    """
    A class for creating basic scatter plots using Matplotlib and Seaborn.

    Inherits from BasicPlot and provides functionalities specific to scatter plots,
    including methods to plot data points and to visualize relationships between variables.

    Attributes:
    config (Config): Configuration object containing settings for the plot.
    title (str): Title of the scatter plot.
    xlabel (str): Label for the x-axis.
    ylabel (str): Label for the y-axis.
    show_legend (bool): Flag indicating whether to display the legend.

    Methods:
    plot(x, y, **kwargs): Creates a scatter plot for the given x and y data.
    plot_moving_average(data, timestamp_col, window, ax, color): Calculates
        and plots the moving average for the given data.
    show_plot(): Displays the scatter plot with configured settings.
    save(filename): Saves the scatter plot to the specified filename.
    """
    def __init__(self, config: Config, title_fig: str, xlabel: str, ylabel: str, filename: str, show_legend: bool = True):
        """
        Initializes the BasicScatterPlot with the provided configuration and plot parameters.

        Parameters:
        config (Config): Configuration object for plot settings.
        title (str): Title of the scatter plot.
        xlabel (str): Label for the x-axis.
        ylabel (str): Label for the y-axis.
        show_legend (bool): Flag to display the legend (default is True).
        """
        super().__init__(config, title_fig, xlabel, ylabel, filename, show_legend)

    def plot(self, x, y, **kwargs):
        """
        Creates a scatter plot with optional additional parameters.
        Parameters:
        config (Config): Configuration object for plot settings.
        title (str): Title of the scatter plot.
        xlabel (str): Label for the x-axis.
        ylabel (str): Label for the y-axis.
        **kwargs: all custom parameters

        """
        sns.scatterplot(x=x, y=y, **kwargs)

    def plot_moving_average(self, data: pd.DataFrame, timestamp_col: str, window: int, ax, color: str):
        """Calculate and plot the moving average."""
        data['moving_avg'] = data[timestamp_col].rolling(window=window).mean()
        moving_avg_plot = MovingAverageLinePlot(data, self.config.timestamp_col, color=color)       
        moving_avg_plot(ax)

class VerticalLine:
    """
    Adds a vertical line in a plot, given coordinates
    """    
    def __init__(self, x: str, label: str, color: str = 'white', horizontalalignment_text='center' ):
        self.x = x
        self.label = label
        self.color = color
        self.horizontalalignment_text=horizontalalignment_text 

    def __call__(self, ax)->None:
        self.draw(ax)

    def draw(self, ax)->None:
        ax.axvline(x=self.x, linestyle='--', label=self.label, color=self.color, zorder=1)
        
        # Get the current limits of the y-axis
        y_limits = ax.get_ylim()
        # Calculate the y position with the specified offset
        y_position = y_limits[1] * 0.8
        
        ax.text(self.x, y_position, self.label, color='red', 
                horizontalalignment=self.horizontalalignment_text, fontsize=10, rotation=90, 
                verticalalignment='top', zorder=2)


class MovingAverageLinePlot:
    """
    Draws a moving avarage line plot
    """    
    def __init__(self, data: pd.DataFrame, timestamp_col: str, color: str = 'gray'):
        self.data = data
        self.timestamp_col = timestamp_col
        self.color = color

    def __call__(self, ax)->None:
        self.draw(ax)

    def draw(self, ax)->None:
        """

        Draws the graphical representation of the object on the provided Axes.

        Parameters:
        ax (matplotlib.axes.Axes): The Axes object on which to draw the graphical representation. 
                                    This should be an instance of matplotlib's Axes, which acts 
                                    as the plotting area for rendering data visualizations.

        Returns:
        None: This method does not return any value. It modifies the Axes directly to 
            include the graphical elements.
        """        
        self.data["moving_avg"] = self.data[self.timestamp_col].rolling(window=1).mean()
        sns.lineplot(data=self.data, x=self.data.index, y="moving_avg", ax=ax, color=self.color)
    