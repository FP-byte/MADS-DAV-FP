def visualize_timeseries(self, p, p_corona):
        fig, ax = plt.subplots(figsize=(12, 6))
        sns.scatterplot(data=p, x=p.index, y="timestamp", ax=ax, color='lightblue')
        sns.scatterplot(data=p_corona, x=p_corona.index, y="timestamp", ax=ax)

        p["moving_avg"] = p["timestamp"].rolling(window=1).mean()
        p_corona["moving_avg"] = p_corona["timestamp"].rolling(window=1).mean()
        sns.lineplot(data=p, x=p.index, y="moving_avg", ax=ax, color='lightblue')
        sns.lineplot(data=p_corona, x=p_corona.index, y="moving_avg", ax=ax)

        # Define the x-coordinates for the vertical lines (start and end of the period)
        start = '2020-11' #Tijdelijk verbod passagiersvluchten uit risicogebieden
        end = '2021-01' #lockdown_feestdagen


        # Add vertical lines
        ax.axvline(x=start,  linestyle='--', label='Start corona-beperkingen')
        ax.axvline(x=end,  linestyle='--', label='End corona-beperkingen')

        # Highlight the area between the two vertical lines
        #ax.axvspan(start_x, end_x, color='gray', alpha=0.3)
        intelligente_lockdown = '2020-11' #Tijdelijk verbod passagiersvluchten uit risicogebieden
        lockdown_feestdagen = '2020-51'
        
        # Label the vertical lines

        ax.text(intelligente_lockdown, ax.get_ylim()[1] * 0.9, 'Intelligent lockdown', color='red', 
                horizontalalignment='right', fontsize=8, rotation=90, verticalalignment='top')  
        ax.text(lockdown_feestdagen, ax.get_ylim()[1] * 0.9, 'Christmas lockdown', color='red', 
                horizontalalignment='center', fontsize=8, rotation=90, verticalalignment='top')    

        # Highlight the area between the two vertical lines
        ax.axvspan(start, end, color='gray', alpha=0.1)

        # Customize x-ticks
        interval = 4
        xticks = p.index[::interval]
        ax.set_xticks(xticks)
        ax.set_xticklabels(xticks, rotation=45, ha='right')

        # Add title and legend
        plt.title("Digital Silence: The WhatsApp Whisper During Lockdown")
        #ax.legend()

        plt.show()

# Example usage
if __name__ == "__main__":
    # Sample data
    data = {
        'author': ['Alice', 'Bob', 'Charlie', 'Alice', 'Bob', 'Charlie'],
        'language': ['NL', 'IT', 'IT', 'NL', 'NL', 'IT']
    }
    df = pd.DataFrame(data)

    # Create a visualization instance with a custom color palette
    custom_colors = ['#FF9999', '#66B3FF', '#99FF99']
    visualization = LanguageUsageVisualization()
    visualization.create_plot()
    visualization.show()