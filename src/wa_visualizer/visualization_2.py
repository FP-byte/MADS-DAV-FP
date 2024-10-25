
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from pathlib import Path
from wa_visualizer.settings import Config
from wa_visualizer.basic_plots import BasicScatterPlot

class TimeSeriesPlot(BasicScatterPlot):
    def __init__(self, title: str, ylabel: str, xlabel: str, filename:str, config:Config):
        super().__init__(self, title, xlabel, ylabel)
        self.config = config

    def __call__(self, p :pd.DataFrame, p_corona:pd.DataFrame, **kwargs):
        self.create_plot(p, p_corona, **kwargs)

    def create_plot(self, p :pd.DataFrame, p_corona:pd.DataFrame, **kwargs):
        _, ax = plt.subplots(figsize=(12, 6))

        # Scatter plots using Seaborn
        self.create_plot(p.index, p[self.config.timestamp_col], color='gray', ax=ax)
        self.create_plot(p_corona.index, p_corona[self.config.timestamp_col], ax=ax)

        # Calculate moving averages
        p["moving_avg"] = p[self.config.timestamp_col].rolling(window=1).mean()
        p_corona["moving_avg"] = p_corona[self.config.timestamp_col].rolling(window=1).mean()

        # Line plots for moving averages
        sns.lineplot(data=p, x=p.index, y="moving_avg", ax=ax, color='gray')
        sns.lineplot(data=p_corona, x=p_corona.index, y="moving_avg", ax=ax)

        # Define the x-coordinates for the vertical lines
        start = '2020-11'  # Start of restrictions
        end = '2021-01'    # End of restrictions

        # Add vertical lines
        ax.axvline(x=start, linestyle='--', label='Start corona-restrictions', color='white')
        ax.axvline(x=end, linestyle='--', label='End corona-restrictions', color='white')

        # Label the vertical lines
        ax.text(start, ax.get_ylim()[1] * 0.9, 'Intelligent lockdown', color='red', 
                horizontalalignment='right', fontsize=10, rotation=90, verticalalignment='top')
        ax.text(end, ax.get_ylim()[1] * 0.9, 'Christmas lockdown', color='red', 
                horizontalalignment='left', fontsize=10, rotation=90, verticalalignment='top')

        # Highlight the area between the two vertical lines
        ax.axvspan(start, end, color='gray', alpha=0.1)

        # Customize x-ticks
        interval = 4
        xticks = p.index[::interval]
        ax.set_xticks(xticks)
        ax.set_xticklabels(xticks, rotation=45, ha='right')

        # Save the plot
        filename = self.config.img_dir / Path(filename)
        plt.savefig(filename, bbox_inches='tight', transparent=False)
        self.show_plot()
        plt.close()

