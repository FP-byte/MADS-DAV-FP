import numpy as np
from wa_visualizer.base_visualization import BaseVisualization
import seaborn as sns
import matplotlib.pyplot as plt

class RelationshipsVisualization(BaseVisualization):
    #les 4: relationship visualization

    def __init__(self, data):
        super().__init__(data)

    def create_plot(self):
        # Assign categories to each author
        category_mapping = {
            'effervescent-camel': 'teenager',
            'hilarious-goldfinch': 'adult',
            'nimble-wombat': 'adult',
            'spangled-rabbit': 'teenager'
        }
        self.data['category'] = self.data['author'].map(category_mapping)

        # Calculate the logarithm of message length
        self.data['log_len'] = np.log(self.data['message_length'])

        # Create a new column to categorize messages based on emoji presence
        self.data['emoji_status'] = self.data['has_emoji'].apply(lambda x: 'With Emoji' if x > 0 else 'Without Emoji')

        # Sort the DataFrame by author
        df_sorted = self.data.sort_values(by='author')

            
        # Create a FacetGrid
        g = sns.FacetGrid(df_sorted, col='emoji_status', hue='category', height=5, aspect=1.5, 
                          palette={'teenager': 'green', 'adult': 'lightgray'})

        # Map the scatter plot to each facet (note that x and y are swapped)
        g.map(sns.scatterplot, 'author', 'log_len', s=100)

        # Add count annotations
        for ax in g.axes.flat:
            # Get the title to determine the emoji status
            emoji_status = ax.get_title().split(' ')[0]  # "With" or "Without"
            
            # Filter the DataFrame based on the emoji status
            for i in range(df_sorted.shape[0]):
                if df_sorted['emoji_status'].iloc[i] == emoji_status:
                    ax.text(df_sorted['author'].iloc[i], df_sorted['log_len'].iloc[i], 
                            df_sorted['count'].iloc[i], fontsize=9, ha='right', va='center')

            # Add grid to the axes
            ax.grid(True)

        # Add titles and labels
        g.set_axis_labels('Author', 'Log of Message Length')
        g.set_titles(col_template='{col_name}')

        # Add a legend
        g.add_legend()

        # Adjust layout
        plt.subplots_adjust(top=0.85)
        g.fig.suptitle("The Emoji Age: Young People Trade Words for Visuals")
        plt.grid(True)
        filename = "./img/4_relationships_visualization.png"
        #plt.savefig(filename, bbox_inches='tight', transparent=False)
        #plt.close()

# Example usage
if __name__ == "__main__":
    # Sample DataFrame
    data = {
        'author': ['effervescent-camel', 'hilarious-goldfinch', 'nimble-wombat', 'spangled-rabbit'],
        'message_length': [36, 32, 31, 23],
        'has_emoji': [0.038, 0.085, 0.141, 0.011],
        'count': [1789, 964, 1858, 538]
    }
    df = pd.DataFrame(data)

    # Create the visualization instance
    visualization = RelationshipsVisualization(df)
    visualization.create_plot()
    visualization.show()