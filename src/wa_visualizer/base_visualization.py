import matplotlib.pyplot as plt
import seaborn as sns
from abc import ABC, abstractmethod
from loguru import logger
#
class BaseVisualization(ABC):
    def __init__(self, data):
        # Set default colors if none are provided
        self.data = data
        colors = ['lightgray', 'salmon', 'gray']
        self.colors = colors if colors is not None else sns.color_palette("Set3", n_colors=len(data.columns))


    @abstractmethod
    def create_plot(self):
        pass

    def show(self):
        plt.show()

    def save(self, filename, transparent=False):
        plt.savefig(filename, bbox_inches='tight', transparent=transparent)
        plt.close()


