#importiamo le librerie per il controllo dell'interfaccia GPIO
import RPi.GPIO as GPIO
import time
import Analogscan1
import Db7
import emailpy
import mod
import sys
def InteruptPIn():
   GPIO.setmode(GPIO.BCM)  
   # GPIO 23 set up as input. It is pulled up to stop false signals  
   GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)
   GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_UP) 
   GPIO.setup(25, GPIO.IN, pull_up_down=GPIO.PUD_UP) 
  
   try:  
      GPIO.wait_for_edge(23, GPIO.FALLING)  
      print( "\nFalling edge detected. Now your program can continue with")  
      print("whatever was waiting for a button press.")  
   except KeyboardInterrupt:  
      GPIO.cleanup()       # clean up GPIO on CTRL+C exit  
    
def main():
   try:
      GPIO.setmode(GPIO.BCM)
      GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)
      GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_UP)
      GPIO.setup(25, GPIO.OUT)
   except:
      emailpy.SendMail(   username = "giampiero.novello@office365.com",
         password = "Autec2025!",
         mail_from = "   AS000861@autecsafety.com",
         mail_to = "giuliano.cristofoli@autecsafety.com",
         mail_subject = "StartingTest ",
         mail_body = "Gpio Non inizializzati PROBLEMA")
   try:
      Modbus=mod.ModClient(ipAdd="10.100.16.41")
      print(Modbus.ibm_32sf(Modbus.ibm_f32s(1.25)))
      print(Modbus.ibm_32sf(Modbus.ibm_f32s(10.25)))
      print(Modbus.ibm_32sf(Modbus.ibm_f32s(1000.25)))
      print(Modbus.GetSMax())
   except:
      emailpy.SendMail(   username = "giampiero.novello@office365.com",
         password = "Autec2025!",
         mail_from = "   AS000TST@autecsafety.com",
         mail_to = "giuliano.cristofoli@autecsafety.com",
         mail_subject = "StartingTest ",
         mail_body = "ModBus Non inizializzati PROBLEMA")
   try:
      A=Analogscan1.AnScan(low_channel=0,high_channel=15,rat=8000,samples=(8000*(2*16)))
      print(A.A2DNAME)
   
   except:
      emailpy.SendMail(   username = "giampiero.novello@office365.com",
         password = "Autec2025!",
         mail_from = "   AS000861@autecsafety.com",
         mail_to = "giuliano.cristofoli@autecsafety.com",
         mail_subject = "StartingTest ",
         mail_body = "DAC NON INIZIALIZZATO  Non inizializzati PROBLEMA")
   try: 
      D=Db7.db(server="10.16.0.197",database="Lab1")
      print(D.TableNameis())
      D.DeleteAllTable()
      D.MakeConfigTable("CONFIG123")
      D.WriteConfigTableRaw(NextTable="CONFIG123",NomeTest="Mio" ,NomeMacchina="Bo" ,IpMacchina="69.69.69.69",NomeArticolo="cazz0" ,Dataeora="1" ,Errori=0,StartIndex=0,StopIndex=1000 ,DurataAcq=10 ,FreqDiCamp=15000 ,Periododiacquisizione=1000 ,NomeA2D01="NULL" ,NomeA2D11="NULL",NomeA2D21="NULL",NomeA2D31="NULL",NomeA2D41="NULL",NomeA2D51="NULL",NomeA2D61="NULL",NomeA2D71="NULL",NomeA2D81="NULL",NomeA2D91="NULL",NomeA2DA1="NULL" ,NomeA2DB1="NULL",NomeA2DC1="NULL",NomeA2DD1="NULL",NomeA2DE1="NULL",NomeA2DF="NULL",NomeA2D02="NULL",NomeA2D12="NULL",NomeA2D22="NULL",NomeA2D32="NULL",NomeA2D42="NULL",NomeA2D52="NULL",NomeA2D62="NULL",NomeA2D72="NULL",NomeA2D82="NULL",NomeA2D92="NULL",NomeA2DA2="NULL",NomeA2DB2="NULL",NomeA2DC2="NULL",NomeA2DD2="NULL",NomeA2DE2="NULL",NomeA2DF2="NULL",NomeA2D03="NULL",NomeA2D13="NULL",NomeA2D23="NULL",NomeA2D33="NULL",NomeA2D43="NULL",NomeA2D53="NULL",NomeA2D63="NULL",NomeA2D73="NULL",NomeA2D83="NULL",NomeA2D93="NULL",NomeA2DA3="NULL",NomeA2DB3="NULL",NomeA2DC3="NULL",NomeA2DD3="NULL",NomeA2DE3="NULL",NomeA2DF3="NULL",ciclitracontrollo=1000,ciclitraAcquisizione =100,ciclitotali=1000 ,numerosemicilci=5 ,pausa=1 ,sel=0 ,f=0  ,AMax =1,VMax=2 ,A0=3  ,SMax=4 )
      Table_config=D.ReadConfigTableRaw("CONFIG123")
      
     
   except:
       emailpy.SendMail(   username = "giampiero.novello@office365.com",
         password = "Autec2025!",
         mail_from = "   AS000861@autecsafety.com",
         mail_to = "giuliano.cristofoli@autecsafety.com",
         mail_subject = "StartingTest ",
         mail_body = "Database di configurazione  Non inizializzati PROBLEMA")
   try:
      DS=Db7.db(server="10.16.0.197",database="AS000861")
      DS.TableNameis()
      DS.DeleteAllTable()
      DS.GetDB()
      DS.TableNameis()
      TableName="LabTTTTTA"
      NameTabella="JOYSTICK1"
      ##DS.MakeRefTable(TableName)
      ##NameTabella=DS.InsertDataInRefTable(TableName=TableName,NomeTest="Test1",Dataeora="111",Articolo="ART1",NomeRaspberry="RA1",NumeroBit=16,Banda=4000,FreqquenzaCampionamento=16000,TestNr=1)
      DS.MakeJsonTable(NameTabella)
   except:
      emailpy.SendMail(   username = "giampiero.novello@office365.com",
         password = "Autec2025!",
         mail_from = "   AS000382@autecsafety.com",
         mail_to = "giuliano.cristofoli@autecsafety.com",
         mail_subject = "StartingTest ",
         mail_body = "AS000861 Db   Non inizializzati PROBLEMA")
   kk=0
   A2DName=[]
   while(kk<16):
      A2DName.append(A.A2DNAME[(kk%16)]+"_FRST")
      kk=kk+1
   while(kk<32):
      A2DName.append(A.A2DNAME[(kk%16)]+"_SECN")
      kk=kk+1
   while(kk<48):
      A2DName.append(A.A2DNAME[(kk%16)]+"_THRD")
      kk=kk+1
   ciclo=0
   cicloDAC=0
   Pin24=False
   Pin23=False
   GPIO.output(25,GPIO.LOW)
   while(1):
      if(GPIO.input(24)):
         if(not Pin24):
            Pin24=True
            GPIO.output(25,GPIO.HIGH)
            
            J=(cicloDAC & 0x03)
            '''
            attenzione il ciclo DAC fa 1000,1001,1002   ===>1003 is errore
            '''
            cicloDAC=int(Modbus.GetCicliAttuali())
            A.SavedScan(DS.InsertJsonInTable,NameTabella,(cicloDAC-J),J,A2DName)
            time.sleep(0.5)
            print("=====>ATTENZIONE cicloDAC",cicloDAC)
            GPIO.output(25,GPIO.LOW)
      else:
         Pin24=False
      if(GPIO.input(23)):
         if(not Pin23):
            Pin23=True
            #GPIO.output(25,GPIO.HIGH)
            time.sleep(0.5)
            ciclo=ciclo+1
            ciclo=int(Modbus.GetCicliAttuali())
            print("Ciclco attuale ",ciclo)
            AB=Modbus.GetStart()
            print(AB)
            #GPIO.output(25,GPIO.LOW)
      else:
         Pin23=False
   while(0):
      ciclo=int(Modbus.GetCicliAttuali())
      print("test loop",ciclo)
      GPIO.output(25,GPIO.LOW)
      time.sleep(1)
      GPIO.output(25,GPIO.HIGH)
      time.sleep(1)
      ciclo=int(Modbus.GetCicliAttuali())
      print(Modbus.GetStart())


   print("Fine")
#######
if __name__ == '__main__':
    main()
   
