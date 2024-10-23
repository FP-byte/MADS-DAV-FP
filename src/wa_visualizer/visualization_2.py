
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from pathlib import Path

class TimeSeriesVisualization():
    #Les 2: Time Series visualization

    def __init__(self, p, p_corona, settings):
        self.p = p
        self.p_corona = p_corona

    def __call__(self):
        self.create_plot()

    def create_plot(self):
        _, ax = plt.subplots(figsize=(12, 6))

        # Scatter plots
        sns.scatterplot(data=self.p, x=self.p.index, y="timestamp", ax=ax, color='gray')
        sns.scatterplot(data=self.p_corona, x=self.p_corona.index, y="timestamp", ax=ax)

        # Calculate moving averages
        self.p["moving_avg"] = self.p["timestamp"].rolling(window=1).mean()
        self.p_corona["moving_avg"] = self.p_corona["timestamp"].rolling(window=1).mean()

        # Line plots for moving averages
        sns.lineplot(data=self.p, x=self.p.index, y="moving_avg", ax=ax, color='gray')
        sns.lineplot(data=self.p_corona, x=self.p_corona.index, y="moving_avg", ax=ax)

        # Define the x-coordinates for the vertical lines
        start = '2020-11'  # Start of restrictions
        end = '2021-01'    # End of restrictions

        # Add vertical lines
        ax.axvline(x=start, linestyle='--', label='Start corona-restrictions', color='gray')
        ax.axvline(x=end, linestyle='--', label='End corona-restrictions', color='gray')

        # Label the vertical lines
        ax.text(start, ax.get_ylim()[1] * 0.9, 'Intelligent lockdown', color='red', 
                horizontalalignment='right', fontsize=10, rotation=90, verticalalignment='top')
        ax.text(end, ax.get_ylim()[1] * 0.9, 'Christmas lockdown', color='red', 
                horizontalalignment='left', fontsize=10, rotation=90, verticalalignment='top')

        # Highlight the area between the two vertical lines
        ax.axvspan(start, end, color='gray', alpha=0.1)

        # Customize x-ticks
        interval = 4
        xticks = self.p.index[::interval]
        ax.set_xticks(xticks)
        ax.set_xticklabels(xticks, rotation=45, ha='right')

        # Add title and legend
        plt.title("Digital Silence: The WhatsApp Whisper During Lockdown")
        ax.legend()
        filename = self.settings.img_dir / Path("2_timeseries_visualization.png")
        plt.savefig(filename, bbox_inches='tight', transparent=False)
        plt.show()
        plt.close()

# Example usage
if __name__ == "__main__":
    # Sample data (replace with actual DataFrame)
    dates = pd.date_range(start='2020-01-01', end='2021-12-31', freq='W')
    p = pd.DataFrame({
        'timestamp': [1, 2, 3, 4] * 26,
    }, index=dates[:104])  # Just for demonstration

    p_corona = pd.DataFrame({
        'timestamp': [1, 2, 3, 4] * 26,
    }, index=dates[104:])  # Just for demonstration

    # Create the visualization instance
    visualization = TimeSeriesVisualization(p, p_corona)
    visualization.create_plot()
    visualization.show()