from os import getenv
import re
import pymssql
import pyjson2
import json
import plotfi
import time
import math
try:
    import matplotlib.pyplot as plt
    import matplotlib.widgets as widgets
    import numpy as np
    from scipy.signal import butter,filtfilt
except:
    print("DB IN RASP?")

#server = getenv("SRVTSTVITARD\SQLEXPRESS")
#server = "SRVTSTVITARD"
#user = "Lab"
#password = "Lab$2021"
#password = getenv("Lab$2021")
#conn = pymssql.connect(server, user, password, "Lab1")
#cursor = conn.cursor()
''' LA STRUTTURA DELLA TABELLA 
Ci sono 2 tabelle 
            La prima contiene le caratteristiche della prova alla quale viene associato un indice  (k).
            La seconda Tabella contiene la lista delle tracce. Le tracce possono variare per numero ciclo ( p.es. ogni 1000  cicli c'e un salvataggio )
            Il secondo parametro determina  A2D USATO. 
            Non Ha senso memorizzare tracce nulle o costati.
            Nota informativa..... massando da numero a char l'ultima scrittura mi si  rallentata..... ma siamo passati da mattina a pomeriggio e non so che cazzo e successo.
'''
class db():
    def __init__(self,server="10.16.0.197",database="Lab1",user="Lab",password="Lab$2021",Debug=False):
        """
        def init della classe di accesso al DB(self):
        inizializza ip  nome del db etc

        :param home:server ip address attenzione DNS non funziona in autec.
        :param database : sono i nomi del db c: TestBD ,Lab + i vari db associati alle macchine
    
        :return: 0 se tutto Ok  1 se errore
        """ 
        self.server=server
        self.database=database
        self.user=user
        self.password=password
        self.conn = pymssql.connect(server, user, password, database)
        self.cursor = self.conn.cursor()
        self.Debug=Debug
        self.Descr=[]
        if(self.Debug):
            #print(record =self.cursor.fetchone())
            print("You are connected into the - ")
            print("Database Init Done %s"%database)
        
    '''
         questo metodo viene usato per chiudere la connessione
    '''
    def __del__(self):
        print("Close connection")
        self.conn.close()
    #questa tabella viene creata per definire i parametri dei test
    # attenzione  da cancellare
    #aggiunto il controllo se la tabella esiste.
    def MakeTestParameterTable(self,TableName):
        #self.conn = psycopg2.connect(database=self.database, user=self.user, password=self.password, host=self.hosts, port= self.port)
        #self.cursor = self.conn.cursor()
        """
        def MakeTestParameterTable viene usato per costruitr la tabella associata
         crea la tabella con tutti i campi definiti.... pS questa era la prima versione .... mantenuta per motivazioni storiche
        :param home: Nome della tabella dei parametri...
        :return: 0 se tutto Ok  1 se errore
        """ 
        if(self.Debug):
            cmd=("DROP TABLE IF EXISTS %s;"%TableName)
            print(cmd)
            self.cursor.execute(cmd) #NON USO IL COMANDO:::: NON CANCELLO
        stmt = ("SHOW TABLES LIKE '%s';",TableName)
        self.cursor.execute(stmt)
        result = self.cursor.fetchone()
        if result:
            return
            # there is a table named "tableName"
        else:
            # there are no tables named "tableName"
            self.sql =("CREATE TABLE %s(NomeTest CHAR(64),Dataeora CHAR(64),NomeArticolo CHAR(64),NomeRaspberry CHAR(64),NumeroBit INT,Banda INT,FrequenzaCamp INT,TestNr INT);" %TableName)
            print(self.sql)
            self.cursor.execute(self.sql)
            self.conn.commit()
    '''
    Usata per creare la tabelle che descrive la prova....
    questi parametri sono usati dal sistema .... giuliano può impostare i campi ....
    ...speriamo bene.
    '''
    def MakeConfigTable(self,TableName):
        '''
         def MakeConfigTable viene usato per costruire la tabella associata
         crea la tabella con tutti i campi definiti.... pS 70  n
        :param home: Nome della tabella dei parametri...
        :return: 0 se tutto Ok  1 se errore
        '''
        result=False
        if(self.Debug):
            cmd=("DROP TABLE IF EXISTS %s;"%TableName)
            print(cmd)
            self.cursor.execute(cmd) #NON USO IL COMANDO:::: NON CANCELLO
        stmt = ("SHOW TABLES LIKE %s;"%TableName)
        #########   self.cursor.execute(stmt)
        ########result = self.cursor.fetchone()
        if result:
            return
            # there is a table named "tableName"
        else:
            #self.sql =("CREATE TABLE %s(id CHAR(64),a2d CHAR(64),data  NVARCHAR(MAX));" %TableName)
            # there are no tables named "tableName"
            #                                1                    2                       3                 4                    5                 6                  7               8               9          10                  11                    12                     13             14                   15               16               17                 18                 19                 20                 21                 22                  23                  24                 25                26                  27                  28                29                    30                    31          32                  33                 34                    35              36                   37               38               39                    40                 41                 42                 43               44                    45                 46                 47                    48            49                 50                  51                 52                53                   54                55                   56               57               58                    59               60                     61                         62                   63         64       65       66   6 7           68         69      70                 71                 VectorParam1  NVARCHAR(MAX) VectorParam1  NVARCHAR(MAX) VectorParam1  NVARCHAR(MAX)                                                                        
            #...........................Nome della tabella......Nome Macchina......0Ip della macchina...Nome articolo......... time...........  Errore........    int start      stop ciclo    in milli secondid               millisecondi           A2D 0 SCHEDA 1       # MODO DI STATO   
            self.sql =("CREATE TABLE %s (NomeTest CHAR(64),NomeMacchina CHAR(64),IpMacchina CHAR(64),NomeArticolo CHAR(64),Dataeora CHAR(64),Errori CHAR(64),StartIndex int ,StopIndex int,DurataAcq int,FreqDiCamp int,Periododiacquisizione int,NomeA2D01 CHAR(32),NomeA2D11 CHAR(32),NomeA2D21 CHAR(32),NomeA2D31 CHAR(32),NomeA2D41 CHAR(32),NomeA2D51 CHAR(32),NomeA2D61 CHAR(32),NomeA2D71 CHAR(32),NomeA2D81 CHAR(32),NomeA2D91 CHAR(32),NomeA2DA1 CHAR(32),NomeA2DB1 CHAR(32),NomeA2DC1 CHAR(32),NomeA2DD1 CHAR(32),NomeA2DE1 CHAR(32),NomeA2DF1 CHAR(32),NomeA2D02 CHAR(32),NomeA2D12 CHAR(32),NomeA2D22 CHAR(32),NomeA2D32 CHAR(32),NomeA2D42 CHAR(32),NomeA2D52 CHAR(32),NomeA2D62 CHAR(32),NomeA2D72 CHAR(32),NomeA2D82 CHAR(32),NomeA2D92 CHAR(32),NomeA2DA2 CHAR(32),NomeA2DB2 CHAR(32),NomeA2DC2 CHAR(32),NomeA2DD2 CHAR(32),NomeA2DE2 CHAR(32),NomeA2DF2 CHAR(32),NomeA2D03 CHAR(32),NomeA2D13 CHAR(32),NomeA2D23 CHAR(32),NomeA2D33 CHAR(32),NomeA2D43 CHAR(32),NomeA2D53 CHAR(32),NomeA2D63 CHAR(32),NomeA2D73 CHAR(32),NomeA2D83 CHAR(32),NomeA2D93 CHAR(32),NomeA2DA3 CHAR(32),NomeA2DB3 CHAR(32),NomeA2DC3 CHAR(32),NomeA2DD3 CHAR(32),NomeA2DE3 CHAR(32),NomeA2DF3 CHAR(32),ciclitracontrollo int,ciclitraAcquisizione int,ciclitotali int,numerosemicilci int,pausa int,sel int,f real ,AMax real,VMax float,A0 real ,SMax real ,DACSNR1 CHAR(32),DACSNR2 CHAR(32),DACSNR3 CHAR(32));" %TableName)
            print(self.sql)
            self.cursor.execute(self.sql)
            self.conn.commit()
        '''
        obbiettivo di questa funzione è quello di scrivere i parametri del test che appunto vengono selezionati....
        Ecco  i parametri che devo scrivere:
            self.sql =("CREATE TABLE %s(NomeDatabase CHAR(64),NomeMacchina CHAR(64),IpMacchina CHAR(64),NomeArticolo CHAR(64),Dataeora CHAR(64),Errori CHAR(64),StartIndex int ,StopIndex int,DurataAcq int,FreqDiCamp int,Periododiacquisizione int,NomeA2D01 CHAR(32),NomeA2D11 CHAR(32),NomeA2D21 CHAR(32),NomeA2D31 CHAR(32),NomeA2D41 CHAR(32),NomeA2D51 CHAR(32),NomeA2D61 CHAR(32),NomeA2D71 CHAR(32),NomeA2D81 CHAR(32),NomeA2D91 CHAR(32),NomeA2DA1 CHAR(32),NomeA2DB1 CHAR(32),NomeA2DC1 CHAR(32),NomeA2DD1 CHAR(32),NomeA2DE1 CHAR(32),NomeA2DF1 CHAR(32),NomeA2D02 CHAR(32),NomeA2D12 CHAR(32),NomeA2D22 CHAR(32),NomeA2D32 CHAR(32),NomeA2D42 CHAR(32),NomeA2D52 CHAR(32),NomeA2D62 CHAR(32),NomeA2D72 CHAR(32),NomeA2D82 CHAR(32),NomeA2D92 CHAR(32),NomeA2DA2 CHAR(32),NomeA2DB2 CHAR(32),NomeA2DC2 CHAR(32),NomeA2DD2 CHAR(32),NomeA2DE2 CHAR(32),NomeA2DF2 CHAR(32),NomeA2D03 CHAR(32),NomeA2D13 CHAR(32),NomeA2D23 CHAR(32),NomeA2D33 CHAR(32),NomeA2D43 CHAR(32),NomeA2D53 CHAR(32),NomeA2D63 CHAR(32),NomeA2D73 CHAR(32),NomeA2D83 CHAR(32),NomeA2D93 CHAR(32),NomeA2DA3 CHAR(32),NomeA2DB3 CHAR(32),NomeA2DC3 CHAR(32),NomeA2DD3 CHAR(32),NomeA2DE3 CHAR(32),NomeA2DF3 CHAR(32),NumeroDiCiclo int,ManualeAutomatico,tempodisalita int,tempodidiscesa int,coppia int,posizionefermo1 int ,posizionefermo2 int,accelerazione int,velocita int ,TableName)    
        (NomeDatabase,NomeMacchina,IpMacchina,NomeArticolo,Dataeora ,Errori ,StartIndex ,StopIndex ,DurataAcq ,FreqDiCamp ,Periododiacquisizione ,NomeA2D01 ,NomeA2D11 ,NomeA2D21 ,NomeA2D31 ,NomeA2D41 ,NomeA2D51 ,NomeA2D61 ,NomeA2D71 ,NomeA2D81 ,NomeA2D91 ,NomeA2DA1 ,NomeA2DB1 ,NomeA2DC1 ,NomeA2DD1 ,NomeA2DE1 ,NomeA2DF1 ,NomeA2D02 ,NomeA2D12 ,NomeA2D22 ,NomeA2D32 ,NomeA2D42 ,NomeA2D52 ,NomeA2D62 ,NomeA2D72 ,NomeA2D82 ,NomeA2D92 ,NomeA2DA2 ,NomeA2DB2 ,NomeA2DC2 ,NomeA2DD2 ,NomeA2DE2 ,NomeA2DF2 ,NomeA2D03 ,NomeA2D13 NomeA2D23 ,NomeA2D33 ,NomeA2D43 ,NomeA2D53 ,NomeA2D63 ,NomeA2D73 ,NomeA2D83 ,NomeA2D93 ,NomeA2DA3 ,NomeA2DB3 ,NomeA2DC3,NomeA2DD3 ,NomeA2DE3,NomeA2DF3,NumeroDiCiclo,ManualeAutomatico,tempodisalita,tempodidiscesa,coppia,posizionefermo1,posizionefermo2,accelerazione,velocita)
            1              2           3           4          5        6       7            8           9        10           11                         12     13         14        15         16         17         18          19         20        21          22         23        24         25          26         27         28         29         30        31          32         33        34           35       36          37        38          39        30   

        '''
          #...........................Nome della tabella......Nome Macchina......0Ip della macchina...Nome articolo......... time...........  Errore........    int start      stop ciclo    in milli secondid               millisecondi           A2D 0 SCHEDA 1       # MODO DI STATO 
          #   self.sql =("CREATE TABLE %s(NomeDatabase CHAR(64),NomeMacchina CHAR(64),IpMacchina CHAR(64),NomeArticolo CHAR(64),Dataeora CHAR(64),Errori CHAR(64),StartIndex int ,StopIndex int,DurataAcq int,FreqDiCamp int,Periododiacquisizione int,NomeA2D01 CHAR(32),NomeA2D11 CHAR(32),NomeA2D21 CHAR(32),NomeA2D31 CHAR(32),NomeA2D41 CHAR(32),NomeA2D51 CHAR(32),NomeA2D61 CHAR(32),NomeA2D71 CHAR(32),NomeA2D81 CHAR(32),NomeA2D91 CHAR(32),NomeA2DA1 CHAR(32),NomeA2DB1 CHAR(32),NomeA2DC1 CHAR(32),NomeA2DD1 CHAR(32),NomeA2DE1 CHAR(32),NomeA2DF1 CHAR(32),NomeA2D02 CHAR(32),NomeA2D12 CHAR(32),NomeA2D22 CHAR(32),NomeA2D32 CHAR(32),NomeA2D42 CHAR(32),NomeA2D52 CHAR(32),NomeA2D62 CHAR(32),NomeA2D72 CHAR(32),NomeA2D82 CHAR(32),NomeA2D92 CHAR(32),NomeA2DA2 CHAR(32),NomeA2DB2 CHAR(32),NomeA2DC2 CHAR(32),NomeA2DD2 CHAR(32),NomeA2DE2 CHAR(32),NomeA2DF2 CHAR(32),NomeA2D03 CHAR(32),NomeA2D13 CHAR(32),NomeA2D23 CHAR(32),NomeA2D33 CHAR(32),NomeA2D43 CHAR(32),NomeA2D53 CHAR(32),NomeA2D63 CHAR(32),NomeA2D73 CHAR(32),NomeA2D83 CHAR(32),NomeA2D93 CHAR(32),NomeA2DA3 CHAR(32),NomeA2DB3 CHAR(32),NomeA2DC3 CHAR(32),NomeA2DD3 CHAR(32),NomeA2DE3 CHAR(32),NomeA2DF3 CHAR(32),ciclitracontrollo int,ciclitraAcquisizione int,ciclitotali int,numerosemicilci int,pausa int,sel int,f float ,AMax float,VMax float,A0 float ,SMax float );" %TableName)
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                
    def WriteConfigTableRaw(self,NextTable,NomeTest ,NomeMacchina ,IpMacchina,NomeArticolo ,Dataeora ,Errori,StartIndex,StopIndex ,DurataAcq ,FreqDiCamp ,Periododiacquisizione ,NomeA2D01="NULL" ,NomeA2D11="NULL",NomeA2D21="NULL",NomeA2D31="NULL",NomeA2D41="NULL",NomeA2D51="NULL",NomeA2D61="NULL",NomeA2D71="NULL",NomeA2D81="NULL",NomeA2D91="NULL",NomeA2DA1="NULL" ,NomeA2DB1="NULL",NomeA2DC1="NULL",NomeA2DD1="NULL",NomeA2DE1="NULL",NomeA2DF="NULL",NomeA2D02="NULL",NomeA2D12="NULL",NomeA2D22="NULL",NomeA2D32="NULL",NomeA2D42="NULL",NomeA2D52="NULL",NomeA2D62="NULL",NomeA2D72="NULL",NomeA2D82="NULL",NomeA2D92="NULL",NomeA2DA2="NULL",NomeA2DB2="NULL",NomeA2DC2="NULL",NomeA2DD2="NULL",NomeA2DE2="NULL",NomeA2DF2="NULL",NomeA2D03="NULL",NomeA2D13="NULL",NomeA2D23="NULL",NomeA2D33="NULL",NomeA2D43="NULL",NomeA2D53="NULL",NomeA2D63="NULL",NomeA2D73="NULL",NomeA2D83="NULL",NomeA2D93="NULL",NomeA2DA3="NULL",NomeA2DB3="NULL",NomeA2DC3="NULL",NomeA2DD3="NULL",NomeA2DE3="NULL",NomeA2DF3="NULL",ciclitracontrollo=1000,ciclitraAcquisizione=1000 ,ciclitotali=1000 ,numerosemicilci=1000 ,pausa=1000 ,sel=0 ,f=1  ,AMax=2 ,VMax=3 ,A0=4  ,SMax =5 ,DACSNR1="0206AFDA",DACSNR2="0206B095",DACSNR3="0206AFF2"): #" %TableName): 
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            
        '''
        def WriteConfigTableRaw viene usata per riempire la tabella definita sopra.
        Attenzione  i parametri sono 70 e definiscono i parametri della prova.
        La duale is la Delete che cancella una riga di test.
        crea la tabella con tutti i campi definiti.... pS 70  n
        :param home: Nome della tabella dei parametri etc  +70
        :return: 0 se tutto Ok  1 se errore
        Funzione che scrive la configuration table:
        self.sql =("CREATE TABLE %s(NomeDatabase CHAR(64),NomeMacchina CHAR(64),IpMacchina CHAR(64),NomeArticolo CHAR(64),Dataeora CHAR(64),Errori CHAR(64),StartIndex int ,StopIndex int,DurataAcq int,FreqDiCamp int,Periododiacquisizione int,NomeA2D01 CHAR(32),NomeA2D11 CHAR(32),NomeA2D21 CHAR(32),NomeA2D31 CHAR(32),NomeA2D41 CHAR(32),NomeA2D51 CHAR(32),NomeA2D61 CHAR(32),NomeA2D71 CHAR(32),NomeA2D81 CHAR(32),NomeA2D91 CHAR(32),NomeA2DA1 CHAR(32),NomeA2DB1 CHAR(32),NomeA2DC1 CHAR(32),NomeA2DD1 CHAR(32),NomeA2DE1 CHAR(32),NomeA2DF1 CHAR(32),NomeA2D02 CHAR(32),NomeA2D12 CHAR(32),NomeA2D22 CHAR(32),NomeA2D32 CHAR(32),NomeA2D42 CHAR(32),NomeA2D52 CHAR(32),NomeA2D62 CHAR(32),NomeA2D72 CHAR(32),NomeA2D82 CHAR(32),NomeA2D92 CHAR(32),NomeA2DA2 CHAR(32),NomeA2DB2 CHAR(32),NomeA2DC2 CHAR(32),NomeA2DD2 CHAR(32),NomeA2DE2 CHAR(32),NomeA2DF2 CHAR(32),NomeA2D03 CHAR(32),NomeA2D13 CHAR(32),NomeA2D23 CHAR(32),NomeA2D33 CHAR(32),NomeA2D43 CHAR(32),NomeA2D53 CHAR(32),NomeA2D63 CHAR(32),NomeA2D73 CHAR(32),NomeA2D83 CHAR(32),NomeA2D93 CHAR(32),NomeA2DA3 CHAR(32),NomeA2DB3 CHAR(32),NomeA2DC3 CHAR(32),NomeA2DD3 CHAR(32),NomeA2DE3 CHAR(32),NomeA2DF3 CHAR(32),ciclitracontrollo int,ciclitraAcquisizione int,ciclitotali int,numerosemicilci int,pausa int,sel int,f float ,AMax float,VMax float,A0 float ,SMax float );" %TableName)
        
        '''
       
        #                         71          1     2     3    4     5     6   7      8    9    10   11    12    13    14   15     16  17    18    19   20    21   22     23  24     25   26    27    28    29   30  31     32    33   34    35   36    37    38    39   40   41    42    43   44    45    46   47   48     49   50   51    52    53   54    55    56   57    58   59     60  61    62    63   64    65    66   67    68   69    70   71       1           2            3             4           5            6        7      8          9          10         11         12                         13     14          15       16        17        18       19         20        21        22         23        24         25        26        27      28        29        30         31      32        33        34        35         36        37        38         39        4 0       41       42        43        44         45       46        47         48        49        50        51         52       53        54       55          56       57         58       59         60       61                62                     63          64             65    66   67   68    69   70    71      
        self.sql = ("insert into %s  VALUES('%s', '%s', '%s','%s', '%s', '%s','%s', '%s', '%s','%s','%s', '%s', '%s','%s', '%s', '%s','%s', '%s', '%s','%s','%s', '%s', '%s','%s', '%s', '%s','%s', '%s', '%s','%s','%s', '%s', '%s','%s', '%s', '%s','%s', '%s', '%s','%s','%s', '%s', '%s','%s', '%s', '%s','%s', '%s', '%s','%s','%s', '%s', '%s','%s', '%s', '%s','%s', '%s', '%s','%s','%s', '%s', '%s','%s', '%s', '%s','%s', '%s', '%s','%s','%s','%s','%s');"%(NextTable,NomeTest ,NomeMacchina ,IpMacchina,NomeArticolo ,Dataeora ,Errori,StartIndex,StopIndex ,DurataAcq ,FreqDiCamp ,Periododiacquisizione ,NomeA2D01 ,NomeA2D11,NomeA2D21,NomeA2D31,NomeA2D41,NomeA2D51,NomeA2D61,NomeA2D71,NomeA2D81,NomeA2D91,NomeA2DA1 ,NomeA2DB1,NomeA2DC1,NomeA2DD1,NomeA2DE1,NomeA2DF,NomeA2D02,NomeA2D12,NomeA2D22,NomeA2D32,NomeA2D42,NomeA2D52,NomeA2D62,NomeA2D72,NomeA2D82,NomeA2D92,NomeA2DA2,NomeA2DB2,NomeA2DC2,NomeA2DD2,NomeA2DE2,NomeA2DF2,NomeA2D03,NomeA2D13,NomeA2D23,NomeA2D33,NomeA2D43,NomeA2D53,NomeA2D63,NomeA2D73,NomeA2D83,NomeA2D93,NomeA2DA3,NomeA2DB3,NomeA2DC3,NomeA2DD3,NomeA2DE3,NomeA2DF3,ciclitracontrollo,ciclitraAcquisizione ,ciclitotali ,numerosemicilci ,pausa ,sel ,f  ,AMax ,VMax ,A0  ,SMax,DACSNR1,DACSNR2,DACSNR3))                
        #...........................Nome della tabella......Nome Macchina......0Ip della macchina...Nome articolo......... time...........  Errore........    int start      stop ciclo    in milli secondid               millisecondi           A2D 0 SCHEDA 1       # MODO DI STATO 
        print(self.sql)
        Numero=self.cursor.execute(self.sql)
        self.conn.commit()
        return NextTable
    '''
    delete_query = DELETE FROM Books WHERE Id= 1
    cursor.execute(delete_query )
    conn.commit()
    '''
    def ReadConfigTableRaw(self,TableName):
        '''
        def ReadConfigTableRaw leggo tutta la tabella  completa....
        Attenzione  i parametri sono 70 e definiscono i parametri della prova.
        La duale is la Delete che cancella una riga di test.
        crea la tabella con tutti i campi definiti.... pS 70  n
        :param home: Nome della tabella dei parametri etc  +70
        :return: 0 se tutto Ok  1 se errore
        '''
         #Creating a cursor object using the cursor() method
        self.sql=("SELECT * from %s ;"%TableName)
        #Retrieving data
        #print(self.sql)
        self.cursor.execute(self.sql)
        #Fetching 1st row from the table
        result = self.cursor.fetchall()
        if(len(result)<1):
            print("Tabella Vuota")
            return 0,0
        else:
           
            R=[]
            i=0
            for row in result:
                data=row[0]
                lung=len(row)
                i=0
                tmp=[]
                while(i<lung):
                    tmp.append(row[i])
                    i=i+1

                
                self.Descr.append("NomeTest")
                self.Descr.append("NomeMacchina")
                self.Descr.append("IpMacchina"),
                self.Descr.append("NomeArticolo") 
                self.Descr.append("Dataeora") 
                self.Descr.append("Errori")
                self.Descr.append("StartIndex")
                self.Descr.append("StopIndex")
                self.Descr.append("DurataAcq")
                self.Descr.append("FreqDiCamp") 
                self.Descr.append("Periododiacquisizione") 
                self.Descr.append("NomeA2D01")
                self.Descr.append("NomeA2D11")
                self.Descr.append("NomeA2D21")
                self.Descr.append("NomeA2D31")
                self.Descr.append("NomeA2D41")
                self.Descr.append("NomeA2D51")
                self.Descr.append("NomeA2D61")
                self.Descr.append("NomeA2D71")
                self.Descr.append("NomeA2D81")
                self.Descr.append("NomeA2D91")
                self.Descr.append("NomeA2DA1")
                self.Descr.append("NomeA2DB1")
                self.Descr.append("NomeA2DC1")
                self.Descr.append("NomeA2DD1")
                self.Descr.append("NomeA2DE1")
                self.Descr.append("NomeA2DF1")
                self.Descr.append("NomeA2D02")
                self.Descr.append("NomeA2D12")
                self.Descr.append("NomeA2D22")
                self.Descr.append("NomeA2D32")
                self.Descr.append("NomeA2D42")
                self.Descr.append("NomeA2D52")
                self.Descr.append("NomeA2D62")
                self.Descr.append("NomeA2D72")
                self.Descr.append("NomeA2D82")
                self.Descr.append("NomeA2D92")
                self.Descr.append("NomeA2DA2")
                self.Descr.append("NomeA2DB2")
                self.Descr.append("NomeA2DC2")
                self.Descr.append("NomeA2DD2")
                self.Descr.append("NomeA2DE2")
                self.Descr.append("NomeA2DF2")
                self.Descr.append("NomeA2D03")
                self.Descr.append("NomeA2D13")
                self.Descr.append("NomeA2D23")
                self.Descr.append("NomeA2D33")
                self.Descr.append("NomeA2D43")
                self.Descr.append("NomeA2D53")
                self.Descr.append("NomeA2D63")
                self.Descr.append("NomeA2D73")
                self.Descr.append("NomeA2D83")
                self.Descr.append("NomeA2D93")
                self.Descr.append("NomeA2DA3")
                self.Descr.append("NomeA2DB3")
                self.Descr.append("NomeA2DC3")
                self.Descr.append("NomeA2DD3")
                self.Descr.append("NomeA2DE3")
                self.Descr.append("NomeA2DF3")
                self.Descr.append("ciclitracontrollo")
                self.Descr.append("ciclitraAcquisizione")
                self.Descr.append("ciclitotali") 
                self.Descr.append("numerosemicilci")
                self.Descr.append("pausa")
                self.Descr.append("sel") 
                self.Descr.append("f")
                self.Descr.append("AMax")
                self.Descr.append("VMax")
                self.Descr.append("A0")
                self.Descr.append("SMax")    
                self.Descr.append("DACSNR1") 
                self.Descr.append("DACSNR2") 
                self.Descr.append("DACSNR3") 
                self.Descr.append("VectorParam1")
                self.Descr.append("VectorParam2")
                self.Descr.append("VectorParam3")
   
                #%(NextTable,NomeDatabase ,NomeMacchina ,IpMacchina,NomeArticolo ,Dataeora ,Errori,StartIndex,StopIndex ,DurataAcq ,FreqDiCamp ,Periododiacquisizione ,NomeA2D01 ,NomeA2D11,NomeA2D21,NomeA2D31,NomeA2D41,NomeA2D51,NomeA2D61,NomeA2D71,NomeA2D81,NomeA2D91,NomeA2DA1 ,NomeA2DB1,NomeA2DC1,NomeA2DD1,NomeA2DE1,NomeA2DF,NomeA2D02,NomeA2D12,NomeA2D22,NomeA2D32,NomeA2D42,NomeA2D52,NomeA2D62,NomeA2D72,NomeA2D82,NomeA2D92,NomeA2DA2,NomeA2DB2,NomeA2DC2,NomeA2DD2,NomeA2DE2,NomeA2DF2,NomeA2D03,NomeA2D13,NomeA2D23,NomeA2D33,NomeA2D43,NomeA2D53,NomeA2D63,NomeA2D73,NomeA2D83,NomeA2D93,NomeA2DA3,NomeA2DB3,NomeA2DC3,NomeA2DD3,NomeA2DE3,NomeA2DF3,ciclitracontrollo,ciclitraAcquisizione ,ciclitotali ,numerosemicilci ,pausa ,sel ,f  ,AMax ,VMax ,A0  ,SMax
                R.append(tmp)
        return R

    def DeleteConfigTableRaw(self,TableName,ColonName,ColonValue):
        '''
        def DeleteConfigTableRaw deleto solo la parte opportuna.
        Attenzione  i parametri sono 70 e definiscono i parametri della prova.
        La duale is la Delete che cancella una riga di test.
        crea la tabella con tutti i campi definiti.... pS 70  n
        :param home: Nome della tabella dei parametri etc  +70
        :return: 0 se tutto Ok  1 se errore
        '''
        self.sql=("DELETE from %s WHERE %s in(%s);"%(TableName,ColonName,ColonValue))
        print(self.sql)
        self.cursor.execute(self.sql) #NON USO IL COMANDO:::: NON CANCELLO
        self.conn.commit()
        
        #cursor.execute('''DELETE FROM EMPLOYEE WHERE AGE > 25''')
        
        

    def DeleteAllTable(self):
        '''
        Delete tutte le tabelle presenti nel DB

        '''
        Res=self.TableNameis()
        i=0
        if(Res!=0):
            while(i<len(Res)):
                self.DeleteTable(Res[i])
                i=i+1
            return 1
        else:
            return 0

    def DeleteTable(self,Tabname):
        cmd=("DROP TABLE IF EXISTS %s;"%Tabname)
        print(cmd)
        self.cursor.execute(cmd) #NON USO IL COMANDO:::: NON CANCELLO
        self.conn.commit()

    def GetDB(self):
        '''
        questa funzione legge il db e lo grafa
        '''
        Res=self.TableNameis()
        print("TABELLE ARE",Res)
        if(Res!=0):
            i=0
            while(i<len(Res)):
                DataTab,A,B=self.ReadTable(Res[i])
                print("Numero di elementi in tabella ",len(DataTab))
                k=0
                if(len(DataTab)>1):
                    while(k<len(DataTab)):
                        print("len array is",len(DataTab[k]))
                        plt.plot(DataTab[k])
                        plt.xlabel(A)
                        plt.ylabel(B)
                        plt.show()
                        k=k+1
                i=i+1
            return
        else:
            if(self.Debug):
                k=0
                DataTab=[]
                A="A"
                B="B"
                while(k<100000):
                    DataTab.append(math.sin(0.001*k))
                    k=k+1
                plt.plot(DataTab)
                plt.xlabel(A)
                plt.ylabel(B)
                plt.show()
            return 0

    #devo dare il nome del database
    def TableNameis(self,TableName="Lab1"):
        '''
        ricerco il nome nel database le tabelle presenti
        '''
        self.sql = "SHOW TABLES FROM %s;"%TableName
        self.cursor.execute("Select * from INFORMATION_SCHEMA.TABLES")
        result = self.cursor.fetchall()
        print(result)
        i=0
        TabNames=[]
        while(i<len(result)):
            print(type(result[i]))
            print(result[i][2])
            TabNames.append(result[i][2])
            i=i+1
        if(len(TabNames)==0):
            return 0
        else:
            return TabNames

        #self.sql =("CREATE TABLE %s(NomeTest CHAR(64),Dataeora CHAR(64),NomeArticolo CHAR(64),NextTableBame CHAR(64),NomeRaspberry CHAR(64),NumeroBit INT,Banda INT,FrequenzaCamp INT,TestNr INT);" %TableName)
        #print(self.sql)
        #self.cursor.execute(self.sql)
        #self.conn.commit()
            
    def isTable(self,Tabname):
        '''
        cerco una specifica tabella Tabname 
        nel databnase selezionato 
        '''
        R=self.TableNameis()
        if(R==0):
            return False
        else:
            i=0
            while(i<len(R)):
                if(R[i]==Tabname):
                    return True
                i=i+1
            return False
        
    '''
    costrutisce i campi della tabella delle prova su questa viene riportato nome dell tabella risultati associati a quella prova.
    potrei comporrere i nomi come AD2 NUMBER DA VERIFICARE.
    '''
    
    def MakeRefTable(self,TableName):
        #self.conn = psycopg2.connect(database=self.database, user=self.user, password=self.password, host=self.hosts, port= self.port)
        #self.cursor = self.conn.cursor()
        if(self.Debug):
            cmd=("DROP TABLE IF EXISTS %s;"%TableName)
            print(cmd)
            self.cursor.execute(cmd) #Debug cancello la tabella per debug
            self.conn.commit()
        result=self.isTable(TableName)
        if result:
            print("Tabella gi presente nel DB")
            return
                # there is a table named "tableName"
        else:
            print("Aggiungo Tabella nel DB")
            self.sql =("CREATE TABLE %s(NomeTest CHAR(64),Dataeora CHAR(64),NomeArticolo CHAR(64),NextTableName CHAR(64),NomeRaspberry CHAR(64),NumeroBit INT,Banda INT,FrequenzaCamp INT,TestNr INT);" %TableName)
            print(self.sql)
            self.cursor.execute(self.sql)
            self.conn.commit()

        
    '''metto i fati nella tabella
        Data=[NomeTest,Data,NomeArticolo,NomeRasp,NumeroBit,Banda,Frequeza,TestNR]
    '''
    def InsertDataInRefTable(self,TableName,NomeTest,Dataeora,Articolo,NomeRaspberry,NumeroBit,Banda,FreqquenzaCampionamento,TestNr):
        NextTable=NomeTest+"E"+Dataeora+"E"+Articolo
        #self.sql = ("INSERT INTO %s (NomeTest,Dataeora, NomeArticolo,NomeRaspberry,NumeroBit,Banda,FrequenzaCamp, TestNr) VALUES (%s, %s, %s, %s, %s,%s, %s, %s);"%(TableName,NomeTest,Dataeora,Articolo,NomeRaspberry,NumeroBit,Banda,FreqquenzaCampionamento,TestNr))
        self.sql = ("insert into %s  VALUES('%s', '%s', '%s','%s', '%s', '%s','%s', '%s', '%s');"%(TableName,NomeTest,Dataeora,Articolo,NextTable,NomeRaspberry,NumeroBit,Banda,FreqquenzaCampionamento,TestNr))
        print(self.sql)
        self.cursor.execute(self.sql)
        self.conn.commit()
        return NextTable

    '''
    metto il raw file.....
    '''
    def MakeJsonTable(self,tablename):
        result=self.isTable(tablename)
        if result:
            print("Tabella gi presente nel DB")
            return
                # there is a table named "tableName"
        else:
            self.sql =("CREATE TABLE %s(idt int ,a2d CHAR(64),data  NVARCHAR(MAX));" %tablename)
            #######self.sql=("CREATE TABLE %s(id integer NOT NULL,NomeTest CHAR(16),date CHAR(16),NomeArticolo CHAR(16),NomeRaspberry CHAR(16),DescrizioneIngresso CHAR(16),NumeroBit INT,TestNr INT ,Banda INT,Fc INT,NumeroCampioni INT,ERRORI CHAR(16),Wave jsonb);" %tablename)
            #                              1                  2                 3              4                    5                        6                         7              8           9       10        11                12                  13   
            #print(self.sql)
            self.cursor.execute(self.sql)
            self.conn.commit()
        
    #INSERT INTO cards VALUES (1, 1, '{"name": "Paint house", "tags": ["Improvements", "Office"], "finished": true}');
    ''' salvo i dati della prova....
    '''
    def InsertJsonRawInTable(self,tablename,filename,A2DName,ciclo):
        NomeTest,data,Articolo,Nodo,DescrizIngresso,BitQuant,NumeroCiclo,Banda,Fc,NumeroCampioni,Errori=pyjson2.TestParameterRd(filename)
        jdata=pyjson2.TestParameterRdForDB(filename)
        index=1
        k=3
        A=jdata["Dati"]
        print("Numero di Dati is",len(A))
        i=0
        STRARR=""
        while(i<len(A)):
            STRARR=STRARR+("%2f4,"%A[i])
            i=i+1
        print("Added finish")
        start_time = time.time()
        self.sql = ("INSERT INTO %s VALUES ('%s','%s','%s');"%(tablename,ciclo,A2DName,STRARR))
        #########self.sql=("INSERT INTO %s VALUES (id,NomeTest CHAR(16),date CHAR(16),NomeArticolo CHAR(16),NomeRaspberry CHAR(16),DescrizioneIngresso CHAR(16),NumeroBit INT,TestNr INT ,Banda INT,Fc INT,NumeroCampioni INT,ERRORI CHAR(16),Wave jsonb) VALUES (%s , %s ,%s, %s, %s, %s,%s, %s, %s,%s,%s,%s,%s);"%(tablename,index,NomeTest,data,Articolo,Nodo,DescrizIngresso,BitQuant,NumeroCiclo,Banda,Fc,NumeroCampioni,Errori,jdata))
        #                               1                   2                 3             4                     5                      6                             7             8           9      10     11                  12            13                1   2    3   4   5   6  7  8   9   10 11 1213      1      2   3       4     5       6    7                 8        9          10   11   12              13  14     (unO IN PIU PER TABELLA NOME)
        print(self.sql)
        self.cursor.execute(self.sql)
        self.conn.commit()
        # your code
        elapsed_time = time.time() - start_time
        print("Fatta scrittura in ",elapsed_time)
        return A
        '''
        def TestParameterWr(Dati=[0,1,2,3]):
        RowDatiDb = {
                    "Dati": []
                    }
        Dati_dict = json.dumps(RowDatiDb)
        Testdata= json.loads(Dati_dict)
        i=0
        while(i<len(Dati)):
            Testdata["Dati"].append(Dati[i])
            i=i+1

    with open(filename, 'w') as filejson:
        json.dump(Testdata, filejson)
        filejson.close()
        ###################################
        def TestParameterRdForDB(filename):
            with open(filename) as jsonFile:
            Testdata = json.load(jsonFile)
            jsonFile.close()
            print(" data is ",Testdata)
        return Testdata
        '''
    def InsertJsonInTable(self,tablename,Dati,A2DName,ciclo):
        RowDatiDb = {
                    "Dati": []
                    }
        Dati_dict = json.dumps(RowDatiDb)
        Testdata= json.loads(Dati_dict)
        i=0
        while(i<len(Dati)):
            Testdata["Dati"].append(Dati[i])
            i=i+1
        index=1
        k=3
        A=Testdata["Dati"]
        print("Numero di Dati is",len(A))
        i=0
        STRARR=""
        while(i<len(A)):
            STRARR=STRARR+("%2f4,"%A[i])
            i=i+1
        print("Added finish")
        start_time = time.time()
        self.sql = ("INSERT INTO %s VALUES ('%s','%s','%s');"%(tablename,ciclo,A2DName,STRARR))
        #########self.sql=("INSERT INTO %s VALUES (id,NomeTest CHAR(16),date CHAR(16),NomeArticolo CHAR(16),NomeRaspberry CHAR(16),DescrizioneIngresso CHAR(16),NumeroBit INT,TestNr INT ,Banda INT,Fc INT,NumeroCampioni INT,ERRORI CHAR(16),Wave jsonb) VALUES (%s , %s ,%s, %s, %s, %s,%s, %s, %s,%s,%s,%s,%s);"%(tablename,index,NomeTest,data,Articolo,Nodo,DescrizIngresso,BitQuant,NumeroCiclo,Banda,Fc,NumeroCampioni,Errori,jdata))
        #                               1                   2                 3             4                     5                      6                             7             8           9      10     11                  12            13                1   2    3   4   5   6  7  8   9   10 11 1213      1      2   3       4     5       6    7                 8        9          10   11   12              13  14     (unO IN PIU PER TABELLA NOME)
        #print(self.sql)
        self.cursor.execute(self.sql)
        self.conn.commit()
        # your code
        elapsed_time = time.time() - start_time
        print("Fatta scrittura in ",elapsed_time)
    
    '''leggo i dati tutti'''

    def DeleteJsonRawInTable(self,tablename,ciclo,ColonValue):
        #self.sql=("DELETE from %s WHERE %s in(%s);"%(tablename,ColonValue,ciclo))
        self.sql=("DELETE from %s WHERE %s in(%s);"%(tablename,ciclo,ColonValue))
        print(self.sql)
        self.cursor.execute(self.sql) #NON USO IL COMANDO:::: NON CANCELLO
        self.conn.commit()
     
    def GetAllFromtable(self,TableName):
        #Creating a cursor object using the cursor() method
        self.sql=("SELECT * from %s ;"%TableName)
        #Retrieving data
        print(self.sql)
        self.cursor.execute(self.sql)
        #Fetching 1st row from the table
        result = self.cursor.fetchall();
        if(len(result)<1):
            print("Tabella Vuota")
            return 0
        else:
            R=[]
            i=0
            for row in result:
                print(row)
                print("==============================================")
                R.append(row)
                i=i+1
        return R

   
    ''' leggo tutti i file.-... uso questa non quella sopra '''
    def GetAllFromtable(self,TableName):
        #Creating a cursor object using the cursor() method
        self.sql=("SELECT * from %s ;"%TableName)
        print(self.sql)
        self.cursor.execute(self.sql)
        #Fetching 1st row from the table
        result = self.cursor.fetchall();
        print("=====>",result)
        #rows = cur.fetchall()
        Res=[]
        for row in result:
            print(row)
            Res=[]
            try:
                a=row.replace("(","")
                b=a.replace(")","")
                Da=b.split(",")
                for ff in Da:
                    Res.append(int(ff))
            except:
                print("finito con errore")
            print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
            print(Res)
        #print(result)
        return result
    ''' prendo la prima riga...'''
    def GetOneFromtable(self,TableName):
        #Setting auto commit false
        #Creating a cursor object using the cursor() method
        self.sql="SELECT * from %s;"%TableName
        #Retrieving data
        self.cursor.execute(self.sql)
        #Fetching 1st row from the table
        result = self.cursor.fetchone();
        print(result)
        return result

    


    def DeleteData(self,Data,Soglia):
        pass
        #cursor.execute('''DELETE FROM EMPLOYEE WHERE AGE > 25''')
     
    
    '''
    questa funzione legge dal db ed eventulmente plotta il file.
    '''
    def ReadTable(self,Tabname):
        self.cursor.execute('SELECT * FROM %s ;'%Tabname)
        AAAA=self.cursor.fetchall()
        print(" DB is  %s Lunghezza frame is%d " %(Tabname,len(AAAA)))
        i=0
        Res=[]
        cicli=[]
        A2DName=[]
        #attenzione devo distinguere sul tipo di tabella
        # se è tabella coon i risultati ....
        while(i<len(AAAA)):
            print(len(AAAA[i]))
            if(len(AAAA[i])<4):
                A2DName.append(AAAA[i][1])
                cicli.append(AAAA[i][0])
                Rch=AAAA[i][2].split(",")
                j=0
                AOUT=[]
                while(j<(len(Rch)-1)):
                    try:
                        AOUT.append(float(Rch[j]))
                    except:
                        print("ERRORE ALL INDICE",j)  
                    j=j+1
                print("Len is",len(Rch))
                Res.append(AOUT)
                #while(k<len(Rch)):
                #plt.plot(Rch)
                #plt.show()
            else:
                print("====>",AAAA[i])
                # print("----",AAAA[i])
                #AOUT.append(AAAA[i][3])
                Res.append("bo")
            i=i+1
                
        return Res ,cicli,A2DName
    
        
    def FillArray(self,Arr):
        i=0
        Save="["
        while(i<(len(Arr)-1)):
            Save=Save+"(%s),"%(Arr[i])
            i=i+1
        Save=Save+",%s)]"%(Arr[i])
        print(Save)
        self.cursor.executemany("INSERT INTO person VALUES (%s)",Save)
        self.conn.commit()
        # you must call commit() to persist your data if you don't set autocommit to True
        

def main_ref():
    Del=True   
    D=db(server="10.16.0.197",database="TestDB")
    if(Del==True):
        D.DeleteAllTable()
    D.TableNameis()
    D.MakeConfigTable("CONFIG123")
    D.WriteConfigTableRaw(NextTable="CONFIG123",NomeTest="Mio" ,NomeMacchina="Bo" ,IpMacchina="69.69.69.69",NomeArticolo="cazz0" ,Dataeora="1" ,Errori=0,StartIndex=0,StopIndex=1000 ,DurataAcq=10 ,FreqDiCamp=15000 ,Periododiacquisizione=1000 ,NomeA2D01="NULL" ,NomeA2D11="NULL",NomeA2D21="NULL",NomeA2D31="NULL",NomeA2D41="NULL",NomeA2D51="NULL",NomeA2D61="NULL",NomeA2D71="NULL",NomeA2D81="NULL",NomeA2D91="NULL",NomeA2DA1="NULL" ,NomeA2DB1="NULL",NomeA2DC1="NULL",NomeA2DD1="NULL",NomeA2DE1="NULL",NomeA2DF="NULL",NomeA2D02="NULL",NomeA2D12="NULL",NomeA2D22="NULL",NomeA2D32="NULL",NomeA2D42="NULL",NomeA2D52="NULL",NomeA2D62="NULL",NomeA2D72="NULL",NomeA2D82="NULL",NomeA2D92="NULL",NomeA2DA2="NULL",NomeA2DB2="NULL",NomeA2DC2="NULL",NomeA2DD2="NULL",NomeA2DE2="NULL",NomeA2DF2="NULL",NomeA2D03="NULL",NomeA2D13="NULL",NomeA2D23="NULL",NomeA2D33="NULL",NomeA2D43="NULL",NomeA2D53="NULL",NomeA2D63="NULL",NomeA2D73="NULL",NomeA2D83="NULL",NomeA2D93="NULL",NomeA2DA3="NULL",NomeA2DB3="NULL",NomeA2DC3="NULL",NomeA2DD3="NULL",NomeA2DE3="NULL",NomeA2DF3="NULL",ciclitracontrollo=1000,ciclitraAcquisizione =100,ciclitotali=1000 ,numerosemicilci=5 ,pausa=1 ,sel=0 ,f=0  ,AMax =1,VMax=2 ,A0=3  ,SMax=4 )
    D.ReadConfigTableRaw("CONFIG123")
    D.DeleteConfigTableRaw("CONFIG123","ciclitracontrollo",1000)
    D.ReadConfigTableRaw("CONFIG123")
    #DS=db(server="10.16.0.197",database="AS000861")
    DS=db(server="10.16.0.197",database="TestDB")
    DS.TableNameis()
    
    DS.GetDB()
    DS.TableNameis()
    TableName="LabTTTTTA"
    DS.MakeRefTable(TableName)
    NameTabella=DS.InsertDataInRefTable(TableName=TableName,NomeTest="Test1",Dataeora="111",Articolo="ART1",NomeRaspberry="RA1",NumeroBit=16,Banda=4000,FreqquenzaCampionamento=16000,TestNr=1)
    DS.MakeJsonTable(NameTabella)
    filename=plotfi.findjsonfile('PrimoTestG*.json','/home/novello/lab/DB/TEST') # mi ritorna la lista dei file json
    print(len(filename))
    print(NameTabella)
    i=0
    while(i<len(filename)):
        time.sleep(1)
        PathName='/home/novello/lab/DB/TEST/'+filename[i]
        DS.InsertJsonRawInTable(NameTabella,PathName,"CIAO",(1000+i))
        time.sleep(1)
        print(i)
        i=i+1
    #D.GetOneFromtable(NameTabella)
    r,ciclo,A2D=DS.ReadTable(NameTabella)
    DS.DeleteJsonRawInTable(NameTabella,"idt",1001)
    print("")
    k=0
    while(k<len(r)):
        print(r[k])
        plt.plot(r[k])
        plt.show()
        k=k+1

    #D.GetAllFromtable(NameTabella)
    print("FIN")
    return 


import os
import unittest
class DBTestCase(unittest.TestCase):
    
    def setUp(self):
        self.DB =db(server="10.16.0.197",database="TestDB")
        self.DB.DeleteAllTable()

    def test_param(self):
        print("test_param ... Make configuration file\n")
        self.assertEqual(self.DB.MakeConfigTable("CONFIG123"), None)

    def test_WriteParam(self):
        print("test_WriteParam ")
        self.assertEqual(self.DB.MakeConfigTable("CONFIG123"), None)
        self.DB.WriteConfigTableRaw(NextTable="CONFIG123",NomeTest="Mio" ,NomeMacchina="Bo" ,IpMacchina="69.69.69.69",NomeArticolo="cazz0" ,Dataeora="1" ,Errori=0,StartIndex=0,StopIndex=1000 ,DurataAcq=10 ,FreqDiCamp=15000 ,Periododiacquisizione=1000 ,NomeA2D01="NULL" ,NomeA2D11="NULL",NomeA2D21="NULL",NomeA2D31="NULL",NomeA2D41="NULL",NomeA2D51="NULL",NomeA2D61="NULL",NomeA2D71="NULL",NomeA2D81="NULL",NomeA2D91="NULL",NomeA2DA1="NULL" ,NomeA2DB1="NULL",NomeA2DC1="NULL",NomeA2DD1="NULL",NomeA2DE1="NULL",NomeA2DF="NULL",NomeA2D02="NULL",NomeA2D12="NULL",NomeA2D22="NULL",NomeA2D32="NULL",NomeA2D42="NULL",NomeA2D52="NULL",NomeA2D62="NULL",NomeA2D72="NULL",NomeA2D82="NULL",NomeA2D92="NULL",NomeA2DA2="NULL",NomeA2DB2="NULL",NomeA2DC2="NULL",NomeA2DD2="NULL",NomeA2DE2="NULL",NomeA2DF2="NULL",NomeA2D03="NULL",NomeA2D13="NULL",NomeA2D23="NULL",NomeA2D33="NULL",NomeA2D43="NULL",NomeA2D53="NULL",NomeA2D63="NULL",NomeA2D73="NULL",NomeA2D83="NULL",NomeA2D93="NULL",NomeA2DA3="NULL",NomeA2DB3="NULL",NomeA2DC3="NULL",NomeA2DD3="NULL",NomeA2DE3="NULL",NomeA2DF3="NULL",ciclitracontrollo=1000,ciclitraAcquisizione =100,ciclitotali=1000 ,numerosemicilci=5 ,pausa=1 ,sel=0 ,f=0  ,AMax =1,VMax=2 ,A0=3  ,SMax=4 )
        R,D=self.DB.ReadConfigTableRaw("CONFIG123")
        self.assertEqual(len(R), 1)
        print("Read data is ",R)
    def test_WriteParam2(self):
        print("test_WriteParam ")
        self.assertEqual(self.DB.MakeConfigTable("CONFIG123"), None)
        self.DB.WriteConfigTableRaw(NextTable="CONFIG123",NomeTest="Mio" ,NomeMacchina="Bo" ,IpMacchina="69.69.69.69",NomeArticolo="cazz0" ,Dataeora="1" ,Errori=0,StartIndex=0,StopIndex=1000 ,DurataAcq=10 ,FreqDiCamp=15000 ,Periododiacquisizione=1000 ,NomeA2D01="NULL" ,NomeA2D11="NULL",NomeA2D21="NULL",NomeA2D31="NULL",NomeA2D41="NULL",NomeA2D51="NULL",NomeA2D61="NULL",NomeA2D71="NULL",NomeA2D81="NULL",NomeA2D91="NULL",NomeA2DA1="NULL" ,NomeA2DB1="NULL",NomeA2DC1="NULL",NomeA2DD1="NULL",NomeA2DE1="NULL",NomeA2DF="NULL",NomeA2D02="NULL",NomeA2D12="NULL",NomeA2D22="NULL",NomeA2D32="NULL",NomeA2D42="NULL",NomeA2D52="NULL",NomeA2D62="NULL",NomeA2D72="NULL",NomeA2D82="NULL",NomeA2D92="NULL",NomeA2DA2="NULL",NomeA2DB2="NULL",NomeA2DC2="NULL",NomeA2DD2="NULL",NomeA2DE2="NULL",NomeA2DF2="NULL",NomeA2D03="NULL",NomeA2D13="NULL",NomeA2D23="NULL",NomeA2D33="NULL",NomeA2D43="NULL",NomeA2D53="NULL",NomeA2D63="NULL",NomeA2D73="NULL",NomeA2D83="NULL",NomeA2D93="NULL",NomeA2DA3="NULL",NomeA2DB3="NULL",NomeA2DC3="NULL",NomeA2DD3="NULL",NomeA2DE3="NULL",NomeA2DF3="NULL",ciclitracontrollo=1000,ciclitraAcquisizione =100,ciclitotali=1000 ,numerosemicilci=5 ,pausa=1 ,sel=0 ,f=0  ,AMax =1,VMax=2 ,A0=3  ,SMax=4 )
        self.DB.WriteConfigTableRaw(NextTable="CONFIG123",NomeTest="Mio" ,NomeMacchina="Bo" ,IpMacchina="69.69.69.69",NomeArticolo="cazz1" ,Dataeora="1" ,Errori=0,StartIndex=0,StopIndex=1000 ,DurataAcq=10 ,FreqDiCamp=15000 ,Periododiacquisizione=1000 ,NomeA2D01="NULL" ,NomeA2D11="NULL",NomeA2D21="NULL",NomeA2D31="NULL",NomeA2D41="NULL",NomeA2D51="NULL",NomeA2D61="NULL",NomeA2D71="NULL",NomeA2D81="NULL",NomeA2D91="NULL",NomeA2DA1="NULL" ,NomeA2DB1="NULL",NomeA2DC1="NULL",NomeA2DD1="NULL",NomeA2DE1="NULL",NomeA2DF="NULL",NomeA2D02="NULL",NomeA2D12="NULL",NomeA2D22="NULL",NomeA2D32="NULL",NomeA2D42="NULL",NomeA2D52="NULL",NomeA2D62="NULL",NomeA2D72="NULL",NomeA2D82="NULL",NomeA2D92="NULL",NomeA2DA2="NULL",NomeA2DB2="NULL",NomeA2DC2="NULL",NomeA2DD2="NULL",NomeA2DE2="NULL",NomeA2DF2="NULL",NomeA2D03="NULL",NomeA2D13="NULL",NomeA2D23="NULL",NomeA2D33="NULL",NomeA2D43="NULL",NomeA2D53="NULL",NomeA2D63="NULL",NomeA2D73="NULL",NomeA2D83="NULL",NomeA2D93="NULL",NomeA2DA3="NULL",NomeA2DB3="NULL",NomeA2DC3="NULL",NomeA2DD3="NULL",NomeA2DE3="NULL",NomeA2DF3="NULL",ciclitracontrollo=1001,ciclitraAcquisizione =100,ciclitotali=1000 ,numerosemicilci=5 ,pausa=1 ,sel=0 ,f=0  ,AMax =1,VMax=2 ,A0=3  ,SMax=4 )
        #self.DB.DeleteConfigTableRaw("CONFIG123","NomeArticolo","cazz1")
        self.DB.DeleteConfigTableRaw("CONFIG123","ciclitracontrollo",1000)
        R,D=self.DB.ReadConfigTableRaw("CONFIG123")
        self.assertEqual(len(R), 1)
        print("Read data is ",R)
        self.DB.DeleteConfigTableRaw("CONFIG123","ciclitracontrollo",1001)
        R,D=self.DB.ReadConfigTableRaw("CONFIG123")
        print("Read data is ",R)
        self.assertEqual(R, 0)
    def test_WriteParam3(self):
        print("test_WriteParam ")
        self.assertEqual(self.DB.MakeConfigTable("CONFIG123"), None)
        self.DB.WriteConfigTableRaw(NextTable="CONFIG123",NomeTest="Mio" ,NomeMacchina="Bo" ,IpMacchina="69.69.69.69",NomeArticolo="cazz0" ,Dataeora="1" ,Errori=0,StartIndex=0,StopIndex=1000 ,DurataAcq=10 ,FreqDiCamp=15000 ,Periododiacquisizione=1000 ,NomeA2D01="NULL" ,NomeA2D11="NULL",NomeA2D21="NULL",NomeA2D31="NULL",NomeA2D41="NULL",NomeA2D51="NULL",NomeA2D61="NULL",NomeA2D71="NULL",NomeA2D81="NULL",NomeA2D91="NULL",NomeA2DA1="NULL" ,NomeA2DB1="NULL",NomeA2DC1="NULL",NomeA2DD1="NULL",NomeA2DE1="NULL",NomeA2DF="NULL",NomeA2D02="NULL",NomeA2D12="NULL",NomeA2D22="NULL",NomeA2D32="NULL",NomeA2D42="NULL",NomeA2D52="NULL",NomeA2D62="NULL",NomeA2D72="NULL",NomeA2D82="NULL",NomeA2D92="NULL",NomeA2DA2="NULL",NomeA2DB2="NULL",NomeA2DC2="NULL",NomeA2DD2="NULL",NomeA2DE2="NULL",NomeA2DF2="NULL",NomeA2D03="NULL",NomeA2D13="NULL",NomeA2D23="NULL",NomeA2D33="NULL",NomeA2D43="NULL",NomeA2D53="NULL",NomeA2D63="NULL",NomeA2D73="NULL",NomeA2D83="NULL",NomeA2D93="NULL",NomeA2DA3="NULL",NomeA2DB3="NULL",NomeA2DC3="NULL",NomeA2DD3="NULL",NomeA2DE3="NULL",NomeA2DF3="NULL",ciclitracontrollo=1000,ciclitraAcquisizione =100,ciclitotali=1000 ,numerosemicilci=5 ,pausa=1 ,sel=0 ,f=0  ,AMax =1,VMax=2 ,A0=3  ,SMax=4 )
        self.DB.WriteConfigTableRaw(NextTable="CONFIG123",NomeTest="Mio" ,NomeMacchina="Bo" ,IpMacchina="69.69.69.69",NomeArticolo="cazz1" ,Dataeora="1" ,Errori=0,StartIndex=0,StopIndex=1000 ,DurataAcq=10 ,FreqDiCamp=15000 ,Periododiacquisizione=1000 ,NomeA2D01="NULL" ,NomeA2D11="NULL",NomeA2D21="NULL",NomeA2D31="NULL",NomeA2D41="NULL",NomeA2D51="NULL",NomeA2D61="NULL",NomeA2D71="NULL",NomeA2D81="NULL",NomeA2D91="NULL",NomeA2DA1="NULL" ,NomeA2DB1="NULL",NomeA2DC1="NULL",NomeA2DD1="NULL",NomeA2DE1="NULL",NomeA2DF="NULL",NomeA2D02="NULL",NomeA2D12="NULL",NomeA2D22="NULL",NomeA2D32="NULL",NomeA2D42="NULL",NomeA2D52="NULL",NomeA2D62="NULL",NomeA2D72="NULL",NomeA2D82="NULL",NomeA2D92="NULL",NomeA2DA2="NULL",NomeA2DB2="NULL",NomeA2DC2="NULL",NomeA2DD2="NULL",NomeA2DE2="NULL",NomeA2DF2="NULL",NomeA2D03="NULL",NomeA2D13="NULL",NomeA2D23="NULL",NomeA2D33="NULL",NomeA2D43="NULL",NomeA2D53="NULL",NomeA2D63="NULL",NomeA2D73="NULL",NomeA2D83="NULL",NomeA2D93="NULL",NomeA2DA3="NULL",NomeA2DB3="NULL",NomeA2DC3="NULL",NomeA2DD3="NULL",NomeA2DE3="NULL",NomeA2DF3="NULL",ciclitracontrollo=1001,ciclitraAcquisizione =100,ciclitotali=1000 ,numerosemicilci=5 ,pausa=1 ,sel=0 ,f=0  ,AMax =1,VMax=2 ,A0=3  ,SMax=4 )
        #self.DB.DeleteConfigTableRaw("CONFIG123","NomeArticolo","cazz1")
        self.DB.DeleteConfigTableRaw("CONFIG123","ciclitracontrollo",1000)
        R,D=self.DB.ReadConfigTableRaw("CONFIG123")
        self.assertEqual(len(R), 1)
        print("Read data is ",R)
        self.DB.DeleteConfigTableRaw("CONFIG123","NomeMacchina","'Bo                                                              '")
        R,D=self.DB.ReadConfigTableRaw("CONFIG123")
        print("Read data is ",R)
        self.assertEqual(R, 0)
    def test_WriteParam4(self):
        print("test_WriteParam ")
        self.assertEqual(self.DB.MakeConfigTable("CONFIG123"), None)
        self.DB.WriteConfigTableRaw(NextTable="CONFIG123",NomeTest="Mio" ,NomeMacchina="Bo" ,IpMacchina="69.69.69.69",NomeArticolo="cazz0" ,Dataeora="1" ,Errori=0,StartIndex=0,StopIndex=1000 ,DurataAcq=10 ,FreqDiCamp=15000 ,Periododiacquisizione=1000 ,NomeA2D01="NULL" ,NomeA2D11="NULL",NomeA2D21="NULL",NomeA2D31="NULL",NomeA2D41="NULL",NomeA2D51="NULL",NomeA2D61="NULL",NomeA2D71="NULL",NomeA2D81="NULL",NomeA2D91="NULL",NomeA2DA1="NULL" ,NomeA2DB1="NULL",NomeA2DC1="NULL",NomeA2DD1="NULL",NomeA2DE1="NULL",NomeA2DF="NULL",NomeA2D02="NULL",NomeA2D12="NULL",NomeA2D22="NULL",NomeA2D32="NULL",NomeA2D42="NULL",NomeA2D52="NULL",NomeA2D62="NULL",NomeA2D72="NULL",NomeA2D82="NULL",NomeA2D92="NULL",NomeA2DA2="NULL",NomeA2DB2="NULL",NomeA2DC2="NULL",NomeA2DD2="NULL",NomeA2DE2="NULL",NomeA2DF2="NULL",NomeA2D03="NULL",NomeA2D13="NULL",NomeA2D23="NULL",NomeA2D33="NULL",NomeA2D43="NULL",NomeA2D53="NULL",NomeA2D63="NULL",NomeA2D73="NULL",NomeA2D83="NULL",NomeA2D93="NULL",NomeA2DA3="NULL",NomeA2DB3="NULL",NomeA2DC3="NULL",NomeA2DD3="NULL",NomeA2DE3="NULL",NomeA2DF3="NULL",ciclitracontrollo=1000,ciclitraAcquisizione =100,ciclitotali=1000 ,numerosemicilci=5 ,pausa=1 ,sel=0 ,f=0  ,AMax =1,VMax=2 ,A0=3  ,SMax=4 )
        R,D=self.DB.ReadConfigTableRaw("CONFIG123")
        self.assertEqual(len(R), 1)
        print("Read data is ",R)
        TableName="LabTTTTTA"
        self.DB.MakeRefTable(TableName)
        NameTabella=self.DB.InsertDataInRefTable(TableName=TableName,NomeTest="Test1",Dataeora="111",Articolo="ART1",NomeRaspberry="RA1",NumeroBit=16,Banda=4000,FreqquenzaCampionamento=16000,TestNr=1)
        self.DB.MakeJsonTable(NameTabella)
        print(NameTabella)
    def test_WriteParam5(self):
        print("test_WriteParam ")
        self.assertEqual(self.DB.MakeConfigTable("CONFIG123"), None)
        self.DB.WriteConfigTableRaw(NextTable="CONFIG123",NomeTest="Mio" ,NomeMacchina="Bo" ,IpMacchina="69.69.69.69",NomeArticolo="cazz0" ,Dataeora="1" ,Errori=0,StartIndex=0,StopIndex=1000 ,DurataAcq=10 ,FreqDiCamp=15000 ,Periododiacquisizione=1000 ,NomeA2D01="NULL" ,NomeA2D11="NULL",NomeA2D21="NULL",NomeA2D31="NULL",NomeA2D41="NULL",NomeA2D51="NULL",NomeA2D61="NULL",NomeA2D71="NULL",NomeA2D81="NULL",NomeA2D91="NULL",NomeA2DA1="NULL" ,NomeA2DB1="NULL",NomeA2DC1="NULL",NomeA2DD1="NULL",NomeA2DE1="NULL",NomeA2DF="NULL",NomeA2D02="NULL",NomeA2D12="NULL",NomeA2D22="NULL",NomeA2D32="NULL",NomeA2D42="NULL",NomeA2D52="NULL",NomeA2D62="NULL",NomeA2D72="NULL",NomeA2D82="NULL",NomeA2D92="NULL",NomeA2DA2="NULL",NomeA2DB2="NULL",NomeA2DC2="NULL",NomeA2DD2="NULL",NomeA2DE2="NULL",NomeA2DF2="NULL",NomeA2D03="NULL",NomeA2D13="NULL",NomeA2D23="NULL",NomeA2D33="NULL",NomeA2D43="NULL",NomeA2D53="NULL",NomeA2D63="NULL",NomeA2D73="NULL",NomeA2D83="NULL",NomeA2D93="NULL",NomeA2DA3="NULL",NomeA2DB3="NULL",NomeA2DC3="NULL",NomeA2DD3="NULL",NomeA2DE3="NULL",NomeA2DF3="NULL",ciclitracontrollo=1000,ciclitraAcquisizione =100,ciclitotali=1000 ,numerosemicilci=5 ,pausa=1 ,sel=0 ,f=0  ,AMax =1,VMax=2 ,A0=3  ,SMax=4 )
        R,D=self.DB.ReadConfigTableRaw("CONFIG123")
        self.assertEqual(len(R), 1)
        print("Read data is ",R)
        TableName="LabTTTTTA"
        self.DB.MakeRefTable(TableName)
        NameTabella=self.DB.InsertDataInRefTable(TableName=TableName,NomeTest="Test1",Dataeora="111",Articolo="ART1",NomeRaspberry="RA1",NumeroBit=16,Banda=4000,FreqquenzaCampionamento=16000,TestNr=1)
        self.DB.MakeJsonTable(NameTabella)
        self.DB.MakeJsonTable(NameTabella)
        filename=plotfi.findjsonfile('PrimoTestG*.json','/home/novello/lab/DB/TEST') # mi ritorna la lista dei file json
        print(len(filename))
        print(NameTabella)
        i=0
        while(i<len(filename)):
            time.sleep(1)
            PathName='/home/novello/lab/DB/TEST/'+filename[i]
            self.DB.InsertJsonRawInTable(NameTabella,PathName,"CIAO",(1000+i))
            time.sleep(1)
            print(i)
            i=i+1
        print(NameTabella)
        print(i)
        self.assertEqual(i, 10)
    def test_WriteParam6(self):
        print("test_WriteParam ")
        self.assertEqual(self.DB.MakeConfigTable("CONFIG123"), None)
        self.DB.WriteConfigTableRaw(NextTable="CONFIG123",NomeTest="Mio" ,NomeMacchina="Bo" ,IpMacchina="69.69.69.69",NomeArticolo="cazz0" ,Dataeora="1" ,Errori=0,StartIndex=0,StopIndex=1000 ,DurataAcq=10 ,FreqDiCamp=15000 ,Periododiacquisizione=1000 ,NomeA2D01="NULL" ,NomeA2D11="NULL",NomeA2D21="NULL",NomeA2D31="NULL",NomeA2D41="NULL",NomeA2D51="NULL",NomeA2D61="NULL",NomeA2D71="NULL",NomeA2D81="NULL",NomeA2D91="NULL",NomeA2DA1="NULL" ,NomeA2DB1="NULL",NomeA2DC1="NULL",NomeA2DD1="NULL",NomeA2DE1="NULL",NomeA2DF="NULL",NomeA2D02="NULL",NomeA2D12="NULL",NomeA2D22="NULL",NomeA2D32="NULL",NomeA2D42="NULL",NomeA2D52="NULL",NomeA2D62="NULL",NomeA2D72="NULL",NomeA2D82="NULL",NomeA2D92="NULL",NomeA2DA2="NULL",NomeA2DB2="NULL",NomeA2DC2="NULL",NomeA2DD2="NULL",NomeA2DE2="NULL",NomeA2DF2="NULL",NomeA2D03="NULL",NomeA2D13="NULL",NomeA2D23="NULL",NomeA2D33="NULL",NomeA2D43="NULL",NomeA2D53="NULL",NomeA2D63="NULL",NomeA2D73="NULL",NomeA2D83="NULL",NomeA2D93="NULL",NomeA2DA3="NULL",NomeA2DB3="NULL",NomeA2DC3="NULL",NomeA2DD3="NULL",NomeA2DE3="NULL",NomeA2DF3="NULL",ciclitracontrollo=1000,ciclitraAcquisizione =100,ciclitotali=1000 ,numerosemicilci=5 ,pausa=1 ,sel=0 ,f=0  ,AMax =1,VMax=2 ,A0=3  ,SMax=4 )
        R,D=self.DB.ReadConfigTableRaw("CONFIG123")
        self.assertEqual(len(R), 1)
        print("Read data is ",R)
        TableName="LabTTTTTA"
        self.DB.MakeRefTable(TableName)
        NameTabella=self.DB.InsertDataInRefTable(TableName=TableName,NomeTest="Test1",Dataeora="111",Articolo="ART1",NomeRaspberry="RA1",NumeroBit=16,Banda=4000,FreqquenzaCampionamento=16000,TestNr=1)
        self.DB.MakeJsonTable(NameTabella)
        self.DB.MakeJsonTable(NameTabella)
        filename=plotfi.findjsonfile('PrimoTestG*.json','/home/novello/lab/DB/TEST') # mi ritorna la lista dei file json
        print(len(filename))
        print(NameTabella)
        i=0
        while(i<len(filename)):
            time.sleep(1)
            PathName='/home/novello/lab/DB/TEST/'+filename[i]
            self.DB.InsertJsonRawInTable(NameTabella,PathName,"CIAO",(1000+i))
            time.sleep(1)
            print(i)
            i=i+1
        print(NameTabella)
        print(i)
        r,ciclo,A2D=self.DB.ReadTable(NameTabella)
        print(r)
        print(ciclo)
        print(A2D)
        self.assertEqual(i, 10)
    
    def test_WriteParam7(self):
        print("test_WriteParam ")
        self.assertEqual(self.DB.MakeConfigTable("CONFIG123"), None)
        self.DB.WriteConfigTableRaw(NextTable="CONFIG123",NomeTest="Mio" ,NomeMacchina="Bo" ,IpMacchina="69.69.69.69",NomeArticolo="cazz0" ,Dataeora="1" ,Errori=0,StartIndex=0,StopIndex=1000 ,DurataAcq=10 ,FreqDiCamp=15000 ,Periododiacquisizione=1000 ,NomeA2D01="NULL" ,NomeA2D11="NULL",NomeA2D21="NULL",NomeA2D31="NULL",NomeA2D41="NULL",NomeA2D51="NULL",NomeA2D61="NULL",NomeA2D71="NULL",NomeA2D81="NULL",NomeA2D91="NULL",NomeA2DA1="NULL" ,NomeA2DB1="NULL",NomeA2DC1="NULL",NomeA2DD1="NULL",NomeA2DE1="NULL",NomeA2DF="NULL",NomeA2D02="NULL",NomeA2D12="NULL",NomeA2D22="NULL",NomeA2D32="NULL",NomeA2D42="NULL",NomeA2D52="NULL",NomeA2D62="NULL",NomeA2D72="NULL",NomeA2D82="NULL",NomeA2D92="NULL",NomeA2DA2="NULL",NomeA2DB2="NULL",NomeA2DC2="NULL",NomeA2DD2="NULL",NomeA2DE2="NULL",NomeA2DF2="NULL",NomeA2D03="NULL",NomeA2D13="NULL",NomeA2D23="NULL",NomeA2D33="NULL",NomeA2D43="NULL",NomeA2D53="NULL",NomeA2D63="NULL",NomeA2D73="NULL",NomeA2D83="NULL",NomeA2D93="NULL",NomeA2DA3="NULL",NomeA2DB3="NULL",NomeA2DC3="NULL",NomeA2DD3="NULL",NomeA2DE3="NULL",NomeA2DF3="NULL",ciclitracontrollo=1000,ciclitraAcquisizione =100,ciclitotali=1000 ,numerosemicilci=5 ,pausa=1 ,sel=0 ,f=0  ,AMax =1,VMax=2 ,A0=3  ,SMax=4 )
        R,D=self.DB.ReadConfigTableRaw("CONFIG123")
        self.assertEqual(len(R), 1)
        print("Read data is ",R)
        TableName="LabTTTTTA"
        self.DB.MakeRefTable(TableName)
        NameTabella=self.DB.InsertDataInRefTable(TableName=TableName,NomeTest="Test1",Dataeora="111",Articolo="ART1",NomeRaspberry="RA1",NumeroBit=16,Banda=4000,FreqquenzaCampionamento=16000,TestNr=1)
        self.DB.MakeJsonTable(NameTabella)
        self.DB.MakeJsonTable(NameTabella)
        filename=plotfi.findjsonfile('PrimoTestG*.json','/home/novello/lab/DB/TEST') # mi ritorna la lista dei file json
        print(len(filename))
        print(NameTabella)
        i=0
        while(i<1):
            time.sleep(1)
            PathName='/home/novello/lab/DB/TEST/'+filename[i]
            D=self.DB.InsertJsonRawInTable(NameTabella,PathName,"CIAO",(1000+i))
            self.DB.InsertJsonInTable(NameTabella,D,"CIAO",(2000+i))
            time.sleep(1)
            print(i)
            i=i+1
        print(NameTabella)
        print(i)
        j=0
        r,ciclo,A2D=self.DB.ReadTable(NameTabella)
        while(j<len(r[0])):
            self.assertEqual(r[0][j], r[1][j])
            j=j+1

        print(r)
        print(ciclo)
        print(A2D)

        self.assertEqual(i, 1)

    def test_WriteParam8(self):
        print("test_WriteParam8 ")
        self.assertEqual(self.DB.MakeConfigTable("CONFIG123"), None)
        self.DB.WriteConfigTableRaw(NextTable="CONFIG123",NomeTest="Mio" ,NomeMacchina="Bo" ,IpMacchina="69.69.69.69",NomeArticolo="cazz0" ,Dataeora="1" ,Errori=0,StartIndex=0,StopIndex=1000 ,DurataAcq=10 ,FreqDiCamp=15000 ,Periododiacquisizione=1000 ,NomeA2D01="NULL" ,NomeA2D11="NULL",NomeA2D21="NULL",NomeA2D31="NULL",NomeA2D41="NULL",NomeA2D51="NULL",NomeA2D61="NULL",NomeA2D71="NULL",NomeA2D81="NULL",NomeA2D91="NULL",NomeA2DA1="NULL" ,NomeA2DB1="NULL",NomeA2DC1="NULL",NomeA2DD1="NULL",NomeA2DE1="NULL",NomeA2DF="NULL",NomeA2D02="NULL",NomeA2D12="NULL",NomeA2D22="NULL",NomeA2D32="NULL",NomeA2D42="NULL",NomeA2D52="NULL",NomeA2D62="NULL",NomeA2D72="NULL",NomeA2D82="NULL",NomeA2D92="NULL",NomeA2DA2="NULL",NomeA2DB2="NULL",NomeA2DC2="NULL",NomeA2DD2="NULL",NomeA2DE2="NULL",NomeA2DF2="NULL",NomeA2D03="NULL",NomeA2D13="NULL",NomeA2D23="NULL",NomeA2D33="NULL",NomeA2D43="NULL",NomeA2D53="NULL",NomeA2D63="NULL",NomeA2D73="NULL",NomeA2D83="NULL",NomeA2D93="NULL",NomeA2DA3="NULL",NomeA2DB3="NULL",NomeA2DC3="NULL",NomeA2DD3="NULL",NomeA2DE3="NULL",NomeA2DF3="NULL",ciclitracontrollo=1000,ciclitraAcquisizione =100,ciclitotali=1000 ,numerosemicilci=5 ,pausa=1 ,sel=0 ,f=0  ,AMax =1,VMax=2 ,A0=3  ,SMax=4 )
        R,D=self.DB.ReadConfigTableRaw("CONFIG123")
        self.assertEqual(len(R), 1)
        print("Read data is ",R)
        TableName="LabTTTTTA"
        self.DB.MakeRefTable(TableName)
        NameTabella=self.DB.InsertDataInRefTable(TableName=TableName,NomeTest="Test1",Dataeora="111",Articolo="ART1",NomeRaspberry="RA1",NumeroBit=16,Banda=4000,FreqquenzaCampionamento=16000,TestNr=1)
        self.DB.MakeJsonTable(NameTabella)
        self.DB.MakeJsonTable(NameTabella)
        filename=plotfi.findjsonfile('PrimoTestG*.json','/home/novello/lab/DB/TEST') # mi ritorna la lista dei file json
        print(len(filename))
        print(NameTabella)
        i=0
        while(i<len(filename)):
            time.sleep(1)
            PathName='/home/novello/lab/DB/TEST/'+filename[i]
            D=self.DB.InsertJsonRawInTable(NameTabella,PathName,"CIAO",(1000+i))
            self.DB.InsertJsonInTable(NameTabella,D,"CIAO",(2000+i))
            time.sleep(1)
            print(i)
            i=i+1
        print(NameTabella)
        print(i)
        j=0
        r,ciclo,A2D=self.DB.ReadTable(NameTabella)
        kk=0
        while(kk<(2*len(filename))):
            while(j<len(r[0])):
                self.assertEqual(r[kk][j], r[kk+1][j])
                j=j+1
            kk=kk+2
        print(r)
        print(ciclo)
        print(A2D)
    def test_WriteParam9(self):
        print("test_WriteParam9 ")
        self.assertEqual(self.DB.MakeConfigTable("CONFIG123"), None)
        self.DB.WriteConfigTableRaw(NextTable="CONFIG123",NomeTest="Mio" ,NomeMacchina="Bo" ,IpMacchina="69.69.69.69",NomeArticolo="cazz0" ,Dataeora="1" ,Errori=0,StartIndex=0,StopIndex=1000 ,DurataAcq=10 ,FreqDiCamp=15000 ,Periododiacquisizione=1000 ,NomeA2D01="NULL" ,NomeA2D11="NULL",NomeA2D21="NULL",NomeA2D31="NULL",NomeA2D41="NULL",NomeA2D51="NULL",NomeA2D61="NULL",NomeA2D71="NULL",NomeA2D81="NULL",NomeA2D91="NULL",NomeA2DA1="NULL" ,NomeA2DB1="NULL",NomeA2DC1="NULL",NomeA2DD1="NULL",NomeA2DE1="NULL",NomeA2DF="NULL",NomeA2D02="NULL",NomeA2D12="NULL",NomeA2D22="NULL",NomeA2D32="NULL",NomeA2D42="NULL",NomeA2D52="NULL",NomeA2D62="NULL",NomeA2D72="NULL",NomeA2D82="NULL",NomeA2D92="NULL",NomeA2DA2="NULL",NomeA2DB2="NULL",NomeA2DC2="NULL",NomeA2DD2="NULL",NomeA2DE2="NULL",NomeA2DF2="NULL",NomeA2D03="NULL",NomeA2D13="NULL",NomeA2D23="NULL",NomeA2D33="NULL",NomeA2D43="NULL",NomeA2D53="NULL",NomeA2D63="NULL",NomeA2D73="NULL",NomeA2D83="NULL",NomeA2D93="NULL",NomeA2DA3="NULL",NomeA2DB3="NULL",NomeA2DC3="NULL",NomeA2DD3="NULL",NomeA2DE3="NULL",NomeA2DF3="NULL",ciclitracontrollo=1000,ciclitraAcquisizione =100,ciclitotali=1000 ,numerosemicilci=5 ,pausa=1 ,sel=0 ,f=0  ,AMax =1,VMax=2 ,A0=3  ,SMax=4 )
        R,D=self.DB.ReadConfigTableRaw("CONFIG123")
        self.assertEqual(len(R), 1)
        print("Read data is ",R)
        TableName="LabTTTTTA"
        self.DB.MakeRefTable(TableName)
        NameTabella=self.DB.InsertDataInRefTable(TableName=TableName,NomeTest="Test1",Dataeora="111",Articolo="ART1",NomeRaspberry="RA1",NumeroBit=16,Banda=4000,FreqquenzaCampionamento=16000,TestNr=1)
        self.DB.MakeJsonTable(NameTabella)
        self.DB.MakeJsonTable(NameTabella)
        filename=plotfi.findjsonfile('PrimoTestG*.json','/home/novello/lab/DB/TEST') # mi ritorna la lista dei file json
        print(len(filename))
        print(NameTabella)
        i=0
        while(i<len(filename)):
            time.sleep(1)
            PathName='/home/novello/lab/DB/TEST/'+filename[i]
            D=self.DB.InsertJsonRawInTable(NameTabella,PathName,"CIAO",(1000+i))
            self.DB.InsertJsonInTable(NameTabella,D,"CIAO",(2000+i))
            time.sleep(1)
            print(i)
            i=i+1
        print(NameTabella)
        print(i)
        j=0
        r,ciclo,A2D=self.DB.ReadTable(NameTabella)
        kk=0
        while(kk<(2*len(filename))):
            while(j<len(r[0])):
                self.assertEqual(r[kk][j], r[kk+1][j])
                j=j+1
            kk=kk+2
        print(r)
        print(ciclo)
        print(A2D)

        self.assertEqual(i, 10)        
if __name__ == "__main__":
    unittest.main()
    #main_ref()


#if __name__ == '__main__':
#    main()
 
