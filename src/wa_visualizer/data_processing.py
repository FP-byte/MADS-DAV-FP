import re
from pathlib import Path
import datetime
from loguru import logger
import pandas as pd
import numpy as np
from wa_visualizer.settings import (BaseRegexes, Folders, Config, BaseStrings)
from wa_visualizer.filehandler import FileHandler

class Preprocessor(FileHandler):
    """
    Manages all the preprocessing steps for the visualizations

    Args:
        FileHandler (class): basic data object class
    """
    def __init__(self, folders: Folders, regexes:BaseRegexes, config:Config, strings :BaseStrings):
        super().__init__(folders, config)
        self.folder = folders
        self.config = config
        self.regexes = regexes
        self.strings = strings
        self.whatsapp_topics={}
        self.regexes = regexes
        self.config = config
        self.strings = strings
    
    def __call__(self):
        self.process()
        self.save_data(self.folder.datafile)

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
        for pattern in self.regexes.patterns.values():
            text = self.find_replace_pattern(text, pattern)
            
        return text.strip()
    
    def clean_data(self):
        """
        Data cleaning logic
        """  
        df = self.data 
        message = self.config.message_col     
        # remove returns and new lines
        df[message] = df[message].apply(self.clean_message)
        empty_messages = df[df[message]==""].index
        df.drop(empty_messages, axis=0, inplace=True)
        #rerun emoticon detection for missing emoij's
        df[self.config.has_emoji_col] =df[message].apply(self.has_emoji)
        #delete empty rows

    
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
            if word in self.strings.dutch_stopwords+self.strings.dutch_frequentwords:
                guessed_language = "NL"
                        
            if word in self.strings.italian_stopwords+self.strings.italian_frequentwords:
                guessed_language = "IT"
        #print(f"guessed_language is {guessed_language}")    
        return guessed_language
                

    def add_communication_type(self)->str:
        """
        Defines communication category (IT, NL or Non-Verbal)

        Returns:
            str: language category
        """        

        for idx, row in self.data.iterrows():
            text=row.message.replace('\r', "").replace('\n', "").replace('?', "").replace('!', "").lower()
            text=text.strip().split(" ") 
            # Check for non-verbal indicators
            if '<media' in row.message or 'http' in row.message or 'www.' in row.message:
                self.data.at[idx, 'language'] = "Non-verbal"
            elif len(text) == 1 and row['has_emoji']:
                self.data.at[idx, 'language'] = 'Non-verbal'             
            else:
                # detect language 
                self.data.at[idx, 'language'] = self.detect_language(text)

    def process_dates(self):
        """add dates information
        """            
        self.data["date"] = self.data[self.config.timestamp_col].dt.date
        self.data["isoweek"] = self.data[self.config.timestamp_col].dt.isocalendar().week
        self.data["year-week"] = self.data[self.config.timestamp_col].dt.strftime("%Y-%W")
    
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
        min_ts = df[self.config.timestamp_col].min()
        max_ts = df[self.config.timestamp_col].max()
        new_index = pd.date_range(start=min_ts, end=max_ts, freq='W', name="year-week").strftime('%Y-%W')
        return p.reindex(new_index, fill_value=0)
    
    def calculate_percentage(self, counts, total_counts):
        # Calculate percentages
        return (counts.div(total_counts, axis=0) * 100)

    def aggregate_languages(self, data):
        # Grouping by author and language
        user_language_counts = data.groupby(['author', 'language']).size().unstack(fill_value=0)

        # Combine 'NL' and 'IT' into 'Verbal'
        user_language_counts['Verbal'] = user_language_counts[['NL', 'IT']].sum(axis=1)

        # Drop the original NL and IT columns
        user_language_counts.drop(['NL', 'IT'], inplace=True, axis=1)

        # Calculate the total counts for each author
        total_counts = user_language_counts.sum(axis=1)

        # Sort user_language_counts based on the sorted language counts
        sorted_user_language_counts = user_language_counts.sort_values(by='Verbal', ascending=False)  # Sort by Verbal column
        percentages = self.calculate_percentage(sorted_user_language_counts, total_counts)
        percentages_sorted = percentages.sort_values(by='Verbal', ascending=False)

        return percentages_sorted
    
    def preprocess_week1(self):
        print("processing visual 1")
        self.add_communication_type()
        return self.aggregate_languages(self.data)


    def preprocess_week2(self, startdate='2019-01-01', enddate='2023-01-01'):
        self.process_dates()          
        # select dataset for corona time - start period
        start_date = datetime.datetime.strptime(startdate, self.config.timeformat).date()
        # end corona period
        end_date = datetime.datetime.strptime(enddate, self.config.timeformat).date()
        df = self.select_dates(self.data, start_date, end_date)

        # select corona data - start first lockdown
        start_date = datetime.datetime.strptime('2020-03-09', self.config.timeformat).date()
        # second lockdown
        end_date = datetime.datetime.strptime('2021-01-15', self.config.timeformat).date()

        df_corona = self.select_dates(self.data, start_date, end_date)

        return df_corona, df

    # Function to check for keywords
    def contains_keywords(self, series, keywords):
         return series.str.contains('|'.join(keywords), case=False, regex=True)

    def preprocess_week3(self):
        print('preprocess week 3')
        df = self.data.copy()
        # Define keywords for each category (selection by hand on the base of frequency and word counts)
        eten_keywords = ['\beten\b', 'eet', "gegeten", 'blijf eten', 'lunch', 'pizza', 'pasta', 'mangia', 'pranzo', 'cena', 'prosciutto', 'kip', 'latte', 'snack', 'indonesisch', 'kapsalon', 'kps', 'delfino', 'ninh', 'bihn', 'spareribs']
        plans_keywords = ['vanavond', 'vandaag', 'morgen', 'afspraak', 'domani', 'stasera', 'ochtend']
        place_keywords = ['trein', 'hilversum', 'amsterdam', 'thuis', 'huis', 'ik ben in', 'dallas', 'spanje', 'mexico', 'indonesië', 'hotel', 'onderweg', 'casa', 'florence', 'italie', 'schiphol']
        people_keywords = self.data.author.unique().tolist() + ['papa','mama', 'nonno', 'nonna', 'giacomo', 'opa', 'oma', 'siem', 'tessa', 'ouders']
        
        df['hour'] = df[self.config.timestamp_col].dt.hour
        df.loc[self.contains_keywords(df[self.config.message_col], eten_keywords), 'topic'] = 'food'
        # Filter DataFrame to remove rows that contain 'food'
        df_food = df[df['topic'] == 'food']
        df  = df[df['topic'] != 'food']
        
        # Filter DataFrame to remove rows that contain 'plans'
        df.loc[self.contains_keywords(df[self.config.message_col], plans_keywords), 'topic'] = 'plans'
        df_plans = df[df['topic'] == 'plans']
        df = df[df['topic'] != 'plans']

        # Filter DataFrame to remove rows that contain 'places'
        df.loc[self.contains_keywords(df[self.config.message_col], place_keywords), 'topic'] = 'places'
        df_places = df[df['topic'] == 'places']
        df = df[df['topic'] != 'places']

        # Filter DataFrame to remove rows that contain 'people'
        df.loc[self.contains_keywords(df[self.config.message_col], people_keywords), 'topic'] = 'people'
        df_people = df[df['topic'] == 'people']
        df_other = df[df['topic'] != 'people']   

        df_all = pd.concat([df_other, df_food, df_plans, df_places, df_people])
        if df_all.shape[0]== self.data.shape[0]:
            file_topics = self.folders.processed / Path(self.folders.current).stem
            self.data.to_csv(f"{file_topics}.csv", index=False)        
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

        return df_normalized

    def preprocess_week4(self):
        df = self.data.copy()
        
        # Include age in the features (cleanup stage)
        df['year'] = df[self.config.timestamp_col].dt.year  # Extract year from datetime
        df['dob'] = df[self.config.author_col].map(self.strings.dob_mapping)
        df['age'] = df['year'] - df['dob']
        df.drop(['dob'], inplace=True, axis=1)

        # Calculate the logarithm of message length
        df["log_len"] = df[self.config.message_length_col].apply(lambda x: np.log(x) if x > 0 else 0)  # Handle log(0)

        # Create a new column to categorize messages based on emoji presence
        df['emoji_status'] = df['has_emoji'].apply(lambda x: 'With Emoji' if x > 0 else 'Without Emoji')

        # Calculate the average log length per age
        avg_log_df = df.groupby(['age', 'emoji_status'])['log_len'].mean().reset_index()
    
        return avg_log_df

    def process(self):
        """
        Data transformation steps needed prior the visualizations
        """               
        self.clean_data()
        # add language column for visualization 1
        self.add_communication_type()
        # add date transformation for visualizazion 2
        self.process_dates()
        #save preprocessed data
        self.save_data()


