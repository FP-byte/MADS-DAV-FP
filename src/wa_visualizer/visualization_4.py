import numpy as np
import pandas as pd
from wa_visualizer.base_visualization import BaseVisualization
import seaborn as sns
import matplotlib.pyplot as plt

class RelationshipsVisualization(BaseVisualization):
    #les 4: relationship visualization

    def __init__(self, data):
        super().__init__(data)

    def create_plot(self, df):
        # Calculate the average log length per author
        avg_log_length_withemoji = df.groupby('age')['message_length'].mean().reset_index()
        #avg_log_length_without_emoji = df_nem.groupby('age')['message_length'].mean().reset_index()

        # Create the regression plot
        #plt.figure(figsize=(10, 6), facecolor='white')

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
        filename = "./img/4_relationships_visualization.png"
        plt.savefig(filename, bbox_inches='tight', transparent=False)

        plt.savefig(filename, bbox_inches='tight', transparent=False)
        # Show the plot
        plt.show()        
        plt.close()