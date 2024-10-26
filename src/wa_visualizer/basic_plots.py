import matplotlib.pyplot as plt
from wa_visualizer.base_dataobj import FileHandler
import pandas as pd
from wa_visualizer.settings import Config
from pathlib import Path
from loguru import logger
import seaborn as sns


class BasicBarPlot():
    def __init__(self, config :Config,  title: str, xlabel: str, ylabel: str):
        self.title = title
        self.xlabel = xlabel
        self.ylabel = ylabel
        self.config = config

    def create_plot(self, data):
        ax = data.percentages.plot(kind='bar', stacked=False, figsize=(12, 8), color=self.config.custom_colors)
        plt.bar(color=self.config.custom_color)
        plt.title(self.title)
        plt.xlabel(self.xlabel)
        plt.ylabel(self.ylabel)
        plt.xticks(rotation=45)
    
    def show_plot(self):
        plt.tight_layout()
        plt.show()

    def save(self, filename: Path):
        filename = self.settings.img_dir / Path("1_categories_visualization.png")
        logger.info(f"Saving file to {filename}")
        self.fig.savefig(filename, bbox_inches='tight', transparent=False)
        plt.close(self.fig)  # Close the figure to free up memory

class BasicScatterPlot:
    def __init__(self, config: Config, title: str, xlabel: str, ylabel: str, show_legend: bool = True):
        self.title = title
        self.xlabel = xlabel
        self.ylabel = ylabel
        self.config = config
        self.show_legend = show_legend  # Set the show_legend attribute

    def plot(self, x, y, **kwargs):
        """Create a scatter plot with optional additional parameters."""
        sns.scatterplot(x=x, y=y, **kwargs)

    def show_plot(self):
        plt.title(self.title)
        plt.xlabel(self.xlabel)
        plt.ylabel(self.ylabel)
        plt.tight_layout()
        if self.show_legend:  # Use the instance variable to check the legend visibility
            plt.legend()
        plt.show()

    def save(self, filename: Path):
        filename = self.config.img_dir / Path("1_categories_visualization.png")
        logger.info(f"Saving file to {filename}")
        plt.savefig(filename, bbox_inches='tight', transparent=False)
        plt.close()  # Close the figure to free up memory

class VerticalLine:
    def __init__(self, x: str, label: str, color: str = 'white', horizontalalignment_text='center' ):
        self.x = x
        self.label = label
        self.color = color
        self.horizontalalignment_text=horizontalalignment_text 

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

    def draw(self, ax):
        self.data["moving_avg"] = self.data[self.timestamp_col].rolling(window=1).mean()
        sns.lineplot(data=self.data, x=self.data.index, y="moving_avg", ax=ax, color=self.color)
        
# class BasicScatterPlot:
#     def __init__(self, title: str, xlabel: str, ylabel: str):
#         self.title = title
#         self.xlabel = xlabel
#         self.ylabel = ylabel

#     def create_plot(self, x, y, color='blue', label=None):
#         plt.scatter(x, y, color=color, label=label)

#     def show_plot(self):
#         plt.title(self.title)
#         plt.xlabel(self.xlabel)
#         plt.ylabel(self.ylabel)
#         plt.tight_layout()
#         plt.legend()
#         plt.show()

# class BasicScatterPlot:
#     def __init__(self, data: pd.DataFrame, config:Config):
#         self.data = data
#         self.fig, self.ax = plt.subplots(figsize=(10, 6))

#     def plot(self, title: str):
#         sns.scatterplot(data=self.data, x="x", y="y", ax=self.ax)
#         self.ax.set_title(title)

    
#     def save(self, filename: Path):
#         logger.info(f"Saving file to {filename}")
#         self.fig.savefig(filename)
#         plt.close(self.fig)  # Close the figure to free up memory

    