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

    def __init__(self, title_fig: str, xlabel: str, ylabel: str, filename: str, custom_palette: list, ax, hue: str, metadata_lb: str = "topic", alpha: float = 0.9, figsize=(20, 8)):
        super().__init__(title_fig, xlabel, ylabel, filename, figsize)
        self.custom_palette = custom_palette
        self.metadata_lb = metadata_lb
        self.alpha = alpha
        self.ax = ax  # Keep track of the axis for plotting

    def plot(self, X: np.ndarray, emb)->None:
        """
        Plots a scatter plot using the given data and embeddings on the specified axis.

        Args:
            X (np.ndarray): Array of shape (n_samples, 2) containing the t-SNE coordinates.
            emb: Embeddings object containing metadata for labeling points.
        Returns:
            None: The function displays the plot 
        """
        labels = [emb.metadata[i][self.metadata_lb] for i in range(len(emb.metadata))]
        
        # Pass ax explicitly to sns.scatterplot
        sns.scatterplot(x=X[:, 0], y=X[:, 1], hue=labels, palette=self.custom_palette, alpha=self.alpha, ax=self.ax)

        # Set the title, xlabel, and ylabel for the current axis
        self.ax.set_title(self.title_fig)
        self.ax.set_xlabel(self.xlabel)
        self.ax.set_ylabel(self.ylabel)

        # Set ticks and grid
        self.ax.set_xticks(np.arange(np.floor(np.min(X[:, 0])), np.ceil(np.max(X[:, 0])) + 1, step=20))  # Round to nearest integer
        self.ax.set_yticks(np.arange(np.floor(np.min(X[:, 1])), np.ceil(np.max(X[:, 1])) + 1, step=20))  # Round to nearest integer

        self.ax.grid(True)

        # If legend is needed, we can show it here
        self.ax.legend(title=self.legend_title, bbox_to_anchor=(1.0, 1), loc='upper left')


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

    def plot_all_tsne(self, X, emb, custom_palette='dark', alpha=0.9, filename='5_tsne_visualization.png')->None:
        """
        Creates two side-by-side t-SNE scatter plots for visualizing the clustering of data based on 
        topics and languages. The function uses the ScatterPlot class to create the plots and saves 
        them as image files. The first plot shows the distribution of topics, and the second shows 
        the distribution of languages.

        Args:
            X (np.ndarray): A 2D numpy array of shape (n_samples, 2) representing the t-SNE coordinates.
            emb (object): An object that contains metadata for labeling the points in the scatter plot.
                        It should have a `metadata` attribute that provides the 'topic' and 'language' labels.
            custom_palette (str or list, optional): A color palette to use for the scatter plot. Default is 'dark'.
            alpha (float, optional): The alpha transparency for the scatter plot points. Default is 0.9.
            filename (str, optional): The name of the file to save the visualizations. Default is '5_tsne_visualization.png'.

        Returns:
            None: The function displays the plot and saves the second plot to a file.
        """
        # Create subplots (1 row, 2 columns)
        fig, axs = plt.subplots(1, 2, figsize=(20, 8))  

        # Extract labels from metadata
        labels_1 = [emb.metadata[i][self.config.topic_col] for i in range(len(emb.metadata))]
        labels_2 = [emb.metadata[i][self.config.language_col] for i in range(len(emb.metadata))]

        # Create ScatterPlot instance for 'topic'
        scatter_plot_1 = ScatterPlot(
            title_fig='Focus en Flair: Gespreksonderwerpen die ertoe doen',
            xlabel='t-SNE Component 1',
            ylabel='t-SNE Component 2',
            filename='5_tsne_topics_visualization.png',
            metadata_lb="topic",
            custom_palette=['darkblue', 'gray', 'green', 'lightgray'],
            ax=axs[0],
            hue=labels_1
        )
        # Plot using the ScatterPlot object
        scatter_plot_1.plot(X, emb)

        # Create ScatterPlot instance for 'language'
        scatter_plot_2 = ScatterPlot(
            title_fig='Van pizza tot strand: Italiaans is de taal van eten en vakanties',
            xlabel='t-SNE Component 1',
            ylabel='t-SNE Component 2',
            filename='5_tsne_visualization.png',
            metadata_lb="language",
            custom_palette=['darkblue', 'green'],
            ax=axs[1],
            hue=labels_2
        )
        # Plot using the ScatterPlot object
        scatter_plot_2.plot(X, emb)
        
        # Save the second plot
        scatter_plot_2.save()

        # Set ticks and grid for the whole figure
        # Adjust the xticks and yticks and round to nearest integer for a clean layout
        plt.xticks(np.arange(np.floor(np.min(X[:, 0])), np.ceil(np.max(X[:, 0])) + 1, step=20))  
        plt.yticks(np.arange(np.floor(np.min(X[:, 1])), np.ceil(np.max(X[:, 1])) + 1, step=20))  
        plt.grid(True)

        # Adjust layout and show plot
        plt.tight_layout()
        plt.show()

      
    def visualization_week5(self):
        """
        Creates a t-SNE scatter plot visualization for week 5 data.

        This method processes the data, applies the t-SNE algorithm,
        and generates scatter plots for verbal messages.
        """
        # Processing pipeline
        model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
        # Select subset with verbal messages
        subset_verbal = df[df[self.config.language_col] != self.config.nonverbal_cat].reset_index(drop=True)
        # Select subset with message log length above 3
        subset = subset_verbal[np.log(subset_verbal[self.config.message_length_col]) >= 3].reset_index(drop=True)
        # Preprocessing step for t-SNE data
        X, emb = self.preprocessor.preprocess_week5(subset)  # Replace with actual method to get X and emb

        #create double scatterplot with title and filename
        self.plot_all_tsne(X, emb)
        
