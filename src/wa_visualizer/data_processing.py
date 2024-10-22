import re
from wa_visualizer.base_dataobj import DataObject
import datetime
from loguru import logger
import pandas as pd
import numpy as np



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

    def find_replace_pattern(self, text:str, pattern:str, replace_str: str='') -> str:
        """_summary_

        Args:
            text (str): text to edit
            pattern (str): regex expression to find
            replace_str (str, optional): text to replace with. Defaults to ''.

        Returns:
            str: string edited
        """               
        return re.sub(pattern, replace_str, text)

    def clean_message(self, text: str)-> str:
        """
        clean message texts for specific patterns  
        Args:
            text (str): input text

        Returns:
            str: cleaned text
        """       
        #removes return and new lines
        rn_pattern = r'[\r\n?]'
        text = self.find_replace_pattern(text, rn_pattern)
        #remove forwarding of changed telephone number
        pattern_fwd =  r'^\d{2}-\d{2}-\d{4} \d{2}:\d{2} - \+\d{2} \d{2} \d{4} \d{4}: '
        text = self.find_replace_pattern(text, pattern_fwd)
        pattern_fwd_tel = r"@\d{10,13}(?:[ ;:,.]|)"
        text = re.sub(pattern_fwd_tel, '', text)
        pattern_email =  r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
        text = re.sub(pattern_email, '', text)
        username_pattern = r"^@[a-zA-Z0-9._]+"
        text = re.sub(username_pattern, '', text)
        
        return text.strip()
    
    def clean_data(self):
        """
        Data cleaning logic
        """        
        # remove returns and new lines
        self.df['message'] = self.df['message'].appy(self.clean_message)
        empty_messages = self.df[self.df['message']==""].index
        self.df.drop(empty_messages, axis=0, inplace=True)
        #rerun emoticon detection for missing emoij's
        self.df['has_emoji'] =self.df['message'].apply(self.has_emoji)
        #delete empty rows
        
        
    def save_data(self, datafile):
        """
        save dataframe
        """        
        
        try:
            self.df.to_csv(datafile, index=False)
            self.df.to_parquet(datafile, index=False)
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
            if word in self.dutch_stopwords+self.dutch_frequentwords:
                guessed_language = "NL"
                        
            if word in self.italian_stopwords+self.italian_frequentwords:
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
        print('prlaceocess week 3')
        df = self.df.copy()
        # Define keywords for each category (selection by hand on the base of frequency and word counts)
        eten_keywords = ['\beten\b', 'eet', "gegeten", 'blijf eten', 'lunch', 'pizza', 'pasta', 'mangia', 'pranzo', 'cena', 'prosciutto', 'kip', 'latte', 'snack', 'indonesisch', 'kapsalon', 'kps', 'delfino', 'ninh', 'bihn']
        plans_keywords = ['vanavond', 'vandaag', 'morgen', 'afspraak', 'domani', 'stasera', 'ochtend']
        place_keywords = ['trein', 'hilversum', 'amsterdam', 'thuis', 'huis', 'ik ben in', 'dallas', 'spanje', 'mexico', 'indonesië', 'hotel', 'onderweg', 'casa']
        people_keywords = self.df.author.unique().tolist() + ['papa','mama', 'nonno', 'nonna', 'giacomo', 'opa', 'oma', 'siem', 'tessa', 'ouders']
        
        df['hour'] = df['timestamp'].dt.hour
        df.loc[self.contains_keywords(df['message'], eten_keywords), 'topic'] = 'food'
        # Filter DataFrame to remove rows that contain 'food'
        df_food = df[df['topic'] == 'food']
        df  = df[df['topic'] != 'food']
        
        # Filter DataFrame to remove rows that contain 'plans'
        df.loc[self.contains_keywords(df['message'], plans_keywords), 'topic'] = 'plans'
        df_plans = df[df['topic'] == 'plans']
        df = df[df['topic'] != 'plans']

        # Filter DataFrame to remove rows that contain 'places'
        df.loc[self.contains_keywords(df['message'], place_keywords), 'topic'] = 'places'
        df_places = df[df['topic'] == 'places']
        df = df[df['topic'] != 'places']

        # Filter DataFrame to remove rows that contain 'people'
        df.loc[self.contains_keywords(df['message'], people_keywords), 'topic'] = 'people'
        df_people = df[df['topic'] == 'people']
        df_other = df[df['topic'] != 'people']   

        df_all = pd.concat([df_other, df_food, df_plans, df_places, df_people])
        if df_all.shape[0]== self.df.shape[0]:
            
            self.df.to_csv("./data/processed/whatsapp-20240916-104455_withtopics.csv", index=False)        
        else:
            print('Could not add topics to data')
        #create topics counts
        self.whatsapp_topics = {
        'food': df_food['hour'].value_counts().sort_index(),
        'plans': df_plans['hour'].value_counts().sort_index(),
        'places': df_places['hour'].value_counts().sort_index(),
        'people': df_people['hour'].value_counts().sort_index(),
        'other': df_other['hour'].value_counts().sort_index(),
        }
        # Create a DataFrame and reindex to ensure all hours are included
        df_counts = pd.DataFrame({
            'Food': pd.Series(self.whatsapp_topics['food'], name='Food'),
            'Plans': pd.Series(self.whatsapp_topics['plans'], name='Plans'),           
            'People': pd.Series(self.whatsapp_topics['people'], name='People'),
            'Places': pd.Series(self.whatsapp_topics['places'], name='Places'),
            'Other': pd.Series(self.whatsapp_topics['other'], name='Other')           
        }).fillna(0).reindex(range(24), fill_value=0)

        # Step 1: Calculate total counts for each hour
        df_counts['Total'] = df_counts.sum(axis=1)

        # Step 2: Normalize each column (Food, Plans, People, Places, Other) to percentages
        df_normalized = df_counts.fillna(0).iloc[:, :-1].div(df_counts['Total'], axis=0) * 100

        # Display the normalized DataFrame
        #print(df_normalized)    

        return df_normalized

    def preprocess_week4(self):
        df = self.df.copy()
        #include age in the features (cleanup stage)
        df['year'] = df["timestamp"].apply(lambda x: x.year)       
        dob_mapping = {'effervescent-camel': 2002, 'nimble-wombat':1971, 'hilarious-goldfinch':1972,
            'spangled-rabbit':2004}
        df['dob'] = df['author'].map(dob_mapping)
        df['age'] = df['year']-df['dob']
        df.drop(['dob'], inplace=True, axis=1)
        df["log_len"] = df["message_length"].apply(lambda x: np.log(x))
        return df

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
        self.save_data(self.datafile)


