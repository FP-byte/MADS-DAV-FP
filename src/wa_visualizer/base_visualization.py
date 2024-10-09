import matplotlib.pyplot as plt
import seaborn as sns
from abc import ABC, abstractmethod

class BaseVisualization(ABC):
    def __init__(self, data):
        # Set default colors if none are provided
        self.data = data
        colors = ['#FF9999', '#66B3FF', '#99FF99']
        self.colors = colors if colors is not None else sns.color_palette("Set3", n_colors=len(data.columns))


    @abstractmethod
    def create_plot(self):
        pass

    def show(self):
        plt.show()

    def save(self, filename, transparent=False):
        plt.savefig(filename, bbox_inches='tight', transparent=transparent)

class ScatterPlot(BaseVisualization):
    def __init__(self, data, x, y, hue=None, style=None):
        super().__init__()
        self.x = x
        self.y = y
        self.hue = hue
        self.style = style

    def create_plot(self):
        plt.figure(figsize=(8, 6))
        sns.scatterplot(data=self.data, x=self.x, y=self.y, hue=self.hue, style=self.style)
        plt.title('Scatter Plot')
        plt.xlabel(self.x)
        plt.ylabel(self.y)
        plt.grid(True)

class Histogram(BaseVisualization):
    def __init__(self, data, column, bins=10):
        super().__init__()
        self.column = column
        self.bins = bins

    def create_plot(self):
        plt.figure(figsize=(8, 6))
        sns.histplot(self.data[self.column], bins=self.bins, kde=True)
        plt.title('Histogram')
        plt.xlabel(self.column)
        plt.ylabel('Frequency')
        plt.grid(True)

# Example usage:
if __name__ == "__main__":
    import pandas as pd

    # Sample data
    data = {
        'x': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        'y': [2, 3, 5, 7, 11, 13, 17, 19, 23, 29],
        'category': ['A', 'B', 'A', 'B', 'A', 'B', 'A', 'B', 'A', 'B']
    }
    df = pd.DataFrame(data)

    # Create a scatter plot
    scatter_plot = ScatterPlot(df, 'x', 'y', hue='category')
    scatter_plot.create_plot()
    scatter_plot.show()

    # Save the scatter plot
    scatter_plot.save('scatter_plot.png')

    # Create a histogram
    histogram = Histogram(df, 'x', bins=5)
    histogram.create_plot()
    histogram.show()

    # Save the histogram
    histogram.save('histogram.png')
