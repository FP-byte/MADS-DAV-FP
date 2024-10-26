
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from pathlib import Path
from wa_visualizer.settings import Config
from wa_visualizer.basic_plots import (BasicScatterPlot, VerticalLine, MovingAverageLinePlot)

import seaborn as sns
import pandas as pd

import matplotlib.pyplot as plt

class TimeSeriesPlot(BasicScatterPlot):
    def __init__(self, title: str, ylabel: str, xlabel: str, filename: str, config: Config, show_legend: bool = True):
        super().__init__(config, title, xlabel, ylabel, show_legend)  # Pass show_legend to the superclass
        self.filename = filename
        self.show_legend = show_legend
        #define custom colors for this plot
        self.color = 'gray'
        self.color_highlight = 'red'
        self.color_vertical_line = '#EEE'
        

    def __call__(self, p: pd.DataFrame, p_corona: pd.DataFrame, **kwargs):
        self.create_plot(p, p_corona, **kwargs)

    def create_plot(self, p: pd.DataFrame, p_corona: pd.DataFrame):
        _, ax = plt.subplots(figsize=(12, 6))

        # Scatter plots using Seaborn
        self.plot(p.index, p[self.config.timestamp_col], ax=ax, color = self.color )
        #define plot for corona time
        self.plot(p_corona.index, p_corona[self.config.timestamp_col], ax=ax, color = self.color_highlight)

        # Create moving average line plots
        moving_avg_plot_p = MovingAverageLinePlot(p, self.config.timestamp_col, color= self.color)
        #define plot for corona time
        moving_avg_plot_corona = MovingAverageLinePlot(p_corona, self.config.timestamp_col, color= self.color_highlight)
        
        moving_avg_plot_p.draw(ax)
        moving_avg_plot_corona.draw(ax)
        start = '2020-11'  # Start of restrictions
        end = '2021-01'    # End of restrictions

        # Define and draw vertical lines
        vertical_line_start = VerticalLine('2020-13', 'Start Intelligent lockdown', self.color_vertical_line, 'right')
        vertical_line_end = VerticalLine('2021-01', 'End Christmas lockdown', self.color_vertical_line, 'left')

        vertical_line_start.draw(ax)
        vertical_line_end.draw(ax)

        # Highlight the area between the two vertical lines
        ax.axvspan(vertical_line_start.x, vertical_line_end.x, color=self.color, alpha=0.1)     

        # Customize x-ticks
        interval = 5
        xticks = p.index[::interval]
        ax.set_xticks(xticks)
        ax.set_xticklabels(xticks, rotation=45, ha='right')


        # Save the plot
        filename = self.config.img_dir / Path(self.filename)
        plt.savefig(filename, bbox_inches='tight', transparent=False)
        self.show_plot()  # Show the plot with the legend setting
        plt.close()


