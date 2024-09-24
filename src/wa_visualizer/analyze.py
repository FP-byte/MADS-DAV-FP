import datetime

class Visualizer:
    
    def calc_messages(self, df):
        topk = list(df[df["is_topk"]].author.unique())
        p = df.groupby("year-week").count()     #group by the isoweeks
        min_ts = df["timestamp"].min()
        max_ts = df["timestamp"].max()
        new_index = pd.date_range(start=min_ts, end=max_ts, freq='W', name="year-week").strftime('%Y-%W')
        p = p.reindex(new_index, fill_value=0)
    return p

    def visualization_week2(self, p, p_corona):
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

    def visualization_week2(self, df):
        self.calc_messages(df)


if __name__ == "__main__":
    visual = Visualization()
    configfile = Path("../config.toml").resolve()

    with configfile.open("rb") as f:
        config = tomllib.load(f)

    datafile = (Path("..") / Path(config["processed"]) / config["current"]).resolve()
if not datafile.exists():
    logger.warning("Datafile does not exist. First run src/preprocess.py, and check the timestamp!")

    df = pd.read_parquet(datafile)

    df["date"] = df["timestamp"].dt.date
    df["isoweek"] = df["timestamp"].dt.isocalendar().week
    df["year-week"] = df["timestamp"].dt.strftime("%Y-%W")

    start_maatregelen = '2019-01-01'
    # eerste maatregel Covid - sluiting scholen braband
    start_date = datetime.datetime.strptime(start_maatregelen, "%Y-%m-%d").date()
    end_maatregelen = '2023-01-01'
    #21 mei 2022 maatregelen Covid-19 niet meer van kracht
    end_date = datetime.datetime.strptime(end_maatregelen, "%Y-%m-%d").date()

    # Select DataFrame rows between two dates
    mask = (df['date'] > start_date) & (df['date'] <= end_date)
    df = df.loc[mask]
    
    p = calc_messages(df)
    p_corona= calc_messages(df_corona)
    visualize_timeserie(p, p_corona)