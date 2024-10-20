import re
from wa_visualizer.base_dataobj import DataObject
import datetime
from loguru import logger
import pandas as pd



class Preprocess(DataObject):
    """_summary_

    Args:
        DataObject (_type_): basic data object class
    """
    def __init__(self, datafile):
        super().__init__(datafile)
        self.whatsapp_topics={}

    def has_emoji(self, text):
        """
        Detect emoijs not in yet included

        Returns:
            _type_: _description_
        """        
        emoji_pattern = re.compile("["
                            u"\U0001F600-\U0001F64F"
                            u"\U0001F920-\U0001F9FF"  # extra missing emoticons
                            u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                            u"\U0001F680-\U0001F6FF"  # transport & map symbols
                            u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                            u"\U00002702-\U000027B0"  # Dingbats
                            u"\U000024C2-\U0001F251"
                            "]+", flags=re.UNICODE)

        return bool(emoji_pattern.search(text))


    def clean_message(self, text: str)-> str:
        """_summary_

        Args:
            text (str): input text

        Returns:
            str: cleaned text
        """        
        #removes return and new lines
        text = re.sub(r'[\r\n?]', '', text)
        return text.strip()
    
    def clean_data(self):
        """
        Data cleaning logic
        """        
        # remove returns and new lines
        self.df['message'] = self.df['message'].appy(self.clean_message)
        #rerun emoticon detection for missing emoij's
        self.df['has_emoji'] =self.df['message'].apply(self.has_emoji)
        
    def save_data(self):
        """
        save dataframe
        """        
        
        try:
            self.df.to_csv(self.datafile, index=False)
            self.df.to_parquet(self.datafile, index=False)
        except Exception as e:
            logger.info(f'Problem with saving: {e}')

    
    def detect_language(self, text)-> str:
        """
        Detect language (Italian or Dutch) using stopwords and common words

        Args:
            text (str): string in a language

        Returns:
            str: guessed language
        """               

        guessed_language= "NL"
        for word in text:       
            if word in self.dutch_stopwords:
                guessed_language = "NL"
                        
            if word in self.italian_stopwords:
                guessed_language = "IT"
        #print(f"guessed_language is {guessed_language}")    
        return guessed_language
                

    def add_communication_type(self)->str:
        """
        Defines communication category (IT, NL or Non-Verbal)

        Returns:
            str: language category
        """        

        for idx, row in self.df.iterrows():
            text=row.message.replace('\r', "").replace('\n', "").replace('?', "").lower()
            text=text.strip().split(" ") 
            # Check for non-verbal indicators
            if '<Media' in row.message or 'http' in row.message:
                self.df.at[idx, 'language'] = "Non-verbal"
            elif len(text) == 1 and row['has_emoji']:
                self.df.at[idx, 'language'] = 'Non-verbal'             
            else:
                # detect language 
                self.df.at[idx, 'language'] = self.detect_language(text)
            #  self.df.to_parquet("../data/processed/whatsapp-20240916-104455.parquet")


    def process_dates(self):
        """add dates information
        """            
        self.df["date"] = self.df["timestamp"].dt.date
        self.df["isoweek"] = self.df["timestamp"].dt.isocalendar().week
        self.df["year-week"] = self.df["timestamp"].dt.strftime("%Y-%W")
       # self.df.to_parquet("../data/processed/whatsapp-20240916-104455.parquet")

    
    def select_dates(self, df, start_date, end_date):
        if 'date' in df:
            # Select DataFrame rows between two dates
            mask = (df['date'] > start_date) & (df['date'] <= end_date)
            return df.loc[mask]
        else:
            logger.info('No date column to select')
            return None
    
    def calc_messages(self, df):
        p = df.groupby("year-week").count()     #group by the isoweeks
        min_ts = df["timestamp"].min()
        max_ts = df["timestamp"].max()
        new_index = pd.date_range(start=min_ts, end=max_ts, freq='W', name="year-week").strftime('%Y-%W')
        return p.reindex(new_index, fill_value=0)
    
    def prepocess_week1(self):
        print("processing visual 1")
        self.add_communication_type()

    def prepocess_week2(self, startdate='2019-01-01', enddate='2023-01-01'):
        self.process_dates()          
        # select data - start period
        start_date = datetime.datetime.strptime(startdate, "%Y-%m-%d").date()
        # end period
        end_date = datetime.datetime.strptime(enddate, "%Y-%m-%d").date()
        df = self.select_dates(self.df, start_date, end_date)

        # select corona data - start first lockdown
        start_date = datetime.datetime.strptime('2020-03-09', "%Y-%m-%d").date()
        # second lockdown
        end_date = datetime.datetime.strptime('2021-01-15', "%Y-%m-%d").date()

        df_corona = self.select_dates(self.df, start_date, end_date)

        return df_corona, df

    # Function to check for keywords
    def contains_keywords(self, series, keywords):
         return series.str.contains('|'.join(keywords), case=False, regex=True)

    def preprocess_week3(self):
        print('process week 3')
        df = self.df
        df_other = {}
        #needs to be refactored
        df['hour'] = df['timestamp'].dt.hour
        # Define keywords for each category
        eten_keywords = ['eten', 'pizza', 'pasta', 'mangia', 'pranzo', 'cena', 'prosciutto', 'kip', 'latte']
        plans_keywords = ['vanavond', 'vandaag', 'morgen', 'afspraak', 'domani', 'stasera']
        place_keywords = ['trein', 'hilversum', 'amsterdam', 'thuis', 'huis', 'ik ben in']
        people_keywords = ['irene', 'lorenzo', 'papa', 'mama', 'nonno', 'nonna', 'giacomo', 'opa', 'oma']
        print(df.shape)
        # Apply keyword checks
        df['contains_eten'] = self.contains_keywords(df['message'], eten_keywords)
         # Filter DataFrame to remove rows that contain 'eten'
        
        df_other = df[~df['contains_eten']]
        print(df.shape[0]-df_other.shape[0])
        df = df_other
        print(df.shape)
        df['contains_plans'] = self.contains_keywords(df['message'], plans_keywords)

        # Filter DataFrame to remove rows that contain 'plans'
        df_other = df[~df['contains_eten']]
        print(df_other.shape)
        df = df_other
        print(df.shape)
        # Check for places in the filtered DataFrame
        df['contains_place'] = self.contains_keywords(df['message'], place_keywords)
        df_other = df[~df['contains_place']]
        df = df_other
        print(df.shape)
        
        df['contains_people'] = self.contains_keywords(df['message'], people_keywords)
        # Filter DataFrame to remove rows that contain 'people'
        df_other = df[~df['contains_people']]
        print(df.shape)
        print(df_other.shape)
        
        #create topics counts
        self.whatsapp_topics = {
        'food': df[df['contains_eten'].fillna(False)]['hour'].value_counts().sort_index(),
        'plans': df[df['contains_plans'].fillna(False)]['hour'].value_counts().sort_index(),
        'place': df[df['contains_place'].fillna(False)]['hour'].value_counts().sort_index(),
        'people': df[df['contains_people'].fillna(False)]['hour'].value_counts().sort_index(),
        'other': df_other['hour'].value_counts().sort_index()
         }

        # Convert to DataFrames
        hour_counts1 = pd.Series(self.whatsapp_topics['food'], name='Food')
        hour_counts2 = pd.Series(self.whatsapp_topics['plans'], name='Plans')
        hour_counts3 = pd.Series(self.whatsapp_topics['place'], name='Places')
        hour_counts4 = pd.Series(self.whatsapp_topics['people'], name='People')
        hour_counts5 = pd.Series(self.whatsapp_topics['other'], name='Other')

        # Create a DataFrame and reindex to ensure all hours are included
        df_counts = pd.DataFrame({
            'Food': hour_counts1,
            'Plans': hour_counts2,           
            'People': hour_counts4,
            'Places': hour_counts3,
            'Other': hour_counts5           
        }).fillna(0).reindex(range(24), fill_value=0)
        return df_counts

    def transform_data(self):
        """
        Data transformation steps needed for the visualizations
        """        
        
        self.clean_data()
        # add language column for visualization 1
        self.add_communication_type()
        # add date transformation for visualizazion 2
        self.process_dates()
        #save preprocessed data
        self.save_data()


