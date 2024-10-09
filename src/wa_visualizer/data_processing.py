from wa_visualizer.basis import DataObject
import datetime
from loguru import logger
import pandas as pd

dutch_stopwords = ['leuk', 'hoor', 'gezellig', "aan","aangaande","aangezien","achte","achter","achterna","af","afgelopen","al","aldaar","aldus","alhoewel","alias","alle","allebei","alleen","alles","als","alsnog","altijd","altoos","ander","andere","anders","anderszins","beetje","behalve","behoudens","beide","beiden","ben","beneden","bent","bepaald","betreffende","bij","bijna","bijv","binnen","binnenin","blijkbaar","blijken","boven","bovenal","bovendien","bovengenoemd","bovenstaand","bovenvermeld","buiten","bv","daar","daardoor","daarheen","daarin","daarna","daarnet","daarom","daarop","daaruit","daarvanlangs","dan","dat","de","deden","deed","der","derde","derhalve","dertig","deze","dhr","die","dikwijls","dit","doch","doe","doen","doet","door","doorgaand","drie","duizend","dus","echter","een","eens","eer","eerdat","eerder","eerlang","eerst","eerste","eigen","eigenlijk","elk","elke","en","enig","enige","enigszins","enkel","er","erdoor","erg","ergens","etc","etcetera","even","eveneens","evenwel","gauw","ge","gedurende","geen","gehad","gekund","geleden","gelijk","gemoeten","gemogen","genoeg","geweest","gewoon","gewoonweg","haar","haarzelf","had","hadden","hare","heb","hebben","hebt","hedden","heeft","heel","hem","hemzelf","hen","het","hetzelfde","hier","hierbeneden","hierboven","hierin","hierna","hierom","hij","hijzelf","hoe","hoewel","honderd","hun","hunne","ieder","iedere","iedereen","iemand","iets","ik","ikzelf","in","inderdaad","inmiddels","intussen","inzake","is","ja","je","jezelf","jij","jijzelf","jou","jouw","jouwe","juist","jullie","kan","klaar","kon","konden","krachtens","kun","kunnen","kunt","laatst","later","liever","lijken","lijkt","maak","maakt","maakte","maakten","maar","mag","maken","me","meer","meest","meestal","men","met","mevr","mezelf","mij","mijn","mijnent","mijner","mijzelf","minder","miss","misschien","missen","mits","mocht","mochten","moest","moesten","moet","moeten","mogen","mr","mrs","mw","na","naar","nadat","nam","namelijk","nee","neem","negen","nemen","nergens","net","niemand","niet","niets","niks","noch","nochtans","nog","nogal","nooit","nu","nv","of","ofschoon","om","omdat","omhoog","omlaag","omstreeks","omtrent","omver","ondanks","onder","ondertussen","ongeveer","ons","onszelf","onze","onzeker","ooit","ook","op","opnieuw","opzij","over","overal","overeind","overige","overigens","paar","pas","per","precies","recent","redelijk","reeds","rond","rondom","samen","sedert","sinds","sindsdien","slechts","sommige","spoedig","steeds","tamelijk","te","tegen","tegenover","tenzij","terwijl","thans","tien","tiende","tijdens","tja","toch","toe","toen","toenmaals","toenmalig","tot","totdat","tussen","twee","tweede","u","uit","uitgezonderd","uw","vaak","vaakwat","van","vanaf","vandaan","vanuit","vanwege","veel","veeleer","veertig","verder","verscheidene","verschillende","vervolgens","via","vier","vierde","vijf","vijfde","vijftig","vol","volgend","volgens","voor","vooraf","vooral","vooralsnog","voorbij","voordat","voordezen","voordien","voorheen","voorop","voorts","vooruit","vrij","vroeg","waar","waarom","waarschijnlijk","wanneer","want","waren","was","wat","we","wederom","weer","weg","wegens","weinig","wel","weldra","welk","welke","werd","werden","werder","wezen","whatever","wie","wiens","wier","wij","wijzelf","wil","wilden","willen","word","worden","wordt","zal","ze","zei","zeker","zelf","zelfde","zelfs","zes","zeven","zich","zichzelf","zij","zijn","zijne","zijzelf","zo","zoals","zodat","zodra","zonder","zou","zouden","zowat","zulk","zulke","zullen","zult", 'turkse']
italian_stopwords = ['grazie', 'ciao', 'pizza', "a","abbastanza","abbia","abbiamo","abbiano","abbiate","accidenti","ad","adesso","affinché","agl","agli","ahime","ahimè","ai","al","alcuna","alcuni","alcuno","all","alla","alle","allo","allora","altre","altri","altrimenti","altro","altrove","altrui","anche","ancora","anni","anno","ansa","anticipo","assai","attesa","attraverso","avanti","avemmo","avendo","avente","aver","avere","averlo","avesse","avessero","avessi","avessimo","aveste","avesti","avete","aveva","avevamo","avevano","avevate","avevi","avevo","avrai","avranno","avrebbe","avrebbero","avrei","avremmo","avremo","avreste","avresti","avrete","avrà","avrò","avuta","avute","avuti","avuto","basta","ben","bene","benissimo","brava","bravo","buono","c","caso","cento","certa","certe","certi","certo","che","chi","chicchessia","chiunque","ci","ciascuna","ciascuno","cima","cinque","cio","cioe","cioè","circa","citta","città","ciò","co","codesta","codesti","codesto","cogli","coi","col","colei","coll","coloro","colui","come","cominci","comprare","comunque","con","concernente","conclusione","consecutivi","consecutivo","consiglio","contro","cortesia","cos","cosa","cosi","così","cui","d","da","dagl","dagli","dai","dal","dall","dalla","dalle","dallo","dappertutto","davanti","degl","degli","dei","del","dell","della","delle","dello","dentro","detto","deve","devo","di","dice","dietro","dire","dirimpetto","diventa","diventare","diventato","dopo","doppio","dov","dove","dovra","dovrà","dovunque","due","dunque","durante","e","ebbe","ebbero","ebbi","ecc","ecco","ed","effettivamente","egli","ella","entrambi","eppure","era","erano","eravamo","eravate","eri","ero","esempio","esse","essendo","esser","essere","essi","ex","fa","faccia","facciamo","facciano","facciate","faccio","facemmo","facendo","facesse","facessero","facessi","facessimo","faceste","facesti","faceva","facevamo","facevano","facevate","facevi","facevo","fai","fanno","farai","faranno","fare","farebbe","farebbero","farei","faremmo","faremo","fareste","faresti","farete","farà","farò","fatto","favore","fece","fecero","feci","fin","finalmente","finche","fine","fino","forse","forza","fosse","fossero","fossi","fossimo","foste","fosti","fra","frattempo","fu","fui","fummo","fuori","furono","futuro","generale","gente","gia","giacche","giorni","giorno","giu","già","gli","gliela","gliele","glieli","glielo","gliene","grande","grazie","gruppo","ha","haha","hai","hanno","ho","i","ie","ieri","il","improvviso","in","inc","indietro","infatti","inoltre","insieme","intanto","intorno","invece","io","l","la","lasciato","lato","le","lei","li","lo","lontano","loro","lui","lungo","luogo","là","ma","macche","magari","maggior","mai","male","malgrado","malissimo","me","medesimo","mediante","meglio","meno","mentre","mesi","mezzo","mi","mia","mie","miei","mila","miliardi","milioni","minimi","mio","modo","molta","molti","moltissimo","molto","momento","mondo","ne","negl","negli","nei","nel","nell","nella","nelle","nello","nemmeno","neppure","nessun","nessuna","nessuno","niente","no","noi","nome","non","nondimeno","nonostante","nonsia","nostra","nostre","nostri","nostro","novanta","nove","nulla","nuovi","nuovo","o","od","oggi","ogni","ognuna","ognuno","oltre","oppure","ora","ore","osi","ossia","ottanta","otto","paese","parecchi","parecchie","parecchio","parte","partendo","peccato","peggio","per","perche","perchè","perché","percio","perciò","perfino","pero","persino","persone","però","piedi","pieno","piglia","piu","piuttosto","più","po","pochissimo","poco","poi","poiche","possa","possedere","posteriore","posto","potrebbe","preferibilmente","presa","press","prima","primo","principalmente","probabilmente","promesso","proprio","puo","pure","purtroppo","può","qua","qualche","qualcosa","qualcuna","qualcuno","quale","quali","qualunque","quando","quanta","quante","quanti","quanto","quantunque","quarto","quasi","quattro","quel","quella","quelle","quelli","quello","quest","questa","queste","questi","questo","qui","quindi","quinto","realmente","recente","recentemente","registrazione","relativo","riecco","rispetto","salvo","sara","sarai","saranno","sarebbe","sarebbero","sarei","saremmo","saremo","sareste","saresti","sarete","sarà","sarò","scola","scopo","scorso","se","secondo","seguente","seguito","sei","sembra","sembrare","sembrato","sembrava","sembri","sempre","senza","sette","si","sia","siamo","siano","siate","siete","sig","solito","solo","soltanto","sono","sopra","soprattutto","sotto","spesso","sta","stai","stando","stanno","starai","staranno","starebbe","starebbero","starei","staremmo","staremo","stareste","staresti","starete","starà","starò","stata","state","stati","stato","stava","stavamo","stavano","stavate","stavi","stavo","stemmo","stessa","stesse","stessero","stessi","stessimo","stesso","steste","stesti","stette","stettero","stetti","stia","stiamo","stiano","stiate","sto","su","sua","subito","successivamente","successivo","sue","sugl","sugli","sui","sul","sull","sulla","sulle","sullo","suo","suoi","tale","tali","talvolta","tanto","te","tempo","terzo","th","ti","titolo","tra","tranne","tre","trenta","triplo","troppo","trovato","tu","tua","tue","tuo","tuoi","tutta","tuttavia","tutte","tutti","tutto","uguali","ulteriore","ultimo","un","una","uno","uomo","va","vai","vale","vari","varia","varie","vario","verso","vi","vicino","visto","vita","voi","volta","volte","vostra","vostre","vostri","vostro","è"]

class Preprocess(DataObject):
    def __init__(self, datafile):
        super().__init__(datafile)
        self.whatsapp_topics={}


    def clean_message(self, text):
        #removes return and new lines

        return re.sub(r'[\r\n?]', '', text)
        
    def clean_data(self):
        # Implement data cleaning logic
        # remove returns and new lines
        self.df['message'] = self.df['message'].appy(lambda x: self.clean_message(x))
       # self.remove_stopwords_in_df(self, languages=False, path='', column = "Word")


    def guess_language(self, text):
        # Load spaCy models for Italian and Dutch
        guessed_language = None
        # Clean using regex
        
        text=text.split(" ")
        if '<Media' in text:
            guessed_language= "Non-verbal"
            return guessed_language
        
        if len(text)==1:
            guessed_language = 'Non-verbal'
            return  guessed_language 
        
        for word in text:              
                if word in ['per', 'via']:
                    return
                if word in dutch_stopwords:
                    guessed_language = "NL"
                    return guessed_language
                    break
                    
                if word in italian_stopwords:
                    guessed_language = "IT"
                    return guessed_language
                    break
                

    def process_languageID(self):
        
        self.df['language'] = "Unknown"
        self.df['language'] = self.df['message'].apply(self.guess_language)


    def process_dates(self):    
        self.df["date"] = self.df["timestamp"].dt.date
        self.df["isoweek"] = self.df["timestamp"].dt.isocalendar().week
        self.df["year-week"] = self.df["timestamp"].dt.strftime("%Y-%W")
     

    def prepocess_week1(self):
        print("processing visual 1")
        self.process_languageID()
    
    def select_dates(self, df, start_date, end_date):
        if 'date' in df:
            # Select DataFrame rows between two dates
            mask = (df['date'] > start_date) & (df['date'] <= end_date)
            return df.loc[mask]
        else:
            logger.info('No date column to select')
            return None
    
    def calc_messages(self, df):
        print(df.columns)
        
        topk = list(df[df["is_topk"]].author.unique())
        p = df.groupby("year-week").count()     #group by the isoweeks
        min_ts = df["timestamp"].min()
        max_ts = df["timestamp"].max()
        new_index = pd.date_range(start=min_ts, end=max_ts, freq='W', name="year-week").strftime('%Y-%W')
        return p.reindex(new_index, fill_value=0)

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
        df = self.df
        #needs to be refactored
        df['hour'] = df['timestamp'].dt.hour
        # Define keywords for each category
        eten_keywords = ['eten', 'pizza', 'pasta', 'mangia', 'pranzo', 'cena', 'prosciutto', 'kip', 'latte']
        plans_keywords = ['vanavond', 'vandaag', 'morgen', 'afspraak', 'domani', 'stasera']
        place_keywords = ['trein', 'hilversum', 'amsterdam', 'thuis', 'huis', 'ik ben in']
        people_keywords = ['irene', 'lorenzo', 'papa', 'mama', 'nonno', 'nonna', 'giacomo', 'opa', 'oma']

        # Apply keyword checks
        df['contains_eten'] = self.contains_keywords(df['message'], eten_keywords)
        df['contains_plans'] = self.contains_keywords(df['message'], plans_keywords)

        # Filter DataFrame to remove rows that contain 'eten'
        df2 = df[~df['contains_eten']]

        # Check for places in the filtered DataFrame
        df['contains_place'] = self.contains_keywords(df2['message'], place_keywords)

        # Optionally, if you need another filtered DataFrame
        df3 = df2[~df2['contains_eten']] 

        df['contains_people'] = self.contains_keywords(df3['message'], people_keywords)

        #create topics counts
        self.whatsapp_topics = {
        'food': df[df['contains_eten'].fillna(False)]['hour'].value_counts().sort_index(),
        'plans': df[df['contains_plans'].fillna(False)]['hour'].value_counts().sort_index(),
        'place': df[df['contains_place'].fillna(False)]['hour'].value_counts().sort_index(),
        'people': df[df['contains_people'].fillna(False)]['hour'].value_counts().sort_index(),
         }

        # Convert to DataFrames
        hour_counts1 = pd.Series(self.whatsapp_topics['food'], name='Food')
        hour_counts2 = pd.Series(self.whatsapp_topics['plans'], name='Plans')
        hour_counts3 = pd.Series(self.whatsapp_topics['place'], name='Places')
        hour_counts4 = pd.Series(self.whatsapp_topics['people'], name='People')

        # Create a DataFrame and reindex to ensure all hours are included
        df_counts = pd.DataFrame({
            'Food': hour_counts1,
            'Plans': hour_counts2,           
            'People': hour_counts4,
            'Places': hour_counts3,            
        }).fillna(0).reindex(range(24), fill_value=0)
        return df_counts

    def transform_data(self):
        # Implement any transformations needed for visualization

        # add language column for visualization 1
        self.process_languageID()

        # add date transformation for visualizazion 2
        self.process_dates()


    def get_processed_data(self):
        # Return the processed data
        return self.data
