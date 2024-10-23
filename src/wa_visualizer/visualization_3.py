import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path



class PlotVisualization():
    """Class for stackplots""" 
    def __init__(self, df_normalized : pd.DataFrame, settings):
        self.df_normalized = df_normalized
        self.settings = settings
    
    def __call__(self):
        self.create_plot()

    def create_plot(self)-> None:
        """
        Create distribution
        """           
        # Plot the normalized data
        self.df_normalized.plot(kind='bar', stacked=True, color=self.settings.custom_colors, alpha=0.7, figsize=(10, 8),)

        # Titles and labels
        plt.title('Are you Coming Home? Late-Night WhatsApp Chats with Teens', fontsize=12)
        plt.xlabel('Hour of the Day', fontsize=9)
        plt.ylabel('Percentage of Total Messages', fontsize=12)
        plt.xticks(rotation=0)
        plt.legend(title='Topics', fontsize=9)

         # Legend placed outside the plot
        plt.legend(title='Topics', bbox_to_anchor=(1.00, 1), loc='upper left', fontsize=10)
        plt.grid(axis='y')

        # Show the plot
        plt.tight_layout()
        
        
        # Save the plot
        filename = self.settings.img_dir / Path("2_timeseries_visualization.png")
        plt.savefig(filename, bbox_inches='tight', transparent=False)
        plt.show()
        plt.close()


