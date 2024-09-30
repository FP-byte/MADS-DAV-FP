import click
import datetime
from pathlib import Path
import tomllib
from loguru import logger
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import spacy
from spacy.lang.it.stop_words import STOP_WORDS as italian_stopwords
from spacy.lang.nl.stop_words import STOP_WORDS as dutch_stopwords

# Load spaCy models for Italian and Dutch
nlp_it = spacy.load("it_core_news_sm")
nlp_nl = spacy.load("nl_core_news_sm")


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


    def prepocess_week2(self):
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

    def visualization_week1(self):
        #to add
        pass

    def remove_stopwords_in_df(df, languages=False, path='', column = "Word"):
    """ Remove stopwords from a dataframe choosing
    a specific column in which to remove those words
    
    Parameters:
    -----------
    df : pandas dataframe
        Dataframe of counts per word per user
    path : string, default ''
        Path of the file that contains the stopwords
    language : str, default False
        The language to be used in the built-in nltk stopwords
    column : string, default 'Word'
        Column to clean

    Returns:
    --------
    df : pandas dataframe
        Dataframe of counts per word per user
        excluding the stopwords
    
    """

    if languages:
        for language in languages:

            try:
                stopwords = nltk_stopwords.words(language)
            except:
                languages = nltk_stopwords.fileids()
                raise Exception(f"Stopwords for {language} not found.")

    else:
        with open(path) as stopwords:
            stopwords = stopwords.readlines()
            stopwords = [word[:-1] for word in stopwords]


    df = df[~df[column].isin(stopwords)]
    
    return df

    def detect_language(self, text):
        guessed_language = None
        text=text.replace('\r', "").replace('\n', "").replace('?', "").split(" ")
        if '<Media' in text:
            guessed_language= "Image"
            return guessed_language
        # Attempt to parse the text with both Italian and Dutch models
        doc_it = nlp_it(text)
        doc_nl = nlp_nl(text)
        #print(doc_it)
        
        # Score the models based on the length of tokens processed
        # Higher length usually means better parsing
        score_it = len(doc_it)
        score_nl = len(doc_nl)
        #print(score_it, score_nl)

        if score_it > score_nl:
            guessed_language = "Italian"
            return 
        elif score_nl > score_it:
            return "Dutch"
        else:
            for word in text:              
                if word in ['per', 'via']:
                    return
                if word in dutch_stopwords or word in ['leuk', 'hoor', 'gezellig']:
                    print(word)
                    guessed_language = "Dutch"
                    return guessed_language
                    break
                    
                if word in italian_stopwords or word in ['grazie', 'ciao']:
                    print(word)
                    guessed_language = "Italian"
                    return guessed_language
                    break
            if len(text)==1:
                 guessed_language = 'Emoij'
                                   
            return guessed_language


    def visualization_week2(self):
        df, df_corona = self.prepocess_week2()
        p = self.calc_messages(df)
        p_corona = self.calc_messages(df_corona)
        self.visualize_timeseries(p, p_corona)

    def visualization_week3(self):
        #need to be refactored
        df['hour'] = df['timestamp'].dt.hour
        df['contains_eten'] = df['message'].str.contains('eten|pizza|pasta|mangia|pranzo|cena|prosciutto|kip|latte', case=False, regex=True)
        df['contains_plans'] = df['message'].str.contains('vanavond|vandaag|morgen|afspraak|domani|stasera', case=False, regex=True)
        df2 = df[~df[['contains_eten']].all(axis=1)]
        df['contains_place'] = df2['message'].str.contains('trein|hilversum|amsterdam|thuis|huis|ik ben in', case=False, regex=True)
        df3 = df2[~df2[['contains_eten']].all(axis=1)]
        df['contains_people'] = df3['message'].str.contains('irene|lorenzo|papa|mama|nonno|nonna|giacomo|opa|oma', case=False, regex=True)
        whatsapp_topics = {
    'food': df[df['contains_eten'].fillna(False)]['hour'].value_counts().sort_index(),
    'plans': df[df['contains_plans'].fillna(False)]['hour'].value_counts().sort_index(),
    'place': df[df['contains_place'].fillna(False)]['hour'].value_counts().sort_index(),
    'people': df[df['contains_people'].fillna(False)]['hour'].value_counts().sort_index(),
         }
         # Convert to DataFrames
        hour_counts1 = pd.Series(whatsapp_topics['food'])
        hour_counts2 = pd.Series(whatsapp_topics['plans'])
        hour_counts3 = pd.Series(whatsapp_topics['place'])
        hour_counts4 = pd.Series(whatsapp_topics['people'])


        # Convert to DataFrames
        hour_counts1 = pd.Series(whatsapp_topics['food'], name='Food')
        hour_counts2 = pd.Series(whatsapp_topics['plans'], name='Plans')
        hour_counts3 = pd.Series(whatsapp_topics['place'], name='Places')
        hour_counts4 = pd.Series(whatsapp_topics['people'], name='People')


        # Create a DataFrame and reindex to ensure all hours are included
        df_counts = pd.DataFrame({
            #'Parents': hour_counts5,
            'Food': hour_counts1,
            'Plans': hour_counts2,
            
            'People': hour_counts4,
            'Places': hour_counts3,
            
            
            #'Mama': hour_counts5,
            #'Papa': hour_counts5,
        }).fillna(0).reindex(range(24), fill_value=0)

        plt.figure(figsize=(12, 6))
        # Define custom colors
        colors = [  'red', 'gray', 'darkgray', 'lightgray', ]

        plt.stackplot(df_counts.index, df_counts.T, colors=colors, labels=df_counts.columns, alpha=0.6)
        plt.title("Feeding the Dialogue: How Hunger Fuels Food Conversations")
        plt.xlabel('Hour of Day')
        plt.ylabel('Number of messages about topic')
        plt.xticks(df_counts.index, rotation=45)
        # Add a legend with a title
        plt.legend(loc='upper left', title='Topics')
        plt.grid()
        plt.show()



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

def remove_stopwords(df, languages=False:list, path='', column = "Message"):
    """ Remove stopwords from a dataframe choosing
    a specific column in which to remove those words
    
    Parameters:
    -----------
    df : pandas dataframe
        Dataframe of counts per word per user
    path : string, default ''
        Path of the file that contains the stopwords
    language : str, default False
        The language to be used in the built-in nltk stopwords
    column : string, default 'Word'
        Column to clean

    Returns:
    --------
    df : pandas dataframe
        Dataframe of counts per word per user
        excluding the stopwords
    
    """

    if languages:
        for language in languages and language in nltk_stopwords.fileids():
            try:
                stopwords = nltk_stopwords.words(language)
            except:
                languages = nltk_stopwords.fileids()
                raise Exception(f"{langugage} is not recognized.")

    else:
        with open(path) as stopwords:
            stopwords = stopwords.readlines()
            stopwords = [word[:-1] for word in stopwords]

    df = df[~df[column].isin(stopwords)]
    
    return df

    
        


if __name__ == "__main__": 
    
    
      

        main()

