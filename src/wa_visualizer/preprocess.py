from analyze import Visualizer
import click

def main():
    visual = Visualizer()
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

@click.command()
@click.option("--week", default="les1", help="Device type: iOS or Android")
if __name__ == "__main__":
    folders = Folders(
        raw=raw,
        processed=processed,
        datafile=datafile,
    )
    visualizer = Visualizer()
    datafile = visualizer.folders.processed / visualizer.folders.datafile
    

    if week.lower()=="1":
        visualizer.visualization_week1(datafile)
    if week.lower()=="2":
        visualizer.visualization_week2(datafile)

    if week.lower()=="3":
        visualizer.visualization_week3(datafile)
    main()
