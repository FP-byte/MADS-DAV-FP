import pandas as pd
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from wa_visualizer.settings import Config
from wa_visualizer.basic_plots import (BasicScatterPlot, VerticalLine, MovingAverageLinePlot)
from wa_visualizer.data_processing import Preprocessor
from loguru import logger

class TimeSeriesPlot(BasicScatterPlot):
    color:str
    color_highlight:str

    def __init__(self, title_fig: str, ylabel: str, xlabel: str, filename: str, config: Config, show_legend: bool = True):
        super().__init__(config, title_fig, xlabel, ylabel, show_legend)  # Pass show_legend to the superclass
        self.filename = filename
        self.show_legend = show_legend
  

    def __call__(self, p: pd.DataFrame, p_corona: pd.DataFrame, **kwargs):
        self.create_plot(p, p_corona, **kwargs)

    def create_plot(self, p: pd.DataFrame, p_corona: pd.DataFrame):
        _, ax = plt.subplots(figsize=(12, 6))
        plt.title(self.title_fig)

        # Scatter plots using Seaborn
        self.plot(p.index, p[self.config.timestamp_col], ax=ax, color = self.color )
        #define plot for corona time
        self.plot(p_corona.index, p_corona[self.config.timestamp_col], ax=ax, color = self.color_highlight)

        moving_avg_plot_p = self.plot_moving_average(p, self.config.timestamp_col, 7, ax, color = self.color)
        moving_avg_plot_corona = self.plot_moving_average(p_corona, self.config.timestamp_col, 7, ax, color = self.color_highlight)

        # Define and draw vertical lines
        vertical_line_start = VerticalLine('2020-13', 'Start Intelligent lockdown', 'right')
        vertical_line_end = VerticalLine('2021-01', 'End Christmas lockdown', 'left')

        vertical_line_start(ax)
        vertical_line_end(ax)

        # Highlight the area between the two vertical lines
        ax.axvspan(vertical_line_start.x, vertical_line_end.x, color=self.color, alpha=0.1)     

        # Customize x-ticks
        interval = 5
        xticks = p.index[::interval]
        ax.set_xticks(xticks)
        ax.set_xticklabels(xticks, rotation=45, ha='right')


        # Save the plot
        filename = self.config.img_dir / Path(self.filename)
        #plt.savefig(filename, bbox_inches='tight', transparent=False)
        self.save()
        self.show_plot()  # Show the plot with the legend setting


class TimeSeriesPlotVisualizer(Preprocessor):
    """
    Visualizes data using time series plots.

    Args:
        preprocessor (Preprocessor): Class responsible for preprocessing steps.
    """
    def __init__(self, preprocessor: Preprocessor):
        self.config = preprocessor.config
        self.preprocessor = preprocessor
        #define custom colors for this plot
        self.color = self.config.basic_color
        self.color_highlight = self.config.basic_color_highlight
        self.color_vertical_line = self.config.color_vertical_line

    def visualization_week2(self):
        """Creates a time series plot for week 2 data."""
        plot = TimeSeriesPlot(
            title_fig="Digitale stilte in tijden van lockdown",
            xlabel="Date: year-week",
            ylabel="Number of messages",
            filename="2_timeseries_visualization.png",
            show_legend=False,  # do not show legend in this plot
            config=self.config
        )
        df_corona, df = self.preprocessor.preprocess_week2()
        p = self.preprocessor.calc_messages(df)
        p_corona = self.preprocessor.calc_messages(df_corona)
        plot(p, p_corona)

        