import matplotlib.pyplot as plt
from wa_visualizer.base_dataobj import FileHandler
import pandas as pd
from wa_visualizer.settings import Config
from pathlib import Path
from loguru import logger
import seaborn as sns

class BasicPlot:
    def __init__(self, config: Config, title: str, xlabel: str, ylabel: str, filename: str, figsize=(12, 8), show_legend: bool = True):
        self.config = config
        self.title = title
        self.xlabel = xlabel
        self.ylabel = ylabel
        self.filename = filename
        self.show_legend = show_legend
    
    def plot(self, data: pd.DataFrame):
        #to define for each plot
        pass

    def show_plot(self):
        plt.title(self.title)
        plt.xlabel(self.xlabel)
        plt.ylabel(self.ylabel)
        plt.tight_layout()
        if self.show_legend:
            plt.legend()
        plt.show()

    def save(self):
        filepath = self.config.img_dir / Path(self.filename)
        plt.savefig(filepath, bbox_inches='tight', transparent=False)
        plt.close()  # Close the figure to free up memory

class BasicScatterPlot(BasicPlot):
    def __init__(self, config: Config, title: str, xlabel: str, ylabel: str, filename: str, show_legend: bool = True):
        super().__init__(config, title, xlabel, ylabel, filename, show_legend)

    def plot(self, x, y, **kwargs):
        """Create a scatter plot with optional additional parameters."""
        sns.scatterplot(x=x, y=y, **kwargs)

    def plot_moving_average(self, data: pd.DataFrame, timestamp_col: str, window: int, ax, color: str):
        """Calculate and plot the moving average."""
        data['moving_avg'] = data[timestamp_col].rolling(window=window).mean()
        moving_avg_plot = MovingAverageLinePlot(data, self.config.timestamp_col, color=color)       
        moving_avg_plot(ax)

class BarPlot(BasicPlot):
    def __init__(self, config: Config, title: str, ylabel: str, xlabel: str, filename: str, legend_title: str = ""):
        super().__init__(config, title, xlabel, ylabel, filename)
        self.legend_title = legend_title

    def __call__(self, data, stacked: bool):
        self.plot(data, stacked)
        self.show_plot()
        self.save()

    def plot(self, data: pd.DataFrame, stacked: bool = False):
        # Plotting
        ax = data.plot(kind='bar', stacked=stacked, figsize=(12, 8), color=self.config.custom_colors)
        plt.title(self.title)
        plt.ylabel(self.ylabel)
        plt.xlabel(self.xlabel)
        plt.xticks(rotation=45)
        plt.legend(title=self.legend_title, bbox_to_anchor=(1.00, 1), loc='upper left')

class RegPlot(BasicPlot):
    def __init__(self, config: Config, title: str, xlabel: str, ylabel: str, filename: str, figsize=(20, 10), show_legend: bool = True):
        super().__init__(config, title, xlabel, ylabel, filename, show_legend)

    def __call__(self, data: pd.DataFrame, x: str, y: str, **kwargs):
        self.plot(data, x, y, **kwargs)
        self.show_plot()
        self.save()

    def plot(self, data: pd.DataFrame, x: str, y: str, scatter_size: int, color: str, label: str = None):
        """Create a regression plot."""
        sns.regplot(data=data, x=x, y=y, marker='o', scatter_kws={'s': scatter_size}, color=color, label=label)
        plt.grid()


class VerticalLine:
    def __init__(self, x: str, label: str, color: str = 'white', horizontalalignment_text='center' ):
        self.x = x
        self.label = label
        self.color = color
        self.horizontalalignment_text=horizontalalignment_text 

    def __call__(self, ax):
        self.draw(ax)

    def draw(self, ax):
        ax.axvline(x=self.x, linestyle='--', label=self.label, color=self.color, zorder=1)
        
        # Get the current limits of the y-axis
        y_limits = ax.get_ylim()
        # Calculate the y position with the specified offset
        y_position = y_limits[1] * 0.8
        
        ax.text(self.x, y_position, self.label, color='red', 
                horizontalalignment=self.horizontalalignment_text, fontsize=10, rotation=90, 
                verticalalignment='top', zorder=2)


class MovingAverageLinePlot:
    def __init__(self, data: pd.DataFrame, timestamp_col: str, color: str = 'gray'):
        self.data = data
        self.timestamp_col = timestamp_col
        self.color = color

    def __call__(self, ax):
        self.draw(ax)

    def draw(self, ax):
        self.data["moving_avg"] = self.data[self.timestamp_col].rolling(window=1).mean()
        sns.lineplot(data=self.data, x=self.data.index, y="moving_avg", ax=ax, color=self.color)
    