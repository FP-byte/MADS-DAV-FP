def visualization_relationships(df):
    
    # Assign categories to each author
        category_mapping = {
            'effervescent-camel': 'teenager',
            'hilarious-goldfinch': 'adult',
            'nimble-wombat': 'adult',
            'spangled-rabbit': 'teenager'
        }
        df['category'] = df['author'].map(category_mapping)

        # Calculate the logarithm of message length
        df['log_len'] = np.log(df['message_length'])

        # Create a new column to categorize messages based on emoji presence
        df['emoji_status'] = df['has_emoji'].apply(lambda x: 'With Emoji' if x > 0 else 'Without Emoji')

        # Sort the DataFrame by author
        df_sorted = df.sort_values(by='author')

        # Create the scatter plot
        plt.figure(figsize=(8, 6), facecolor='white')  
        # Create a FacetGrid
        g = sns.FacetGrid(df_sorted, col='emoji_status', hue='category', height=5, aspect=1.5, palette={'teenager': 'green', 'adult': 'lightgray'})

        # Map the scatter plot to each facet (note that x and y are swapped)
        g.map(sns.scatterplot, 'author', 'log_len', s=100)

        # Add count annotations
        for ax in g.axes.flat:
            # Get the title to determine the emoji status
            emoji_status = ax.get_title().split(' ')[0]  # "With" or "Without"
            
            # Filter the DataFrame based on the emoji status
            for i in range(df_sorted.shape[0]):
                if df_sorted['emoji_status'].iloc[i] == emoji_status:
                    ax.text(df_sorted['author'].iloc[i], df_sorted['log_len'].iloc[i], df_sorted['count'].iloc[i], 
                            fontsize=9, ha='right', va='center')

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

        # Save the plot with an opaque background
        plt.savefig('4_scatter_plot_with_emojis.png', bbox_inches='tight', transparent=False)
        # Show the plot
        plt.show()