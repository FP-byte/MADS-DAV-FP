import numpy as np
import pandas as pd
from pathlib import Path
import seaborn as sns
import matplotlib.pyplot as plt
from wa_visualizer.settings import Config
from wa_visualizer.basic_plots import RegPlot

class RelationshipsVisualization(RegPlot):
    def __init__(self, config: Config, title: str, xlabel: str, ylabel: str, filename:str, show_legend:bool=False):
        self.config = config
        self.title = title
        self.xlabel = xlabel
        self.ylabel = ylabel
        self.filename = filename
        self.show_legend = show_legend
        
    def __call__(self, data, x, y, **kwargs):
         self.create_plot(data, x, y, **kwargs)
         self.show_plot()
         self.save()

    def create_plot(self, data: pd.DataFrame, x :str, y :str, **kwargs):
        # Create the regression plots
        self.plot(data, x=x, y=y, scatter_size=30, color='red')



# class RelationshipsVisualization():
#     #les 4: relationship visualization

#     def __init__(self, data: pd.DataFrame, config:Config):
#         self.config = config
#         self.df = data
    
#     def __call__(self):
#         self.create_plot()

#     def create_plot(self):
#         # Calculate the average log length per author
#         avg_log_length_withemoji = self.df.groupby('age')[self.config.message_length_col].mean().reset_index()
#         avg_log_length_without_emoji = df_nem.groupby('age')[self.config.message_length_col].mean().reset_index()

#         # Regression line for average log length against age
#         sns.regplot(data=avg_log_length_withemoji, x='age', y=self.config.message_length_col, marker='o', scatter_kws={'s': 60}, color='red')
#         sns.regplot(data=avg_log_length_without_emoji, x='age', y=self.config.message_length_col, marker='o', scatter_kws={'s': 100})

#         # Add titles and labels
#         plt.title("Getting Slower Fingers with age: Adults Save Typing Time with Emojis")
#         plt.xlabel('Author Age')
#         plt.ylabel('Average Log of Message Length containing Emoijs')
#         plt.xticks()
#         plt.grid()

#         # Adjust layout
#         plt.tight_layout()

#         # Save the plot
#         filename = self.config.img_dir / Path("4_relationships_visualization.png")
#         plt.savefig(filename, bbox_inches='tight', transparent=False)
#         # Show the plot
#         plt.show()        
#         plt.close()