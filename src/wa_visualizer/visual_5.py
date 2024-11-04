import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
from wa_visualizer.settings import Config
from wa_visualizer.basic_plots import BasicPlot
from wa_visualizer.data_processing import Preprocessor

class ScatterPlot(BasicPlot):
    """
    A class for creating scatter plots using Seaborn.

    Args:
        title_fig (str): Title of the figure.
        xlabel (str): Label for the x-axis.
        ylabel (str): Label for the y-axis.
        filename (str): Filename for saving the plot.
        figsize (tuple, optional): The size of the figure in inches (width, height). Default is (20, 8).
        custom_palette (list): Custom color palette for the scatter plot.
        metadata_lb (str, optional): Label for metadata used in hue. Defaults to "author".
        alpha (float, optional): Alpha transparency for the points. Defaults to 0.9.
    """
    def __init__(self, title_fig: str, xlabel: str, ylabel: str, filename: str, custom_palette: list, metadata_lb: str = "author", alpha: float = 0.9, figsize: tuple = (20, 8)):
        super().__init__(title_fig, xlabel, ylabel, filename, figsize)
        self.custom_palette = custom_palette
        self.metadata_lb = metadata_lb
        self.alpha = alpha

    def plot(self, X: np.ndarray, emb):
        """
        Plots a scatter plot using the given data and embeddings.

        Args:
            X (np.ndarray): Array of shape (n_samples, 2) containing the t-SNE coordinates.
            emb: Embeddings object containing metadata for labeling points.
        """
        labels = [emb.metadata[i][self.metadata_lb] for i in range(len(emb.metadata))]
        sns.scatterplot(x=X[:, 0], y=X[:, 1], hue=labels, palette=self.custom_palette, alpha=self.alpha)

        # Set the title, xlabel, and ylabel
        plt.title(self.title_fig)
        plt.xlabel(self.xlabel)
        plt.ylabel(self.ylabel)

        # Set ticks and grid
        plt.xticks(np.arange(np.min(X[:, 0]), np.max(X[:, 0]) + 1, step=10))  # Adjust steps for visualization
        plt.yticks(np.arange(np.min(X[:, 1]), np.max(X[:, 1]) + 1, step=10))
        plt.grid(True)

        # Show legend if applicable
        if self.show_legend:
            plt.legend(title=self.legend_title, bbox_to_anchor=(1.0, 1), loc='upper left')

        plt.tight_layout()


class TSNEPlotVisualizer:
    """
    Visualizes t-SNE scatter plots.

    Args:
        preprocessor (Preprocessor): Class responsible for preprocessing steps.
        custom_palette (list, optional): Custom color palette for the plots. Defaults to 'dark' color palette.
    """
    def __init__(self, preprocessor: Preprocessor, custom_palette: list = 'dark'):
        self.config = preprocessor.config
        self.preprocessor = preprocessor
        self.custom_palette = custom_palette

    def visualization_week5(self):
        """
        Creates a t-SNE scatter plot visualization for week 5 data.

        This method processes the data, applies the t-SNE algorithm,
        and generates scatter plots for verbal messages.
        """
        # Processing pipeline
        model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
        # Select subset with verbal messages
        subset_verbal = df[df["language"] != 'Non-verbal'].reset_index(drop=True)
        # Select subset with message log length above 3
        subset = subset_verbal[np.log(subset_verbal["message_length"]) >= 3].reset_index(drop=True)
        # Preprocessing step for t-SNE data
        X, emb = self.preprocessor.preprocess_week5(subset)  # Replace with actual method to get X and emb

        #create scatterplot with title and filename
        scatter_plot = ScatterPlot(
            title_fig='Focus en Flair: Gespreksonderwerpen die Ertoe Doen',
            xlabel='t-SNE Component 1',
            ylabel='t-SNE Component 2',
            filename='5_tsne_topics_visualization.png',
            custom_palette=['darkblue',  'gray', 'green', 'lightgray'],
            metadata_lb="topic"  
        )
        #plot data
        scatter_plot.plot(X, emb)
        #save plot
        scatter_plot.save()
        #show plot
        scatter_plot.show_plot()
        
        #create scatterplot with title and filename
        scatter_plot2 = ScatterPlot(
            title_fig='Smakelijke Gesprekken: Voedselgesprekken zijn makkelijker in het Italiaans',
            xlabel='t-SNE Component 1',
            ylabel='t-SNE Component 2',
            filename='5_tsne_language_visualization.png',
            custom_palette=['gray',  'green'],
            metadata_lb="language"  
        )

        #plot data
        scatter_plot2.plot(X, emb)
        #save plot
        scatter_plot2.save()
        #show plot
        scatter_plot2.show_plot()
