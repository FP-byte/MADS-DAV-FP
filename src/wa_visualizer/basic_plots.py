import matplotlib.pyplot as plt
from wa_visualizer.base_dataobj import FileHandler
import pandas as pd
from wa_visualizer.settings import Config
from pathlib import Path
from loguru import logger


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
    def __init__(self, config :Config,  title: str, xlabel: str, ylabel: str):
        self.title = title
        self.xlabel = xlabel
        self.ylabel = ylabel
        self.config = config

    def create_plot(self, x, y, **kwargs):
        """Create a scatter plot with optional additional parameters."""
        sns.scatterplot(x=x, y=y, ax=ax, **kwargs)

    def show_plot(self):
        plt.title(self.title)
        plt.xlabel(self.xlabel)
        plt.ylabel(self.ylabel)
        plt.tight_layout()
        plt.legend()
        plt.show()

    def save(self, filename: Path):
        filename = self.settings.img_dir / Path("1_categories_visualization.png")
        logger.info(f"Saving file to {filename}")
        self.fig.savefig(filename, bbox_inches='tight', transparent=False)
        plt.close(self.fig)  # Close the figure to free up memory

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

    