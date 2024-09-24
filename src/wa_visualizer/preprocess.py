import click
import datetime
from pathlib import Path
import tomllib
from loguru import logger
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


class Visualizer:
    def __init__(self, datafile):
        self.datafile=datafile

    
    def calc_messages(self, df):
        topk = list(df[df["is_topk"]].author.unique())
        p = df.groupby("year-week").count()     #group by the isoweeks
        min_ts = df["timestamp"].min()
        max_ts = df["timestamp"].max()
        new_index = pd.date_range(start=min_ts, end=max_ts, freq='W', name="year-week").strftime('%Y-%W')
        return p.reindex(new_index, fill_value=0)


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

    def select_dates(self, df, start_date, end_date):
        if 'date' in df:
            # Select DataFrame rows between two dates
            mask = (df['date'] > start_date) & (df['date'] <= end_date)
            return df.loc[mask]
        else:
            logger('No date column to select')
            return None


    def prepoces_week2(self):
        df = pd.read_parquet(self.datafile)
        df["date"] = df["timestamp"].dt.date
        df["isoweek"] = df["timestamp"].dt.isocalendar().week
        df["year-week"] = df["timestamp"].dt.strftime("%Y-%W")

        
        # select data - start period
        start_date = datetime.datetime.strptime('2019-01-01', "%Y-%m-%d").date()
        # end period
        end_date = datetime.datetime.strptime('2023-01-01', "%Y-%m-%d").date()
        df = self.select_dates(df, start_date, end_date)

        # select corona data - start first lockdown
        start_date = datetime.datetime.strptime('2020-03-09', "%Y-%m-%d").date()
        # second lockdown
        end_date = datetime.datetime.strptime('2021-01-15', "%Y-%m-%d").date()

        df_corona = self.select_dates(df, start_date, end_date)
        
        return df, df_corona


    def visualization_week2(self):
        df, df_corona = self.prepoces_week2()
        p = self.calc_messages(df)
        p_corona = self.calc_messages(df_corona)
        self.visualize_timeseries(p, p_corona)

@click.command()
@click.option("--week", default="1", help="Device type: iOS or Android")
def main(week):    

    configfile = Path("./config.toml").resolve()
    print(configfile)

    with configfile.open("rb") as f:
        config = tomllib.load(f)

    datafile = (Path(".") / Path(config["processed"]) / config["current"]).resolve()
    if not datafile.exists():
        logger.warning("Datafile does not exist.")
    else:
        visualizer = Visualizer(datafile)

        if week.lower()=="1":
            visualizer.visualization_week1()
        if week.lower()=="2":
            visualizer.visualization_week2()

        if week.lower()=="3":
            visualizer.visualization_week3()

    
        


if __name__ == "__main__": 
    
    
      

        main()

