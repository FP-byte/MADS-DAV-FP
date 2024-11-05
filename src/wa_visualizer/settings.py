from pydantic import BaseModel
from dataclasses import dataclass
from pathlib import Path
import numpy as np

@dataclass
class BaseRegexes:
    """
    A class to hold regex patterns.

    Attributes:
        patterns (dict): A dictionary of regex patterns.
    """
    patterns: dict


@dataclass
class Config:
    """
    A class to hold configuration settings for data processing.

    Attributes:
        img_dir (Path): Path to the directory containing images.
        timestamp_col (str): Name of the column for timestamps.
        message_col (str): Name of the column for messages.
        author_col (str): Name of the column for authors.
        message_length_col (str): Name of the column for message lengths.
        has_emoji_col (str): Name of the column indicating emoji presence.
        topic_col (str): Name of the column for topics.
        log_length_col (str): Name of the column for logarithm of message lengths.
        age_col (str): Name of the column for ages.
        emoji_status_col (str): Name of the column for emoji status.
        year_col (str): Name of the column for years.
        language_col (str): Name of the column for languages.
        hour_col (str): Name of the column for hours.
        date_col (str): Name of the column for dates.
        isoweek_col (str): Name of the column for ISO weeks.
        year_week_col (str): Name of the column for year-week.
        timeformat (str): String format for date and time.
        basic_color (str): Default color for plots.
        color_palette (list): List of colors for plotting.
        basic_color_highlight (str): Highlight color for plots.
        color_vertical_line (str): Color for vertical lines in plots.
    """
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
    language_col: str
    hour_col: str
    date_col: str
    isoweek_col: str
    year_week_col: str
    timeformat: str
    basic_color: str
    color_palette: list
    basic_color_highlight: str
    color_vertical_line: str
    people_topic: str
    other_topic: str
    homecoming_topic: str
    travel_topic: str
    food_topic: str


@dataclass
class BaseStrings:
    """
    A class to hold various string lists and dictionaries for processing.

    Attributes:
        dutch_stopwords (list): List of Dutch stopwords.
        italian_stopwords (list): List of Italian stopwords.
        dutch_frequentwords (list): List of frequently used Dutch words.
        italian_frequentwords (list): List of frequently used Italian words.
        topic_keywords (dict): Dictionary of keywords associated with topics.
    """
    dutch_stopwords: list
    italian_stopwords: list
    dutch_frequentwords: list
    italian_frequentwords: list
    topic_keywords: dict
 
@dataclass
class Folders:
    """
    A class to represent folder paths for data processing.

    Attributes:
        raw (Path): Path to the folder containing raw data.
        processed (Path): Path to the folder for processed data.
        datafile (Path): Path to the main data file.
        rawdatafile (Path): Path to the source data file.
        csvraw: (Path): Path to the source csv file.
        csv (Path): Path to output CSV file.
        
    """
    raw: Path
    csv: Path
    processed: Path
    datafile: Path
    rawdatafile: Path # source datafile
    csvraw : Path

    def __repr__(self):
        return (f"Folders(raw={self.raw}, processed={self.processed},"
                f"datafile={self.datafile}, rawdatafile={self.rawdatafile}," 
                f"csv={self.csv}, csvraw={self.csvraw}")

@dataclass
class Embedding:
    metadata: list
    vectors: np.ndarray

    def __getitem__(self, idx: int) -> tuple:
        return (self.vectors[idx], self.metadata[idx])

    def __len__(self) -> int:
        return len(self.metadata)

    def __repr__(self) -> str:
        return f"Embedding, dims={self.vectors.shape}"

basicConfig = Config(
        img_dir = Path('img/').resolve(),
        timestamp_col = 'timestamp',
        message_col = 'message',
        author_col = 'author',
        has_emoji_col= 'has_emoji',
        message_length_col= 'message_length',
        topic_col='topic',
        log_length_col= 'log_len',
        age_col= 'age',
        emoji_status_col= 'emoij_status',
        year_col= 'year',
        language_col = 'language',
        hour_col = 'hour',
        date_col = 'date',
        isoweek_col = 'isoweek',
        year_week_col = 'year-week',
        timeformat= "%Y-%m-%d",
        basic_color= 'gray',
        color_palette= ['salmon', 'gray', '#444', 'darkgray', '#EEE',"lightgray"],
        basic_color_highlight = 'salmon',
        color_vertical_line = '#EEE',
        people_topic = 'mensen',
        other_topic = 'anders',
        homecoming_topic ='kom thuis',
        travel_topic = 'reizen',
        food_topic ='eten',
    )
    
keywordsFilter = BaseStrings(
            dutch_stopwords  = ["aan","aangaande","aangezien","achte","achter","achterna","af","afgelopen","al","aldaar","aldus","alhoewel","alias","alle","allebei","alleen","alles","als","alsnog","altijd","altoos","ander","andere","anders","anderszins","beetje","behalve","behoudens","beide","beiden","ben","beneden","bent","bepaald","betreffende","bij","bijna","bijv","binnen","binnenin","blijkbaar","blijken","boven","bovenal","bovendien","bovengenoemd","bovenstaand","bovenvermeld","buiten","bv","daar","daardoor","daarheen","daarin","daarna","daarnet","daarom","daarop","daaruit","daarvanlangs","dan","dat","de","deden","deed","der","derde","derhalve","dertig","deze","dhr","die","dikwijls","dit","doch","doe","doen","doet","door","doorgaand","drie","duizend","dus","echter","een","eens","eer","eerdat","eerder","eerlang","eerst","eerste","eigen","eigenlijk","elk","elke","en","enig","enige","enigszins","enkel","er","erdoor","erg","ergens","etc","etcetera","even","eveneens","evenwel","gauw","ge","gedurende","geen","gehad","gekund","geleden","gelijk","gemoeten","gemogen","genoeg","geweest","gewoon","gewoonweg",'goede','goed',"haar","haarzelf","had","hadden","hare","heb","hebben","hebt","hedden","heeft","heel","hem","hemzelf","hen","het","hetzelfde","hier","hierbeneden","hierboven","hierin","hierna","hierom","hij","hijzelf","hoe","hoewel","honderd","hun","hunne","ieder","iedere","iedereen","iemand","iets","ik","ikzelf", "inderdaad","inmiddels","intussen","inzake","is","ja","je","jezelf","jij","jijzelf","jou","jouw","jouwe","juist","jullie","kan","klaar","kon","konden","krachtens","kun","kunnen","kunt","laatst","later","liever","lijken","lijkt","maak","maakt","maakte","maakten","maar","mag","maken","me","meer","meest","meestal","men","met","mevr","mezelf","mij","mijn","mijnent","mijner","mijzelf","minder","miss","misschien","missen","mits","mocht","mochten","moest","moesten","moet","moeten","mogen","mr","mrs","mw","na","naar","nadat","nam","namelijk","nee","neem","negen","nemen","nergens","net","niemand","niet","niets","niks","noch","nochtans","nog","nogal","nooit","nu","nv","of","ofschoon","om","omdat","omhoog","omlaag","omstreeks","omtrent","omver","ondanks","onder","ondertussen","ongeveer","ons","onszelf","onze","onzeker","ooit","ook","op","opnieuw","opzij","over","overal","overeind","overige","overigens","paar","pas","precies","recent","redelijk","reeds","rond","rondom","samen","sedert","sinds","sindsdien","slechts","sommige","spoedig","steeds","tamelijk","te","tegen","tegenover","tenzij","terwijl","thans","tien","tiende","tijdens","tja","toch","toe","toen","toenmaals","toenmalig","tot","totdat","tussen","twee","tweede","u","uit","uitgezonderd","uw","vaak","vaakwat","van","vanaf","vandaan","vanuit","vanwege","veel","veeleer","veertig","verder","verscheidene","verschillende","vervolgens","vier","vierde","vijf","vijfde","vijftig","vol","volgend","volgens","voor","vooraf","vooral","vooralsnog","voorbij","voordat","voordezen","voordien","voorheen","voorop","voorts","vooruit","vrij","vroeg","waar","waarom","waarschijnlijk","wanneer","want","waren","was","wat","we","wederom","weer","weg","wegens","weinig","wel","weldra","welk","welke","werd","werden","werder","wezen","whatever","wie","wiens","wier","wij","wijzelf","wil","wilden","willen","word","worden","wordt","zal","ze","zei","zeker","zelf","zelfde","zelfs","zes","zeven","zich","zichzelf","zij","zijn","zijne","zijzelf","zo","zoals","zodat","zodra","zonder","zou","zouden","zowat","zulk","zulke","zullen","zult",'turks', 'ivm'],
            dutch_frequentwords = ['dankjewel', 'toch', 'sowieso', 'dank', 'hoi','ok', 'oké', 'okay', 'top', 'huh','omg', 'lol', 'yeah', 'leuk', 'hoor', 'gezellig','turks', 'goed', 'mama', 'papa', 'mooi', 'straks', 'gefeliciteeeeeerd', 'gefeliciteerd','even', 'ga', 'natuurlijk', 'hè', 'zoek', 'pfff', 'wow', 'wowowow', 'wowowowowow'],
            italian_stopwords  = ['grazie', 'ciao', 'pizza', "a","abbastanza","abbia","abbiamo","abbiano","abbiate","accidenti","ad","adesso","affinché","agl","agli","ahime","ahimè","ai","al","alcuna","alcuni","alcuno","all'","alla","alle","allo","allora","altre","altri","altrimenti","altro","altrove","altrui","anche","ancora","anni","anno","ansa","anticipo","assai","attesa","attraverso","avanti","avemmo","avendo","avente","aver","avere","averlo","avesse","avessero","avessi","avessimo","aveste","avesti","avete","aveva","avevamo","avevano","avevate","avevi","avevo","avrai","avranno","avrebbe","avrebbero","avrei","avremmo","avremo","avreste","avresti","avrete","avrà","avrò","avuta","avute","avuti","avuto","basta","ben","bene","benissimo","brava","bravo","buono","c","caso","cento","certa","certe","certi","certo","che","chi","chicchessia","chiunque","ci","ciascuna","ciascuno","cima","cinque","cio","cioe","cioè","circa","citta","città","ciò","co","codesta","codesti","codesto","cogli","coi","col","colei","coll","coloro","colui","come","cominci","comprare","comunque","con","concernente","conclusione","consecutivi","consecutivo","consiglio","contro","cortesia","cos","cosa","cosi","così","cui","d","da","dagl","dagli","dai","dal","dall","dalla","dalle","dallo","dappertutto","davanti","degl","degli","dei","del","dell","della","delle","dello","dentro","detto","deve","devo","di","dice","dietro","dire","dirimpetto","diventa","diventare","diventato","dopo","doppio","dov","dove","dovra","dovrà","dovunque","due","dunque","durante","e","ebbe","ebbero","ebbi","ecc","ecco","ed","effettivamente","egli","ella","entrambi","eppure","era","erano","eravamo","eravate","eri","ero","esempio","esse","essendo","esser","essere","essi","ex","fa","faccia","facciamo","facciano","facciate","faccio","facemmo","facendo","facesse","facessero","facessi","facessimo","faceste","facesti","faceva","facevamo","facevano","facevate","facevi","facevo","fai","fanno","farai","faranno","fare","farebbe","farebbero","farei","faremmo","faremo","fareste","faresti","farete","farà","farò","fatto","favore","fece","fecero","feci","fin","finalmente","finche","fine","fino","forse","forza","fosse","fossero","fossi","fossimo","foste","fosti","fra","frattempo","fu","fui","fummo","fuori","furono","futuro","generale","gente","gia","giacche","giorni","giorno","giu","già","gli","gliela","gliele","glieli","glielo","gliene","grande","grazie","gruppo","ha","hai","hanno","ho","i","ie","ieri","il","improvviso","inc","indietro","infatti","inoltre","insieme","intanto","intorno","invece","io","l","la","lasciato","lato","le","lei","li","lo","lontano","loro","lui","lungo","luogo","là","ma","macche","magari","maggior","mai","male","malgrado","malissimo","me","medesimo","mediante","meglio","meno","mentre","mesi","mezzo","mi","mia","mie","miei", "miliardi","milioni","minimi","mio","modo","molta","molti","moltissimo","molto","momento","mondo","ne","negl","negli","nei","nel","nell","nella","nelle","nello","nemmeno","neppure","nessun","nessuna","nessuno","niente","no","noi","nome","non","nondimeno","nonostante","nonsia","nostra","nostre","nostri","nostro","novanta","nove","nulla","nuovi","nuovo","o","od","oggi","ogni","ognuna","ognuno","oltre","oppure","ora","ore","osi","ossia","ottanta","otto","paese","parecchi","parecchie","parecchio","parte","partendo","peccato","peggio", "perche","perchè","perché","percio","perciò","perfino","pero","persino","persone","però","piedi","pieno","piglia","piu","piuttosto","più","po","pochissimo","poco","poi","poiche","possa","possedere","posteriore","posto","potrebbe","preferibilmente","presa","press", "primo","principalmente","probabilmente","promesso","proprio","puo","pure","purtroppo","può","qua","qualche","qualcosa","qualcuna","qualcuno","quale","quali","qualunque","quando","quanta","quante","quanti","quanto","quantunque","quarto","quasi","quattro","quel","quella","quelle","quelli","quello","quest","questa","queste","questi","questo","qui","quindi","quinto","realmente","recente","recentemente","registrazione","relativo","riecco","rispetto","salvo","sara","sarai","saranno","sarebbe","sarebbero","sarei","saremmo","saremo","sareste","saresti","sarete","sarà","sarò","scola","scopo","scorso","se","secondo","seguente","seguito","sei","sembra","sembrare","sembrato","sembrava","sembri","sempre","senza","sette","si","sia","siamo","siano","siate","siete","sig","solito","solo","soltanto","sono","sopra","soprattutto","sotto","spesso","sta","stai","stando","stanno","starai","staranno","starebbe","starebbero","starei","staremmo","staremo","stareste","staresti","starete","starà","starò","stata","state","stati","stato","stava","stavamo","stavano","stavate","stavi","stavo","stemmo","stessa","stesse","stessero","stessi","stessimo","stesso","steste","stesti","stette","stettero","stetti","stia","stiamo","stiano","stiate","sto","su","sua","subito","successivamente","successivo","sue","sugl","sugli","sui","sul","sull","sulla","sulle","sullo","suo","suoi","tale","tali","talvolta","tanto","te","tempo","terzo","th","ti","titolo","tra","tranne","tre","trenta","triplo","troppo","trovato","tu","tua","tue","tuo","tuoi","tutta","tuttavia","tutte","tutti","tutto","uguali","ulteriore","ultimo","un","una","uno","uomo","va","vai","vale","vari","varia","varie","vario","verso","vi","vicino","visto","vita","voi","volta","volte","vostra","vostre","vostri","vostro","è"],
            italian_frequentwords  = ['grazie', 'ciao', 'pizza', 'buon', 'nonni', 'nonno', 'nonna', 'dentro', 'essere',  'uffa', 'eh', 'immagino'],
            # Define keywords for each category
            topic_keywords = {
                basicConfig.food_topic: ['kom naar', 'thuis', 'huis', 'naar huis', 'a casa', 'hoe laat', 'hoelaat', 'laat', 'slapen', 'slaap bij', 'donker', 'bed', 'thuis', 'huis', 'terug', 'blijf bij', 'ik ben in','onderweg', 'casa', 'notte', 'nacht', 'sleutel', 'blijven', 'vannacht'],
                basicConfig.travel_topic: [
                    'hilversum', 'amsterdam', 'reis', 'arrivati', 'aangekomen', 'vertrek', 'ingecheckt', 'bus', 'trein',
                    'dallas', 'spanje', 'mexico', 'boot', 'indonesië', 'hotel', 'florence', 'italie', 'schiphol', 'grado', 'tiare', 'ho chi minh', 
                ],
                basicConfig.food_topic: [
                    r'\beten\b', 'eet', "gegeten", 'blijf eten', 'lunch', 
                    'pizza', 'pasta', 'mangia', 'pranzo', 'cena', 
                    'prosciutto', 'kip', 'latte', 'snack', 
                    'indonesisch', 'kapsalon', 'kps', 'delfino', 
                    'ninh', 'bihn', 'spareribs', 'vis', 'restaurant'
                ],           
                
                #'plannen': ['vanavond', 'vandaag', 'morgen', 'afspraak', 'domani', 'stasera', 'ochtend', 'oggi', 'domani'],
                basicConfig.people_topic: [
                    'papa', 'mama', 'nonno', 'nonna', 'giacomo', 'greta','nonni',
                    'opa', 'oma', 'siem', 'tessa', 'ouders', 'mila', 'julia', 'vera'
                ]
            }
        )





extraRegexes = BaseRegexes(patterns={
            #patterns to delete from messages
            "email" : r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", # detect all emails
            "date_phone" : r'^\d{2}-\d{2}-\d{4} \d{2}:\d{2} - \+\d{2} \d{2} \d{4} \d{4}: ', # detect date followed by phone
            "bericht_verwijderd": r'bericht verwijderd', # delete message about deleted messages 
            "return_newline": r'[\r\n?]', # returns en new lines
            "username_pattern" : r"^@[a-zA-Z0-9._]+",
            "@telefoonummer": r"@\d{10,13}"
        } )    
