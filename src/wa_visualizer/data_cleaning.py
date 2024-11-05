import re
from pathlib import Path
from loguru import logger
import pandas as pd
from wa_visualizer.settings import (BaseRegexes, Folders, Config)
from wa_visualizer.filehandler import FileHandler

class DataCleaner(FileHandler):
    def __init__(self, folders: Folders, regexes:BaseRegexes, config:Config, source:str):
        super().__init__(folders, config, source)
        self.folder = folders
        self.config = config
        self.regexes = regexes
    
    def __call__(self):
        self.clean_data()
        self.save_data()

    #******** help methods *******************

    def has_emoji(self, text) -> bool:
        """
        Detect whether the given text contains any emoji characters.

        This method uses a regular expression to identify a range of emoji characters
        across various Unicode blocks (extra emoij's patterns added).

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
        # Apply regex patterns removal
        df[message] = df[message].apply(self.clean_message)
        empty_messages = df[df[message] == ""].index
        df.drop(empty_messages, axis=0, inplace=True)
        # Rerun emoticon detection for missing emojis
        df[self.config.has_emoji_col] = df[message].apply(self.has_emoji)
        # Update current data
        self.data = df
        logger.info('Data has been cleaned')
