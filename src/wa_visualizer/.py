class RelationshipsPlotVisualizer(Visualizer):
    """
    Visualizes relationships in data.

    Args:
        preprocessor (Preprocessor): Class responsible for preprocessing steps.
    """

    def visualization_week4(self):
        """Creates a relationships plot for week 4 data."""
        avg_log_df = self.preprocessor.preprocess_week4()

        self.create_plot(
            RelationshipsPlot,
            title="Getting Slower Fingers with Age: Adults Save (Typing) Time with Emojis",
            xlabel='Author Age',
            ylabel='Average Log of Message Length',
            filename='4_relationships_visualization.png',
            data=avg_log_df,
            x='age',
            y='log_len',
            scatter_size=60
        )
