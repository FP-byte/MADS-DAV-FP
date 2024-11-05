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
    """
    A class for creating time series plots.

    Inherits from BasicScatterPlot and provides functionality to visualize time series data,
    including handling of moving averages and highlighting specific time periods.

    Args:
        title_fig (str): Title of the figure.
        ylabel (str): Label for the y-axis.
        xlabel (str): Label for the x-axis.
        filename (str): Filename for saving the plot.
        config (Config): Configuration object containing settings for the plot.
        show_legend (bool, optional): Flag indicating whether to display the legend. Defaults to True.
    """
    color: str
    color_highlight: str

    def __init__(self, title_fig: str, ylabel: str, xlabel: str, filename: str, config: Config, vert_line_text:list, vert_line_period:list,show_legend: bool = True):
        super().__init__(config, title_fig, xlabel, ylabel, show_legend)
        self.filename = filename
        self.show_legend = show_legend
        self.vertical_line_startdate = vert_line_period[0]
        self.vertical_line_enddate = vert_line_period[1]
        self.vertical_line_start_text = vert_line_text[0]
        self.vertical_line_end_text = vert_line_text[1]

    def __call__(self, p: pd.DataFrame, p_corona: pd.DataFrame, **kwargs):
        """
        Calls the create_plot method to generate the time series plot.

        Args:
            p (pd.DataFrame): Data for the main time series.
            p_corona (pd.DataFrame): Data for the highlighted time series during the pandemic.
            **kwargs: Additional arguments for customization.
        """
        self.create_plot(p, p_corona, **kwargs)

    def create_plot(self, p: pd.DataFrame, p_corona: pd.DataFrame):
        """
        Creates the time series plot.

        Args:
            p (pd.DataFrame): Data for the main time series.
            p_corona (pd.DataFrame): Data for the highlighted time series during the pandemic.
        """
        _, ax = plt.subplots(figsize=(12, 6))
        plt.title(self.title_fig)

        # Scatter plots using Seaborn
        self.plot(p.index, p[self.config.timestamp_col], ax=ax, color=self.color)
        # Define plot for corona time
        self.plot(p_corona.index, p_corona[self.config.timestamp_col], ax=ax, color=self.color_highlight)

        moving_avg_plot_p = self.plot_moving_average(p, self.config.timestamp_col, 7, ax, color=self.color)
        moving_avg_plot_corona = self.plot_moving_average(p_corona, self.config.timestamp_col, 7, ax, color=self.color_highlight)

        # Define and draw vertical lines
        vertical_line_start = VerticalLine(self.vertical_line_startdate, self.vertical_line_start_text, 'right')
        vertical_line_end = VerticalLine(self.vertical_line_enddate, self.vertical_line_end_text, 'left')

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
        # Define custom colors for this plot
        self.color = self.config.basic_color
        self.color_highlight = self.config.basic_color_highlight
        self.color_vertical_line = self.config.color_vertical_line

    def visualization_week2(self):
        """
        Creates a time series plot for week 2 data.
        This visualization focuses on the number of messages over time,
        particularly during the lockdown periods.
        """
        plot = TimeSeriesPlot(
            title_fig="Digitale stilte in tijden van lockdown",
            xlabel="Datum: jaar-week",
            ylabel="Aantal berichten",
            filename="2_timeseries_visualization.png",
            vert_line_period = ['2020-13', '2021-01'],
            vert_line_text = ['Start Intelligent lockdown', 'End Christmas lockdown'],
            show_legend=False,  # Do not show legend in this plot
            config=self.config
        )
        df_corona, df = self.preprocessor.preprocess_week2()
        p = self.preprocessor.calc_messages(df)
        p_corona = self.preprocessor.calc_messages(df_corona)
        plot(p, p_corona)

        