import matplotlib.pyplot as plt
from wa_visualizer.base_visualization import BaseVisualization
import seaborn as sns
import matplotlib.pyplot as plt

import pandas as pd
import matplotlib.pyplot as plt

class BaseVisualization:
    def __init__(self, data):
        self.data = data

    def show(self):
        plt.show()

class StackPlotVisualization(BaseVisualization):
    def __init__(self, data):
        super().__init__(data)

    def create_plot(self):
        # Normalize the data to get percentages
        total_counts = self.data.sum(axis=1)
        print("Total counts per hour:", total_counts)
        
        # Normalize each column by dividing by the total counts for that hour
        normalized_data = self.data.div(total_counts, axis=0) * 100
        
        # Check normalized data
        print("Normalized data (%):", normalized_data)

        plt.figure(figsize=(12, 6))
        
        # Define custom colors
        colors = ['red', 'gray', 'darkgray', 'lightgray', 'white']
        
        # Create the stack plot
        plt.stackplot(normalized_data.index, normalized_data.T, colors=colors, labels=self.data.columns, alpha=0.6)
        
        # Title and labels
        plt.title("Feeding the Dialogue: How Hunger Fuels Food Conversations")
        plt.xlabel('Hour of Day')
        plt.ylabel('Percentage of Messages About Topic (%)')
        
        plt.xticks(normalized_data.index, rotation=45)
        
        # Add a legend with a title
        plt.legend(loc='upper left', title='Topics')
        plt.grid()
        
        # Save the plot
        filename = "./img/3_distribution_visualization.png"
        #plt.savefig(filename, bbox_inches='tight', transparent=False)
        #plt.close()

# Example usage
if __name__ == "__main__":
    # Sample DataFrame
    hours = range(24)  # Example for 24 hours
    df_counts = pd.DataFrame({
        'Food': [1, 2, 3, 4, 5, 1, 2, 3, 4, 5, 6, 5, 4, 3, 2, 1, 0, 1, 2, 3, 4, 5, 6, 7],
        'Drink': [2, 3, 4, 1, 0, 1, 2, 3, 4, 2, 1, 0, 1, 2, 3, 4, 5, 6, 7, 1, 2, 3, 4, 5],
        'Snack': [0, 1, 2, 1, 0, 1, 0, 1, 2, 3, 2, 1, 0, 1, 2, 3, 4, 5, 6, 7, 1, 2, 1, 0]
    }, index=hours)

    # Create the visualization instance
    visualization = StackPlotVisualization(df_counts)
    visualization.create_plot()
    visualization.show()
