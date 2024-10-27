import datetime
from pathlib import Path
import tomllib
from loguru import logger
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import click
import numpy as np

from wa_visualizer.data_processing import Preprocessor
from wa_visualizer.settings import (BaseRegexes, Folders, Config, BaseStrings)
from wa_visualizer.base_dataobj import FileHandler
from wa_visualizer.visual_1 import BarPlotVisualizer
from wa_visualizer.visual_2 import TimeSeriesPlotVisualizer
from wa_visualizer.visual_4 import RelationshipsPlotVisualizer
from loguru import logger

# Set up the logger
#logging.basicConfig(level=logging.INFO)
#logger = logging.getLogger(__name__)



# class Visualizer():
#     """
#     Manages the visualizations and receives data from the preprocessor.

#     Args:
#         Preprocess (class): class for proprocess steps
#     """    
#     def __init__(self, preprocessor :Preprocessor):
#       # super().__init__(folders, regexes, config, strings)
#        self.config = preprocessor.config
#        self.preprocessor = preprocessor
    
#     def visualization_week1(self):
#         processed_data = self.preprocessor.prepocess_week1()
#         plot1 = BarPlot(title_fig="A Picture Isn't Worth a Thousand Words",
#                                   ylabel="Percentage",
#                                   xlabel="Author",
#                                   filename= "1_categories_visualization.png",
#                                   config=self.config)
#         plot1(processed_data, False)

#     def visualization_week2(self):
#         df_corona, df = self.preprocessor.prepocess_week2()
#         p = self.preprocessor.calc_messages(df)
#         p_corona = self.preprocessor.calc_messages(df_corona)
#         visualization2 = TimeSeriesPlot(
#                          title_fig="Digital Silence: The WhatsApp Whisper During Lockdown",
#                          xlabel="Date: year-week",
#                          ylabel="Number of messages",
#                          filename = "2_timeseries_visualization.png",
#                          config=self.config, 
#                          show_legend = False # do not show legend in this plot 
#                          )
#         visualization2(p, p_corona)        

#     def visualization_week3(self):
       
#         df_counts_normalized = self.preprocessor.preprocess_week3()
#         self.config.custom_colors = ["lightgray", 'gray', "#333",'salmon', '#EEE',  '#444']
#         # Create the visualization instance
#         plot3 = BarPlot(title_fig='Are you Coming Home? Late-Night WhatsApp Chats with Teens',
#                                   ylabel='Percentage of Total Messages',
#                                   xlabel='Hour of the Day',
#                                   filename= "3_categories_visualization.png",
#                                   config=self.config,
#                                   legend_title = 'Topics')
#         plot3(df_counts_normalized, True)
    
#     def visualization_week4(self):
#         #avg_log_length_withemoji, avg_log_length_withoutemoji = self.preprocessor.preprocess_week4()
#         avg_log_df = self.preprocessor.preprocess_week4()

#         #Create the plot
#         plot = RelationshipsPlot(
#             config=self.config,
#             title_fig="Getting Slower Fingers with Age: Adults Save (Typing) Time with Emoji's",
#             xlabel='Author Age',
#             ylabel='Average Log of Message Length',
#             filename='4_relationships_visualization.png')

#         # Call the plot
#         plot(avg_log_df, 'age', 'log_len', scatter_size=60)


@click.command()
@click.option("--week", default="1", help="Week number: input 1 to 7")
@click.option("--all", default=False, help="All visualizations")
def main(week, all):
    possible_options = ["all", '1', '2', '3', '4', '5', '6', '7']
    if week not in possible_options:
        raise ValueError('Must be a number between 1 and 7')

    configfile = Path("./config.toml").resolve()

    with open("config.toml", "rb") as f:
        config = tomllib.load(f)
        raw = Path(config["raw"])
        processed = Path(config["processed"])
        datafile = Path(config["input"])
        current = Path(config["current"])

    datafile = (Path(".") / processed / config["current"]).resolve()

    if not datafile.exists():
        logger.warning("Datafile does not exist.")
    else:
        folders = Folders(
        raw = raw,
        processed = processed,
        datafile = datafile,
        current = current,       
        )

        config = Config(
        img_dir = Path('img/').resolve(),       
        timestamp_col = 'timestamp',
        message_col = 'message',
        author_col = 'author',
        has_emoji_col= 'has_emoji',
        message_length_col= 'message_length',
        timeformat= "%Y-%m-%d"
    )

        regexes = BaseRegexes(patterns={
            "email" : r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}",
            "date_phone" : r'^\d{2}-\d{2}-\d{4} \d{2}:\d{2} - \+\d{2} \d{2} \d{4} \d{4}: ',
            "telephone" : r"@\d{10,13}(?:[ ;:,.]|)",
            "return_newline": r'[\r\n?]',
            # "username_pattern" : r"^@[a-zA-Z0-9._]+"
        } )

        strings = BaseStrings(
            dutch_stopwords  = ['ok','leuk', 'hoor', 'gezellig', "aan","aangaande","aangezien","achte","achter","achterna","af","afgelopen","al","aldaar","aldus","alhoewel","alias","alle","allebei","alleen","alles","als","alsnog","altijd","altoos","ander","andere","anders","anderszins","beetje","behalve","behoudens","beide","beiden","ben","beneden","bent","bepaald","betreffende","bij","bijna","bijv","binnen","binnenin","blijkbaar","blijken","boven","bovenal","bovendien","bovengenoemd","bovenstaand","bovenvermeld","buiten","bv","daar","daardoor","daarheen","daarin","daarna","daarnet","daarom","daarop","daaruit","daarvanlangs","dan","dat","de","deden","deed","der","derde","derhalve","dertig","deze","dhr","die","dikwijls","dit","doch","doe","doen","doet","door","doorgaand","drie","duizend","dus","echter","een","eens","eer","eerdat","eerder","eerlang","eerst","eerste","eigen","eigenlijk","elk","elke","en","enig","enige","enigszins","enkel","er","erdoor","erg","ergens","etc","etcetera","even","eveneens","evenwel","gauw","ge","gedurende","geen","gehad","gekund","geleden","gelijk","gemoeten","gemogen","genoeg","geweest","gewoon","gewoonweg","haar","haarzelf","had","hadden","hare","heb","hebben","hebt","hedden","heeft","heel","hem","hemzelf","hen","het","hetzelfde","hier","hierbeneden","hierboven","hierin","hierna","hierom","hij","hijzelf","hoe","hoewel","honderd","hun","hunne","ieder","iedere","iedereen","iemand","iets","ik","ikzelf", "inderdaad","inmiddels","intussen","inzake","is","ja","je","jezelf","jij","jijzelf","jou","jouw","jouwe","juist","jullie","kan","klaar","kon","konden","krachtens","kun","kunnen","kunt","laatst","later","liever","lijken","lijkt","maak","maakt","maakte","maakten","maar","mag","maken","me","meer","meest","meestal","men","met","mevr","mezelf","mij","mijn","mijnent","mijner","mijzelf","minder","miss","misschien","missen","mits","mocht","mochten","moest","moesten","moet","moeten","mogen","mr","mrs","mw","na","naar","nadat","nam","namelijk","nee","neem","negen","nemen","nergens","net","niemand","niet","niets","niks","noch","nochtans","nog","nogal","nooit","nu","nv","of","ofschoon","om","omdat","omhoog","omlaag","omstreeks","omtrent","omver","ondanks","onder","ondertussen","ongeveer","ons","onszelf","onze","onzeker","ooit","ook","op","opnieuw","opzij","over","overal","overeind","overige","overigens","paar","pas","precies","recent","redelijk","reeds","rond","rondom","samen","sedert","sinds","sindsdien","slechts","sommige","spoedig","steeds","tamelijk","te","tegen","tegenover","tenzij","terwijl","thans","tien","tiende","tijdens","tja","toch","toe","toen","toenmaals","toenmalig","tot","totdat","tussen","twee","tweede","u","uit","uitgezonderd","uw","vaak","vaakwat","van","vanaf","vandaan","vanuit","vanwege","veel","veeleer","veertig","verder","verscheidene","verschillende","vervolgens","vier","vierde","vijf","vijfde","vijftig","vol","volgend","volgens","voor","vooraf","vooral","vooralsnog","voorbij","voordat","voordezen","voordien","voorheen","voorop","voorts","vooruit","vrij","vroeg","waar","waarom","waarschijnlijk","wanneer","want","waren","was","wat","we","wederom","weer","weg","wegens","weinig","wel","weldra","welk","welke","werd","werden","werder","wezen","whatever","wie","wiens","wier","wij","wijzelf","wil","wilden","willen","word","worden","wordt","zal","ze","zei","zeker","zelf","zelfde","zelfs","zes","zeven","zich","zichzelf","zij","zijn","zijne","zijzelf","zo","zoals","zodat","zodra","zonder","zou","zouden","zowat","zulk","zulke","zullen","zult",'turks'],
            italian_stopwords  = ['grazie', 'ciao', 'pizza', "a","abbastanza","abbia","abbiamo","abbiano","abbiate","accidenti","ad","adesso","affinché","agl","agli","ahime","ahimè","ai","al","alcuna","alcuni","alcuno","all","alla","alle","allo","allora","altre","altri","altrimenti","altro","altrove","altrui","anche","ancora","anni","anno","ansa","anticipo","assai","attesa","attraverso","avanti","avemmo","avendo","avente","aver","avere","averlo","avesse","avessero","avessi","avessimo","aveste","avesti","avete","aveva","avevamo","avevano","avevate","avevi","avevo","avrai","avranno","avrebbe","avrebbero","avrei","avremmo","avremo","avreste","avresti","avrete","avrà","avrò","avuta","avute","avuti","avuto","basta","ben","bene","benissimo","brava","bravo","buono","c","caso","cento","certa","certe","certi","certo","che","chi","chicchessia","chiunque","ci","ciascuna","ciascuno","cima","cinque","cio","cioe","cioè","circa","citta","città","ciò","co","codesta","codesti","codesto","cogli","coi","col","colei","coll","coloro","colui","come","cominci","comprare","comunque","con","concernente","conclusione","consecutivi","consecutivo","consiglio","contro","cortesia","cos","cosa","cosi","così","cui","d","da","dagl","dagli","dai","dal","dall","dalla","dalle","dallo","dappertutto","davanti","degl","degli","dei","del","dell","della","delle","dello","dentro","detto","deve","devo","di","dice","dietro","dire","dirimpetto","diventa","diventare","diventato","dopo","doppio","dov","dove","dovra","dovrà","dovunque","due","dunque","durante","e","ebbe","ebbero","ebbi","ecc","ecco","ed","effettivamente","egli","ella","entrambi","eppure","era","erano","eravamo","eravate","eri","ero","esempio","esse","essendo","esser","essere","essi","ex","fa","faccia","facciamo","facciano","facciate","faccio","facemmo","facendo","facesse","facessero","facessi","facessimo","faceste","facesti","faceva","facevamo","facevano","facevate","facevi","facevo","fai","fanno","farai","faranno","fare","farebbe","farebbero","farei","faremmo","faremo","fareste","faresti","farete","farà","farò","fatto","favore","fece","fecero","feci","fin","finalmente","finche","fine","fino","forse","forza","fosse","fossero","fossi","fossimo","foste","fosti","fra","frattempo","fu","fui","fummo","fuori","furono","futuro","generale","gente","gia","giacche","giorni","giorno","giu","già","gli","gliela","gliele","glieli","glielo","gliene","grande","grazie","gruppo","ha","haha","hai","hanno","ho","i","ie","ieri","il","improvviso","inc","indietro","infatti","inoltre","insieme","intanto","intorno","invece","io","l","la","lasciato","lato","le","lei","li","lo","lontano","loro","lui","lungo","luogo","là","ma","macche","magari","maggior","mai","male","malgrado","malissimo","me","medesimo","mediante","meglio","meno","mentre","mesi","mezzo","mi","mia","mie","miei","mila","miliardi","milioni","minimi","mio","modo","molta","molti","moltissimo","molto","momento","mondo","ne","negl","negli","nei","nel","nell","nella","nelle","nello","nemmeno","neppure","nessun","nessuna","nessuno","niente","no","noi","nome","non","nondimeno","nonostante","nonsia","nostra","nostre","nostri","nostro","novanta","nove","nulla","nuovi","nuovo","o","od","oggi","ogni","ognuna","ognuno","oltre","oppure","ora","ore","osi","ossia","ottanta","otto","paese","parecchi","parecchie","parecchio","parte","partendo","peccato","peggio", "perche","perchè","perché","percio","perciò","perfino","pero","persino","persone","però","piedi","pieno","piglia","piu","piuttosto","più","po","pochissimo","poco","poi","poiche","possa","possedere","posteriore","posto","potrebbe","preferibilmente","presa","press","prima","primo","principalmente","probabilmente","promesso","proprio","puo","pure","purtroppo","può","qua","qualche","qualcosa","qualcuna","qualcuno","quale","quali","qualunque","quando","quanta","quante","quanti","quanto","quantunque","quarto","quasi","quattro","quel","quella","quelle","quelli","quello","quest","questa","queste","questi","questo","qui","quindi","quinto","realmente","recente","recentemente","registrazione","relativo","riecco","rispetto","salvo","sara","sarai","saranno","sarebbe","sarebbero","sarei","saremmo","saremo","sareste","saresti","sarete","sarà","sarò","scola","scopo","scorso","se","secondo","seguente","seguito","sei","sembra","sembrare","sembrato","sembrava","sembri","sempre","senza","sette","si","sia","siamo","siano","siate","siete","sig","solito","solo","soltanto","sono","sopra","soprattutto","sotto","spesso","sta","stai","stando","stanno","starai","staranno","starebbe","starebbero","starei","staremmo","staremo","stareste","staresti","starete","starà","starò","stata","state","stati","stato","stava","stavamo","stavano","stavate","stavi","stavo","stemmo","stessa","stesse","stessero","stessi","stessimo","stesso","steste","stesti","stette","stettero","stetti","stia","stiamo","stiano","stiate","sto","su","sua","subito","successivamente","successivo","sue","sugl","sugli","sui","sul","sull","sulla","sulle","sullo","suo","suoi","tale","tali","talvolta","tanto","te","tempo","terzo","th","ti","titolo","tra","tranne","tre","trenta","triplo","troppo","trovato","tu","tua","tue","tuo","tuoi","tutta","tuttavia","tutte","tutti","tutto","uguali","ulteriore","ultimo","un","una","uno","uomo","va","vai","vale","vari","varia","varie","vario","verso","vi","vicino","visto","vita","voi","volta","volte","vostra","vostre","vostri","vostro","è"],
            dutch_frequentwords = ['ok','leuk', 'hoor', 'gezellig','turks', 'goed', 'mama', 'papa', 'mooi'],
            italian_frequentwords  = ['grazie', 'ciao', 'pizza', 'mamma', 'papà', 'bel', 'buon'],
            dob_mapping = {'effervescent-camel': 2002, 'nimble-wombat':1971, 'hilarious-goldfinch':1972,
                    'spangled-rabbit':2004}
        )
        preprocessor = Preprocessor(folders, regexes, config, strings)
        bar_plot_visualizer = False

        if week.lower()=="1" or all:
            print("week 1")
            if not bar_plot_visualizer:
                bar_plot_visualizer = BarPlotVisualizer(preprocessor)
                
            bar_plot_visualizer.visualization_week1()
            

        if week.lower()=="2" or all:
            print("week 2")
            time_series_plot_visualizer = TimeSeriesPlotVisualizer(preprocessor)
            time_series_plot_visualizer.visualization_week2()
            
            

        if week.lower()=="3" or all:
            print("week 3")
            if not bar_plot_visualizer:
                bar_plot_visualizer = BarPlotVisualizer(preprocessor)
            bar_plot_visualizer.visualization_week3()
            

        if week.lower()=="4" or all:
            print("week 4")
            relationships_plot_visualizer = RelationshipsPlotVisualizer(preprocessor)
            relationships_plot_visualizer.visualization_week4()
        

if __name__ == "__main__":   
        
        main("2", all)

