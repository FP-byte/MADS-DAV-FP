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

    def delete_system_messages(self, df:pd.DataFrame, author:str)-> pd.DataFrame:
        """
        Delete authomatic system messages under the same author name

        Args:
            df (pd.DataFrame): data to change
            author (str): author name as given to automatic author messages
        Returns:
            pd.DataFrame: dataframe without the author
        """        	    
        sys_messages = df[df[self.config.author_col]==author].index
        df.drop(sys_messages, inplace=True, axis=0)
        return df
    
    def merge_users(self, df:pd.DataFrame, author1:str, author2:str):
        """
        Merge two users which are using aliases, for ex. two different telephones but are the same person

        Args:
            df (pd.DataFrame): dataframe to modify
            author1 (str): author1 is the main author
            author2 (str): author alias to replace with author1 
        """        
        df.loc[df[self.config.author_col]==author2, 'author'] = author1
        return df


    
    def clean_data(self):
        """
        Data cleaning
        """  
        df = self.data 
        message = self.config.message_col
        #delete system messages 
        df = self.delete_system_messages(df, 'glittering-penguin')
        #merging two users 
        df = self.merge_users(df, 'effervescent-camel','funny-bouncing')  
        # remove messages with regex
        df[message] = df[message].apply(self.clean_message)
        empty_messages = df[df[message]==""].index
        df.drop(empty_messages, axis=0, inplace=True)
        #rerun emoticon detection for missing emoij's
        df[self.config.has_emoji_col] =df[message].apply(self.has_emoji)
        

    
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
            if '<Media' in row.message or 'http' in row.message or 'www.' in row.message:
                self.data.at[idx, self.config.language_col] = "Non-verbal"
            elif len(text) == 1 and row[self.config.has_emoji_col]:
                self.data.at[idx, self.config.language_col] = 'Non-verbal'             
            else:
                # detect language 
                self.data.at[idx, self.config.language_col] = self.detect_language(text)

    def process_dates(self)-> None:
        """
        Adds dates information to the dataframe
        """            
        self.data[self.config.date_col] = self.data[self.config.timestamp_col].dt.date
        self.data[self.config.isoweek_col] = self.data[self.config.timestamp_col].dt.isocalendar().week
        self.data[self.config.year_week_col] = self.data[self.config.timestamp_col].dt.strftime("%Y-%W")
    
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

    def filter_by_keywords(self, df, keywords, topic):
        """Filter DataFrame rows based on keywords and assign a topic."""
        df.loc[self.contains_keywords(df[self.config.message_col], keywords), 'topic'] = topic
        return df[df['topic'] == topic]


    def preprocess_week3(self):
        print('preprocess week 3')
        df = self.data.copy()
        df[self.config.hour_col] = df[self.config.timestamp_col].dt.hour

        # Define keywords for each category
        keywords = {
            'home coming': ['kom', 'naar huis', 'hoe laat', 'hoelaat', 'laat', 'slapen', 'slaap bij', 'donker', 'bed', 'thuis', 'huis', 'terug', 'blijf bij', 'ik ben in','onderweg', 'casa', 'notte', 'nacht', 'sleutel', 'blijven', 'vannacht'],
            'reizen': [
                 'hilversum', 'amsterdam', 'reis', 'arrivati', 'aangekomen', 'vertrek', 'ingecheckt'
                 'dallas', 'spanje', 'mexico', 'bus', 'boot', 'trein',
                'indonesië', 'hotel', 'florence', 'italie', 'schiphol', 'grado', 'tiare', 'ho chi minh', 
            ],
            'food': [
                r'\beten\b', 'eet', "gegeten", 'blijf eten', 'lunch', 
                'pizza', 'pasta', 'mangia', 'pranzo', 'cena', 
                'prosciutto', 'kip', 'latte', 'snack', 
                'indonesisch', 'kapsalon', 'kps', 'delfino', 
                'ninh', 'bihn', 'spareribs'
            ],           
            
            #'plans': ['vanavond', 'vandaag', 'morgen', 'afspraak', 'domani', 'stasera', 'ochtend', 'oggi', 'domani'],
            'people': self.data.author.unique().tolist() + [
                'papa', 'mama', 'nonno', 'nonna', 'giacomo', 'greta',
                'opa', 'oma', 'siem', 'tessa', 'ouders', 'mila', 'julia', 'vera'
            ]
        }

        # Initialize an empty dictionary to hold filtered DataFrames
        filtered_dfs = {topic: None for topic in keywords.keys()}

        for topic, words in keywords.items():
            filtered_dfs[topic] = self.filter_by_keywords(df, words, topic)
            df = df[df[self.config.topic_col] != topic]  # Remove rows already categorized
        
        # Remaining rows are classified as 'other'
        # Filter out non verbal messages
        filtered_dfs['other'] = df[df[self.config.language_col]!='Non-verbal']

        df_all = pd.concat(filtered_dfs.values(), ignore_index=True)

        if df_all.shape[0] == self.data.shape[0]:
            file_topics = self.folders.processed / Path(self.folders.current).stem
           # self.data.to_csv(f"{file_topics}_with_topics.csv", index=False)
            self.save_data()
        else:
            print('Could not add topics to data')

        # Create topics counts
        self.whatsapp_topics = {
            topic: df['hour'].value_counts().sort_index() for topic, df in filtered_dfs.items() if df is not None
        }

        # Create a DataFrame and reindex to ensure all hours are included
        df_counts = pd.DataFrame({
            topic.capitalize(): pd.Series(self.whatsapp_topics[topic], name=topic.capitalize())
            for topic in self.whatsapp_topics.keys()
        }).fillna(0).reindex(range(24), fill_value=0)

        # Calculate total counts for each hour
        df_counts['Total'] = df_counts.sum(axis=1)

        # Normalize each column to percentages
        df_normalized = df_counts.iloc[:, :-1].div(df_counts['Total'], axis=0) * 100

        return df_normalized


    def preprocess_week4(self):
        df = self.data.copy()
        # Include age in the features (cleanup stage)
        df[self.config.year_col] = df[self.config.timestamp_col].dt.year  # Extract year from datetime
        df['dob'] = df[self.config.author_col].map(self.strings.dob_mapping)
        df[self.config.age_col] = df[self.config.year_col] - df['dob']
        df.drop(['dob'], inplace=True, axis=1)
        print(df.columns)
        df[self.config.message_length_col] = df[self.config.message_col].str.len()

        # Calculate the logarithm of message length
        df[self.config.log_length_col] = df[self.config.message_length_col].apply(lambda x: np.log(x) if x > 0 else 0)  # Handle log(0)

        # Create a new column to categorize messages based on emoji presence
        df[self.config.emoji_status_col] = df[self.config.has_emoji_col].apply(lambda x: 'With Emoji' if x > 0 else 'Without Emoji')

        # Calculate the average log length per age
        avg_log_df = df.groupby([self.config.age_col, self.config.emoji_status_col])[self.config.log_length_col].mean().reset_index()
    
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


