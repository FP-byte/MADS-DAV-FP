import re
from pathlib import Path
import datetime
from loguru import logger
import pandas as pd
import numpy as np
from wa_visualizer.settings import (BaseRegexes, Folders, Config, BaseStrings, keywordsFilter, extraRegexes, basicConfig, Embedding)
from wa_visualizer.filehandler import FileHandler

#from sentence_transformers import SentenceTransformer
from sklearn.manifold import TSNE


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
        # define dob for this dataset
        self.dob_mapping = {'effervescent-camel': 2002, 'nimble-wombat':1971, 'hilarious-goldfinch':1972, 'spangled-rabbit':2004}
    
    def __call__(self):
        self.process()
        self.save_data()

    #******** hulpmethoden *******************

    def has_emoji(self, text) -> bool:
        """
        Detect whether the given text contains any emoji characters.

        This method uses a regular expression to identify a range of emoji characters
        across various Unicode blocks.

        Args:
            text (str): The text in which to detect emojis.

        Returns:
            bool: True if the text contains at least one emoji, False otherwise.
        """        
        emoji_pattern = re.compile("["  # Compile a regex pattern for emoji detection
            u"\U0001F600-\U0001F64F"  # Emoticons
            u"\U0001F920-\U0001F9FF"  # Extra missing emoticons
            u"\U0001F300-\U0001F5FF"  # Symbols & pictographs
            u"\U0001F680-\U0001F6FF"  # Transport & map symbols
            u"\U0001F1E0-\U0001F1FF"  # Flags (iOS)
            u"\U00002702-\U000027B0"  # Dingbats
            u"\U000024C2-\U0001F251"  # Miscellaneous symbols
            "]+", flags=re.UNICODE)

        return bool(emoji_pattern.search(text))  # Return True if an emoji is found
    @logger.catch
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
    @logger.catch
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
    @logger.catch
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
    @logger.catch
    def merge_users(self, df:pd.DataFrame, author1:str, author2:str)-> pd.DataFrame:
        """
        Merge two users which are using aliases, for ex. two different telephones but are the same person

        Args:
            df (pd.DataFrame): dataframe to modify
            author1 (str): author1 is the main author
            author2 (str): author alias to replace with author1 
        Returns:
            pd.DataFrame: dataframe with merged authors
        """        
        df.loc[df[self.config.author_col]==author2, 'author'] = author1
        return df
    @logger.catch
    def add_communication_type(self) -> None:
        """
        Defines communication category (IT, NL or Non-Verbal)
        """        

        for idx, row in self.data.iterrows():
            #remove ? and !, make message lower case
            text=row.message.replace('?', "").replace('!', "").lower()
            text=text.strip().split(" ") 
            # Check for non-verbal indicators
            if '<Media' in row.message or 'http' in row.message or 'www.' in row.message:
                self.data.at[idx, self.config.language_col] = "Non-verbal"
            elif len(text) == 1 and row[self.config.has_emoji_col]:
                self.data.at[idx, self.config.language_col] = 'Non-verbal'             
            else:
                # detect language 
                self.data.at[idx, self.config.language_col] = self.detect_language(text)
    @logger.catch
    def process_dates(self) -> None:
        """
        Adds dates information to the dataframe
        """            
        self.data[self.config.date_col] = self.data[self.config.timestamp_col].dt.date
        self.data[self.config.isoweek_col] = self.data[self.config.timestamp_col].dt.isocalendar().week
        self.data[self.config.year_week_col] = self.data[self.config.timestamp_col].dt.strftime("%Y-%W")
    @logger.catch
    def select_dates(self, df, start_date, end_date) -> None:
        if 'date' in df:
            # Select DataFrame rows between two dates
            mask = (df['date'] > start_date) & (df['date'] <= end_date)
            return df.loc[mask]
        else:
            logger.info('No date column to select')
            return None
    @logger.catch
    def calc_messages(self, df):
        """
        Calculate the number of messages per ISO week.

        This method groups the provided DataFrame by ISO weeks and counts the number
        of messages for each week. It also creates a complete index of weeks within 
        the range of timestamps in the dataset, filling in missing weeks with a count of zero.

        Args:
            df (pd.DataFrame): The DataFrame containing message data, which includes 
                            a timestamp column.

        Returns:
            pd.Series: A Series indexed by year-week, representing the count of messages 
                        for each week. Missing weeks are filled with zeros.
        """
        p = df.groupby("year-week").count()  # Group by the ISO weeks and count messages
        min_ts = df[self.config.timestamp_col].min()  # Get the minimum timestamp
        max_ts = df[self.config.timestamp_col].max()  # Get the maximum timestamp
        new_index = pd.date_range(start=min_ts, end=max_ts, freq='W', name="year-week").strftime('%Y-%W')  # Create a new index for weeks
        return p.reindex(new_index, fill_value=0)  # Reindex with new index, filling missing weeks with zero
    
    @logger.catch
    def calculate_percentage(self, counts:pd.Series, total_counts:pd.Series)->pd.Series:
        """
        Calculate the percentage of counts relative to total counts of two dataframes

        Args:
            counts (pd.Series or pd.DataFrame): The counts for which percentages are to be calculated.
            total_counts (pd.Series or pd.DataFrame): The total counts used as the denominator.

        Returns:
            pd.Series or pd.DataFrame: The calculated percentages as a Series or DataFrame,
                                        with the same shape as the input counts.
        """
        # Calculates percentages from counts and total
        return (counts.div(total_counts, axis=0) * 100)  # Compute percentage
    @logger.catch
    def aggregate_languages(self, data:pd.DataFrame)->pd.DataFrame:
        """
        Aggregate language usage by author.
        This method groups the input data by author and language, counting the occurrences of each language
        per author. It combines the counts of 'NL' (Dutch) and 'IT' (Italian) into a single category called
        'Verbal', then calculates the percentage of verbal communication for each author.

        Args:
            data (pd.DataFrame): A DataFrame containing at least 'author' and 'language' columns.

        Returns:
            pd.DataFrame: A DataFrame with authors as the index and their corresponding 
                        percentages of verbal communication, sorted by the 'Verbal' counts.
        """
        # Grouping by author and language, counting occurrences
        user_language_counts = data.groupby(['author', 'language']).size().unstack(fill_value=0)

        # Combine 'NL' and 'IT' language counts into a new 'Verbal' category
        user_language_counts['Verbal'] = user_language_counts[['NL', 'IT']].sum(axis=1)

        # Drop the original 'NL' and 'IT' columns as they are no longer needed
        user_language_counts.drop(['NL', 'IT'], inplace=True, axis=1)

        # Calculate the total counts for each author across all languages
        total_counts = user_language_counts.sum(axis=1)

        # Sort the user_language_counts DataFrame by the 'Verbal' counts in descending order
        sorted_user_language_counts = user_language_counts.sort_values(by='Verbal', ascending=False)

        # Calculate percentages of each language count relative to the total counts
        percentages = self.calculate_percentage(sorted_user_language_counts, total_counts)

        # Sort the percentages DataFrame based on the 'Verbal' counts in descending order
        percentages_sorted = percentages.sort_values(by='Verbal', ascending=False)

        return percentages_sorted  # Return the sorted percentages DataFrame
    @logger.catch
    def detect_language(self, text)-> str:
        """
        Detect language (Italian or Dutch) using stopwords and common words

        Args:
            text (str): string in a language

        Returns:
            str: guessed language
        """               
        #set standerd NL language
        guessed_language= "NL"
        for word in text:
            # if word is in dutch string return language NL      
            if word in self.strings.dutch_stopwords+self.strings.dutch_frequentwords:
                guessed_language = "NL"
            # if word is in Italian string return language IT          
            if word in self.strings.italian_stopwords+self.strings.italian_frequentwords:
                guessed_language = "IT"
        #print(f"guessed_language is {guessed_language}")    
        return guessed_language

    @logger.catch
    def contains_keywords(self, series:pd.Series, keywords:list[str]):
        """
        Checks if keywords are present in a dataframe column
        Args:
            series (pd.Series): column with strings
            keywords (list): list of keywords

        Returns:
            _type_: _description_
        """
        return series.str.contains('|'.join(keywords), case=False, regex=True)
    
    @logger.catch
    def filter_by_keywords(self, df: pd.DataFrame, keywords: list, topic: str) -> pd.DataFrame:
        """
        Filter DataFrame rows based on specified keywords and assign a topic.
        This method searches for the presence of keywords in the specified message column of the DataFrame
        and assigns the given topic to rows containing any of the keywords. It then returns a filtered DataFrame
        containing only the rows that have the assigned topic.

        Args:
            df (pd.DataFrame): The DataFrame to be filtered.
            keywords (list): A list of keywords to search for in the message column.
            topic (str): The topic to assign to rows that contain any of the keywords.

        Returns:
            pd.DataFrame: A DataFrame containing only the rows that have the assigned topic.
        """
        # Assign the topic to rows containing any of the keywords
        df.loc[self.contains_keywords(df[self.config.message_col], keywords), 'topic'] = topic
        # Return the filtered DataFrame with only the rows assigned the topic
        return df[df[self.config.topic_col] == topic]

    def add_topics(self) -> dict:
        """
        Adds topics to the data based on predefined keywords.

        This method filters the DataFrame by keywords associated with each topic, categorizing the data accordingly.
        It also adds the author names to the list of keywords under the 'people' category. 
        Remaining rows are classified as 'other'. The modified DataFrame is saved, and a CSV file is created
        containing the original data with the assigned topics.

        Returns:
            dict: A dictionary containing filtered DataFrames for each topic, including an 'other' category
                for any messages that do not match predefined topics.
        """
        df = self.data.copy()
        df[self.config.hour_col] = df[self.config.timestamp_col].dt.hour
        keywords = self.strings.topic_keywords
        # Add author names to the people keywords
        keywords['people'] = self.data.author.unique().tolist() + keywords['people']
        
        # Initialize an empty dictionary to hold filtered DataFrames
        filtered_dfs = {topic: None for topic in keywords.keys()}

        for topic, words in keywords.items():
            filtered_dfs[topic] = self.filter_by_keywords(df, words, topic)
            df = df[df[self.config.topic_col] != topic]  # Remove rows already categorized
        
        # Remaining rows are classified as 'other'
        filtered_dfs['other'] = df
        df_all = pd.concat(filtered_dfs.values(), ignore_index=True)
        
        # save data only if all strings are included
        if df_all.shape[0] == self.data.shape[0]:
            self.data = df_all
            file_topics = self.folders.processed / Path(self.folders.current).stem
            #save to a specific csv
            df_all.to_csv(f"{file_topics}_with_topics.csv", index=False)
            self.save_data()
        else:
            logger.info('Could not add topics to dataframe')

        return filtered_dfs

    def normalizeTopicCounts(self, filtered_dfs:dict)->pd.DataFrame:
        """
        Normalizes topic counts from filtered DataFrames.

        This method calculates the counts of messages per hour for each topic,
        creates a DataFrame with these counts, and normalizes them to percentages.

        Args:
            filtered_dfs (dict): A dictionary of DataFrames, each containing messages filtered by topic.

        Returns:
            DataFrame: A DataFrame containing normalized topic counts as percentages per hour.
        """
        # Create topics counts
        self.whatsapp_topics = {
            topic: df[self.config.hour_col].value_counts().sort_index() for topic, df in filtered_dfs.items() if df is not None
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

              
   
    #***************** data cleaning steps ***********************
    @logger.catch
    def clean_data(self):
        """
        Cleans the dataset by removing unwanted messages and normalizing user data.

        This method performs several data cleaning operations:
        - Deletes system messages from the dataset.
        - Merges messages from two specified users into one.
        - Cleans message content using a regex-based approach.
        - Removes empty messages from the dataset.
        - Re-evaluates the presence of emojis in the cleaned messages.

        After processing, the cleaned data is updated in the instance's data attribute.

        Returns:
            None
        """
        df = self.data.copy()
        message = self.config.message_col
        # Delete system messages 
        df = self.delete_system_messages(df, 'glittering-penguin')
        # Merging two users 
        df = self.merge_users(df, 'effervescent-camel', 'funny-bouncing')  
        # Remove messages with regex
        df[message] = df[message].apply(self.clean_message)
        empty_messages = df[df[message] == ""].index
        df.drop(empty_messages, axis=0, inplace=True)
        # Rerun emoticon detection for missing emojis
        df[self.config.has_emoji_col] = df[message].apply(self.has_emoji)
        # Update current data
        self.data = df
        logger.info('Data cleaned')

    @logger.catch
    def process(self)-> None:
        """
        Performs data transformation steps required before visualizations.

        This method orchestrates several preprocessing operations, including:
        - Cleaning the data to remove unwanted entries.
        - Adding a language column for visualization purposes.
        - Processing date information for further visualizations.
        - Saving the preprocessed data to a file for future use.

        Returns:
            None
        """
        self.clean_data()
        # Add language column for visualization 1
        self.add_communication_type()
        # Add date transformation for visualization 2
        self.process_dates()
        # Save preprocessed data
        self.save_data()
        
    #***************** preprocessing functions for each visualization ***********************
    @logger.catch
    def preprocess_week1(self)->pd.DataFrame:
        """
        Preprocesses data for the first visualization.

        This method performs the following steps:
        - Adds a communication type column to the dataset.
        - Aggregates language data based on author and language counts.

        Returns:
            DataFrame: A DataFrame containing aggregated language data.
        """
        print("processing visual 1")
        self.add_communication_type()
        return self.aggregate_languages(self.data)

    @logger.catch
    def preprocess_week2(self, startdate :str ='2019-01-01', enddate :str ='2023-01-01'):
        """
        Preprocess the dataset for week 2 by selecting data within specific date ranges.

        This method extracts data from the specified start date to the end date, as well as
        data related to specific lockdown periods during the pandemic.

        Args:
            startdate (str): The start date for the initial data selection.
            enddate (str): The end date for the initial data selection.

        Returns:
            tuple: A tuple containing two DataFrames:
                - df_corona: DataFrame with data during the lockdown periods.
                - df: DataFrame with data from the specified date range.
        """
        # Process the date fields in the dataset
        self.process_dates()          

        # Select dataset for the specified date range (corona time - start period)
        start_date = datetime.datetime.strptime(startdate, self.config.timeformat).date()
        end_date = datetime.datetime.strptime(enddate, self.config.timeformat).date()
        df = self.select_dates(self.data, start_date, end_date)

        # Define the start date for the first lockdown
        start_date = datetime.datetime.strptime('2020-03-09', self.config.timeformat).date()
        # Define the end date for the second lockdown
        end_date = datetime.datetime.strptime('2021-01-15', self.config.timeformat).date()

        # Select corona data for the specified lockdown period
        df_corona = self.select_dates(self.data, start_date, end_date)

        # Return the DataFrames containing corona data and the full dataset
        return df_corona, df

    @logger.catch
    def preprocess_week3(self):
        """
        Preprocess the dataset for week 3 by adding topics and normalizing topic counts.

        This method performs the necessary preprocessing steps to prepare the data for analysis.

        Returns:
            pd.DataFrame: A DataFrame with normalized topic counts.
        """
        # Log the start of the preprocessing for week 3
        logger.info('Start preprocess week 3')

        # Add topics to the dataset and get the filtered DataFrame
        filtered_dfs = self.add_topics()

        # Normalize the topic counts in the filtered DataFrame
        df_normalized = self.normalizeTopicCounts(filtered_dfs)

        # Return the DataFrame with normalized topic counts
        return df_normalized
    @logger.catch
    def preprocess_week4(self):
        """
        Preprocess the dataset for week 4 by extracting relevant features and calculating statistics.

        This method performs several data transformations, including extracting the year from timestamps,
        calculating ages, message lengths, and categorizing messages based on emoji presence.

        Returns:
            pd.DataFrame: A DataFrame containing the average logarithmic message length grouped by age and emoji status.
        """
        logger.info('Start preprocess week 4')
        # Create a copy of the original data to avoid modifying it directly
        df = self.data.copy()

        # Extract the year from the timestamp column and create a new year column
        df[self.config.year_col] = df[self.config.timestamp_col].dt.year

        # Map authors to their dates of birth using the dob_mapping dictionary
        df['dob'] = df[self.config.author_col].map(self.dob_mapping)

        # Calculate age by subtracting the date of birth from the year
        df[self.config.age_col] = df[self.config.year_col] - df['dob']

        # Drop the temporary 'dob' column as it is no longer needed
        df.drop(['dob'], inplace=True, axis=1)

        # Add a new column for message length by calculating the length of each message
        df[self.config.message_length_col] = df[self.config.message_col].str.len()

        # Calculate the logarithm of message lengths, handling cases where length is zero
        df[self.config.log_length_col] = df[self.config.message_length_col].apply(lambda x: np.log(x) if x > 0 else 0)

        # Create a new column to indicate whether messages contain emojis
        df[self.config.emoji_status_col] = df[self.config.has_emoji_col].apply(lambda x: 'With Emoji' if x > 0 else 'Without Emoji')

        # Save the modified dataset back to the instance variable
        self.data = df
        self.save_data()  # Save the updated data to persistent storage

        # Calculate the average logarithmic message length per age and emoji status
        avg_log_df = df.groupby([self.config.age_col, self.config.emoji_status_col])[self.config.log_length_col].mean().reset_index()

        return avg_log_df  # Return the resulting DataFrame

    def preprocess_week5(self, subset:pd.DataFrame):
        """
        Preprocess the data for week 5 by creating embeddings and applying t-SNE.

        Args:
            subset (pd.DataFrame): The subset of data to be processed.

        Returns:
            tuple: A tuple containing:
                - X (np.ndarray): The 2D representation of the data after t-SNE transformation.
                - emb (np.ndarray): The embeddings generated from the input subset.
        """
        # Load the pre-trained SentenceTransformer model
        model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
        # Create embeddings for the input subset using the loaded model
        emb = create_embedding(subset, model)
        # Apply t-SNE to the embeddings to reduce dimensionality for visualization
        X = fit_tsne(emb, learning_rate=300, perplexity=15, n_iter=2000)

        return X, emb



