
import numpy as np
import pandas as pd
from pathlib import Path
import seaborn as sns
import matplotlib.pyplot as plt
from wa_visualizer.settings import Config
from wa_visualizer.basic_plots import BasicPlot

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
