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
    timeformat: str  

@dataclass
class BaseStrings:
    dutch_stopwords : list
    italian_stopwords : list
    dutch_frequentwords : list
    italian_frequentwords : list
    dob_mapping : dict
 
@dataclass
class Folders:
    raw: Path
    processed: Path
    datafile: Path
    current: Path
    csv: Path
    

    
