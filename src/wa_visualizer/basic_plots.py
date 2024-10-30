import matplotlib.pyplot as plt
from wa_visualizer.filehandler import FileHandler
from wa_visualizer.data_processing import Preprocessor
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
        #define basic custom colors for plots
        self.color = 'gray'
        self.color_highlight = 'red'
        #set gray scala colors as default
        self.custom_colors = ['gray', "lightgray", 'darkgray', '#EEE']   
    
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
        plt.close()  # Close the figure to free up memory

    def save(self):
        filepath = self.config.img_dir / Path(self.filename)
        plt.savefig(filepath, bbox_inches='tight', transparent=False)
        print(f"Plot saved to: {filepath}")
        

class BarPlot(BasicPlot):
    def __init__(self, config: Config, title_fig: str, ylabel: str, xlabel: str, filename: str, legend_title: str = ""):
        super().__init__(config, title_fig, xlabel, ylabel, filename)
        self.legend_title = legend_title

    def __call__(self, data, stacked: bool):
        self.plot(data, stacked)
        self.show_plot()
        self.save()

    def plot(self, data: pd.DataFrame, stacked: bool = False):
        # Plotting
        ax = data.plot(kind='bar', stacked=stacked, figsize=(10, 8), color=self.config.custom_colors)
        plt.title(self.title_fig)
        plt.ylabel(self.ylabel)
        plt.xlabel(self.xlabel)
        plt.xticks(rotation=45)
        plt.legend(title=self.legend_title, bbox_to_anchor=(1.05, 1), loc='upper left')


class BasicScatterPlot(BasicPlot):
    """
    A class for creating basic scatter plots using Matplotlib and Seaborn.

    Inherits from BasicPlot and provides functionalities specific to scatter plots,
    including methods to plot data points and to visualize relationships between variables.

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
        Creates a scatter plot for the given x and y data, with optional additional parameters.
        Parameters:
        config (Config): Configuration object for plot settings.
        title (str): Title of the scatter plot.
        xlabel (str): Label for the x-axis.
        ylabel (str): Label for the y-axis.
        **kwargs: all custom parameters

        """
        sns.scatterplot(x=x, y=y, **kwargs)

    def plot_moving_average(self, data: pd.DataFrame, timestamp_col: str, window: int, ax, color: str):
        """
        Calculates and plots the moving average for the given data.

        This function computes the moving average of a specified time series data column 
        over a defined window size and then visualizes it on the provided axes.

        Args:
            data (pd.DataFrame): The input data from which the moving average will be calculated.
            timestamp_col (str): The name of the column containing the timestamps to be used for calculating the moving average.
            window (int): The size of the moving window (number of periods) for averaging.
            ax (matplotlib.axes.Axes): The axes on which to plot the moving average line.
            color (str): The color of the moving average line for visualization.

        Returns:
            None: This function does not return any value; it directly modifies the provided axes.
        """     
        data['moving_avg'] = data[timestamp_col].rolling(window=window).mean()
        moving_avg_plot = MovingAverageLinePlot(data, self.config.timestamp_col, color=color)       
        moving_avg_plot(ax)

class VerticalLine:
    """
    A class to add a vertical line to a plot at a specified x-coordinate.

    This class allows for the customization of the vertical line's label, color, and text alignment. 
    It is designed to enhance the visualization of specific points in a plot by marking them with 
    dashed vertical lines and associated labels.

    Attributes:
    x (str): The x-coordinate at which to draw the vertical line.
    label (str): The label to display alongside the vertical line.
    color (str): The color of the vertical line (default is 'white').
    horizontalalignment_text (str): The horizontal alignment of the label text (default is 'center').

    Methods:
    __call__(ax): Calls the draw method to render the vertical line on the given axes.
    draw(ax): Draws the vertical line on the specified axes and adds the corresponding label.
    """

    def __init__(self, x: str, label: str,  horizontalalignment_text='center', color: str = 'gray'):
        """
        Initializes the VerticalLine with the specified parameters.

        Parameters:
        x (str): The x-coordinate for the vertical line.
        label (str): The label for the vertical line.
        color (str): The color of the vertical line (default is 'gray').
        horizontalalignment_text (str): The horizontal alignment of the label text (default is 'center').
        """
        self.x = x
        self.label = label
        self.color = color
        self.horizontalalignment_text = horizontalalignment_text

    def __call__(self, ax) -> None:
        """
        Calls the draw method to render the vertical line.

        Parameters:
        ax (matplotlib.axes.Axes): The axes on which to draw the vertical line.
        """
        self.draw(ax)

    def draw(self, ax) -> None:
        """
        Draws the vertical line and its label on the specified axes.

        Parameters:
        ax (matplotlib.axes.Axes): The axes on which to draw the vertical line.
        """
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
    A class for drawing a moving average line plot.

    This class takes a DataFrame and a specified timestamp column to calculate and
    visualize the moving average of a time series.

    Attributes:
    data (pd.DataFrame): The input data containing the time series values.
    timestamp_col (str): The name of the column containing timestamp data for the x-axis.
    color (str): The color of the moving average line (default is 'gray').

    Methods:
    __call__(ax): Calls the draw method to render the moving average plot on the given axes.
    draw(ax): Draws the moving average line plot on the specified axes.
    """

    def __init__(self, data: pd.DataFrame, timestamp_col: str, color: str = 'gray'):
        """
        Initializes the MovingAverageLinePlot with the provided data and parameters.

        Parameters:
        data (pd.DataFrame): The input data containing the values to calculate the moving average.
        timestamp_col (str): The name of the column in the DataFrame to use as the x-axis (timestamp).
        color (str): The color of the moving average line (default is 'gray').
        """
        self.data = data
        self.timestamp_col = timestamp_col
        self.color = color

    def __call__(self, ax) -> None:
        """
        Calls the draw method to render the moving average plot.

        Parameters:
        ax (matplotlib.axes.Axes): The axes on which to draw the moving average line plot.
        """
        self.draw(ax)

    def draw(self, ax)->None:
        """
        Draws the graphical representation of the object on the provided Axes.

        Parameters:
        ax (matplotlib.axes.Axes): The Axes object on which to draw the graphical representation. 
                                    This should be an instance of matplotlib's Axes, which acts 
                                    as the plotting area for rendering data visualizations.

        Returns:
        None: This method modifies the Axes directly to include the graphical elements.
        """        
        self.data["moving_avg"] = self.data[self.timestamp_col].rolling(window=1).mean()
        sns.lineplot(data=self.data, x=self.data.index, y="moving_avg", ax=ax, color=self.color)


class Visualizer:
    """
    Manages the visualizations and receives data from the preprocessor.

    Args:
        preprocessor (Preprocessor): Class for preprocessing steps.
    """
    def __init__(self, preprocessor: Preprocessor):
        self.config = preprocessor.config
        self.preprocessor = preprocessor