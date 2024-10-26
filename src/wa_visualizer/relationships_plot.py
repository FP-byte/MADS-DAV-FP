import numpy as np
import pandas as pd
from pathlib import Path
import seaborn as sns
import matplotlib.pyplot as plt
from wa_visualizer.settings import Config
from wa_visualizer.basic_plots import BasicPlot
#from wa_visualizer.basic_plots import RegPlot

# class RelationshipsPlot(RegPlot):
#     def __init__(self, config: Config, title: str, xlabel: str, ylabel: str, filename:str, show_legend:bool=False):
#         self.config = config
#         self.title = title
#         self.xlabel = xlabel
#         self.ylabel = ylabel
#         self.filename = filename
#         self.show_legend = show_legend
        
#     def __call__(self, data, x, y, **kwargs):
#          self.create_plot(data, x, y, **kwargs)
#          self.show_plot()
#          self.save()

#     def create_plot(self, data: pd.DataFrame, x :str, y :str, **kwargs):
#         # Create the regression plots
#         self.plot(data, x=x, y=y, scatter_size=60, color='red')

class RelationshipsPlot(BasicPlot):
    def __init__(self, config: Config, title_fig: str, xlabel: str, ylabel: str, filename: str, show_legend: bool = False):
        super().__init__(config, title_fig, xlabel, ylabel, filename, show_legend)  # Initialize superclass

    def __call__(self, data: pd.DataFrame, x: str, y: str, **kwargs):
        self.create_plot(data, x, y, **kwargs)  # Pass additional kwargs to create_plot
        

    def create_plot(self, data: pd.DataFrame, x: str, y: str, **kwargs):
        # Create a FacetGrid with a custom palette
        palette = {'With Emoji': 'blue', 'Without Emoji': 'orange'}
        g = sns.FacetGrid(data, col='emoji_status', hue='emoji_status', height=5, aspect=1.5, palette=palette)

        # Map the regression plot using the plot method from the RegPlot class
        g.map_dataframe(self.plot, x, y, scatter_size=60)

        # Set a main title above the grid
        g.fig.suptitle(self.title_fig, fontsize=16)

        # Set titles for each subplot correctly
        g.set_titles(col_template="Messages {col_name}")  # Customize if needed

        # Set axis labels
        g.set_axis_labels(self.xlabel, self.ylabel)

        # Adjust layout to avoid overlap with the main title
        plt.subplots_adjust(top=0.85)

        # Finally, show the plot
        plt.show()
        self.save()


        


       

    def plot(self, x: str, y: str, scatter_size: int, label: str = None, **kwargs):
        """Create a regression plot on each facet."""
        sns.regplot(x=x, y=y, marker='o', scatter_kws={'s': scatter_size}, label=label, **kwargs)
        plt.grid()
        #self.show_plot()
        #self.save()


# class RelationshipsPlot(RegPlot):
#     def __init__(self, config: Config, title: str, xlabel: str, ylabel: str, filename: str, show_legend: bool = False):
#         super().__init__(config, title, xlabel, ylabel, filename, show_legend=show_legend)  # Initialize superclass

#     def __call__(self, data: pd.DataFrame, x: str, y: str, color= "red"):
#         self.create_plot(data=data, x=x, y=y, color=color)
#         self.show_plot()
#         self.save()

#     def plot(self, data, x: str, y: str, scatter_size: int, **kwargs):
#         """Create a regression plot on each facet."""
#         sns.regplot(data=data, x=x, y=y, marker='o', scatter_kws={'s': scatter_size}, **kwargs)
#         plt.grid()

#     def create_plot(self, data: pd.DataFrame, x: str, y: str, **kwargs):
#         # Create a FacetGrid
#         g = sns.FacetGrid(data, col='emoji_status', height=5, aspect=1.5)

#         # Map the regression plot using the plot method from the RegPlot class
#         g.map_dataframe(self.plot, x, y, **kwargs)  # Pass any additional keyword arguments here

#         # Set titles and labels for each facet
#         g.set_titles(col_template="{col_name} Messages")
#         g.set_axis_labels(x, y)
#          # Set a main title above the grid
#         g.fig.suptitle("Average Log Length by Age and Emoji Status", fontsize=16)

#         # Adjust layout to avoid overlap with the main title
#         plt.subplots_adjust(top=0.85)

#     #def create_plot(self, plot_col,  data: pd.DataFrame, x: str, y: str, **kwargs):
#         # Create a FacetGrid
#       #  g = sns.FacetGrid(data1, col='emoji_status', hue='emoji_status', height=5, aspect=1.5)

#         # Map the regression plot using the plot method from the RegPlot class
#        # g.map(self.plot, x, y, scatter_size=60, **kwargs)
#       #  g.map(sns.scatterplot, 'age', 'log_len', s=100)
       # g.add_legend()
            
        # Set titles and labels
        # g.set_titles(col_template="{col_name}")
        #g.set_axis_labels(self.xlabel, self.ylabel)

        # Set a main title
       # plt.subplots_adjust(top=0.9)
       # g.fig.suptitle(self.title)

    


    

    
