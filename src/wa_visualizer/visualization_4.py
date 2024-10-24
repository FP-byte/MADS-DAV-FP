import numpy as np
import pandas as pd
from pathlib import Path
import seaborn as sns
import matplotlib.pyplot as plt
from wa_visualizer.settings import Settings


class RelationshipsVisualization():
    #les 4: relationship visualization

    def __init__(self, data: pd.DataFrame, settings:Settings):
        self.settings = settings
        self.df = data
    
    def __call__(self):
        self.create_plot()

    def create_plot(self):
        # Calculate the average log length per author
        avg_log_length_withemoji = self.df.groupby('age')['message_length'].mean().reset_index()
        #avg_log_length_without_emoji = df_nem.groupby('age')['message_length'].mean().reset_index()

        # Regression line for average log length against age
        sns.regplot(data=avg_log_length_withemoji, x='age', y='message_length', marker='o', scatter_kws={'s': 60}, color='red')
        #sns.regplot(data=avg_log_length_without_emoji, x='age', y='message_length', marker='o', scatter_kws={'s': 100})

        # Add titles and labels
        plt.title("Getting Slower Fingers with age: Adults Save Typing Time with Emojis")
        plt.xlabel('Author Age')
        plt.ylabel('Average Log of Message Length containing Emoijs')
        plt.xticks()
        plt.grid()

        # Adjust layout
        plt.tight_layout()

        # Save the plot
        filename = self.settings.img_dir / Path("4_relationships_visualization.png")
        plt.savefig(filename, bbox_inches='tight', transparent=False)
        # Show the plot
        plt.show()        
        plt.close()