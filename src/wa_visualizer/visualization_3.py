import matplotlib.pyplot as plt
import pandas as pd

from wa_visualizer.base_visualization import BaseVisualization

class PlotVisualization(BaseVisualization):
    """Class for stackplots""" 
    def __init__(self, data, df_normalized : pd.DataFrame):
        super().__init__(data)
        self.df_normalized = df_normalized 

    def create_plot(self)-> None:
        """
        Create distribution
        """        
             
        # Plot the normalized data
        self.df_normalized.plot(kind='bar', stacked=True, color=[ 'black', 'gray',  'darkgray','salmon',  'lightgray', ], alpha=0.7, figsize=(10, 8),)

        # Titles and labels
        plt.title('Are you Coming Home? Late-Night WhatsApp Chats with Teens', fontsize=12)
        plt.xlabel('Hour of the Day', fontsize=9)
        plt.ylabel('Percentage of Total Messages', fontsize=12)
        plt.xticks(rotation=0)
        plt.legend(title='Topics', fontsize=9)

        # Set more y-ticks
        #plt.gca().yaxis.set_major_locator(plt.MaxNLocator(20))  # Show up to 10 ticks on y-axis
        #plt.gca().yaxis.set_major_locator(plt.MultipleLocator(20))  # Set a specific interval for y-ticks (e.g., every 10)
        # Legend placed outside the plot
        plt.legend(title='Topics', bbox_to_anchor=(1.00, 1), loc='upper left', fontsize=10)
        plt.grid(axis='y')

        # Show the plot
        plt.tight_layout()
        plt.show()
        
        # Save the plot
        filename = "./img/3_distribution_visualization.png"
        plt.savefig(filename, bbox_inches='tight', transparent=False)
        plt.close('all')


