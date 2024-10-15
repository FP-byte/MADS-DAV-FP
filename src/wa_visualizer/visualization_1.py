from wa_visualizer.base_visualization import BaseVisualization
import seaborn as sns
import matplotlib.pyplot as plt

class LanguageUsageVisualization(BaseVisualization):
    # Les 1: comparing categories
    def __init__(self, data):
        super().__init__(data)

    def create_plot(self):
        # Grouping by author and language
        user_language_counts = self.data.groupby(['author', 'language']).size().unstack(fill_value=0)

        # Combine 'NL' and 'IT' into 'Verbal'
        user_language_counts['Verbal'] = user_language_counts[['NL', 'IT']].sum(axis=1)

        # Drop the original NL and IT columns
        user_language_counts.drop(['NL', 'IT'], inplace=True, axis=1)

        # Calculate the total counts for each author
        total_counts = user_language_counts.sum(axis=1)

        # Calculate percentages
        user_language_percentages = user_language_counts.div(total_counts, axis=0) * 100

        # Plotting
        ax = user_language_percentages.plot(kind='bar', stacked=False, figsize=(12, 8), color=self.colors)
        plt.title("Voices in Numbers: Words take over on WhatsApp")
        plt.ylabel('Percentage (%)')
        plt.xlabel('Author')
        plt.xticks(rotation=45)
        plt.legend(title='Communication type')

        # Annotate each bar with the percentage
        for p in ax.patches:
            ax.annotate(f'{p.get_height():.1f}%', 
                        (p.get_x() + p.get_width() / 2, p.get_height()), 
                        ha='center', va='bottom', 
                        fontsize=10)
        filename = "./img/1_categories_visualization.png"
        plt.savefig(filename, bbox_inches='tight', transparent=False)
        plt.close()
        

