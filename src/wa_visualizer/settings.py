from pydantic import BaseModel
from dataclasses import dataclass
from pathlib import Path

@dataclass
class BaseRegexes:
    patterns : dict


@dataclass
class Config:
    img_dir: Path
    timestamp_col: str
    message_col: str
    author_col: str
    message_length_col: str
    has_emoji_col: str
    topic_col: str
    log_length_col: str
    age_col: str
    emoji_status_col: str
    year_col: str
    language_col:str
    hour_col:str
    date_col:str
    isoweek_col:str
    year_week_col:str
    timeformat: str 
    basic_color: str
    color_palette: list
    basic_color_highlight: str
    color_vertical_line: str

@dataclass
class BaseStrings:
    dutch_stopwords : list
    italian_stopwords : list
    dutch_frequentwords : list
    italian_frequentwords : list
    dob_mapping : dict
    topic_keywords: dict
 
@dataclass
class Folders:
    raw: Path
    processed: Path
    datafile: Path
    current: Path
    csv: Path
    

    
