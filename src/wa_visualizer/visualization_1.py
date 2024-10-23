
import seaborn as sns
import matplotlib.pyplot as plt
from pathlib import Path

class LanguageUsageVisualization():
    # Les 1: comparing categories

    def __init__(self, user_language_percentages, settings):
        self.user_language_percentages = user_language_percentages  # Initialize with the data for visualization
        self.settings = settings

    def __call__(self):
        self.create_plot()

    def create_plot(self):
        # Plotting
        ax = self.user_language_percentages.plot(kind='bar', stacked=False, figsize=(12, 8), color=self.settings.custom_colors)
        plt.title("Voices in Numbers: in Whatsapp ")
        plt.ylabel('Percentage')
        plt.xlabel('Author')
        plt.xticks(rotation=45)
        plt.legend(title='Communication type')

        # Annotate each bar with the percentage
        for p in ax.patches:
            ax.annotate(f'{p.get_height():.1f}%', 
                        (p.get_x() + p.get_width() / 2, p.get_height()), 
                        ha='center', va='bottom', 
                        fontsize=10)
        filename = self.settings.img_dir / Path("1_categories_visualization.png")
        plt.savefig(filename, bbox_inches='tight', transparent=False)
        plt.show()
        plt.close()
