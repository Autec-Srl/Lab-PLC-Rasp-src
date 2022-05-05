#importiamo le librerie per il controllo dell'interfaccia GPIO
import RPi.GPIO as GPIO
import time
import sys
import unittest
from emailnov import SendMail
import paramiko
import Db3
import _thread
import time
import  subprocess
import os
import Safetycheck
import pyjson2
#import email
import Analogscan
#definizione delle funzioni
global TableName
global NomeA2D
global Articolo
global NomeTabella
NomeTest="PrimoTestG"
NumeroTot=10
NumeroParziale=10
Nodo="RASPBERRY4-1"
Dataais=""
ts=0
global NameTabella

def print_time( threadName, delay):
   count = 0
   while count < 5:
      time.sleep(delay)
      count += 1
      print ("%s: %s" % ( threadName, time.ctime(time.time()) ))

# Create two threads as follows
#try:
#   _thread.start_new_thread( print_time, ("Thread-1", 2, ) )
#   _thread.start_new_thread( print_time, ("Thread-2", 4, ) )
#except:
def copy_file(hostname, port, username, password, src, dst):
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    print (" Connecting to %s \n with username=%s... \n" %(hostname,username))
    t = paramiko.Transport(hostname, port)
    t.connect(username=username,password=password)
    sftp = paramiko.SFTPClient.from_transport(t)
    print ("Copying file: %s to path: %s" %(src, dst))
    sftp.put(src, dst)
    sftp.close()
    t.close() 
Dataais=0
#print "time.time(): %f " %  time.time()
#print time.localtime( time.time() )
ts=0
def Analog(threadName, ciclo,NomeTabella,DD,NameTabella1):
   print('Analog\n')
   global NomeTest
   global NumeroTot
   global NumeroParziale
   global Nodo
   global ts
   global Dataais
   global NomeA2D
   global Articolo
   ts=ciclo
   try:
      A=Analogscan.AnScan(low_channel=0,high_channel=15,rat=15000,samples=(15000*16*5))
   except:
      print("Ananlog scan not working\n")
   j=0
   plotting=False
   time.sleep(20)
   try:
      j=0
      while(j<3):
         R=A.doScan(i=j)
         print("len is",len(R[0]))
         print("A rate is",A.rate)
         x=[]
         i=0
         print("len is ",len(R))
         while(i<len(R)):
            nomefile="saved%d-%d-%d.txt"%(i,j,k)
            filename="/home/ubuntu/"+nomefile
            print("File name is ",filename)
            f = open(filename, "a")
            kk=0
            while(kk<len(R[i])):
               f.write(" %f" %R[i][kk])
               kk=kk+1
            f.close()
            #subprocess.run(["scp", filename, "novello@10.100.16.101:/home/novello/lab/plot "])
            #pyjson2.TestParameterWr(filename,NomeTest,data,Articolo,Nodo,DescrizIngresso,BitQuant,NumeroCiclo,Banda,Fc,NumeroCampioni,Errori,Dati=R[kk])
            print("filename is ",filename)
            copy_file("10.100.16.40", 22, "lab01", "novello", filename, "/home/lab01/Test1/AS000TST/"+nomefile)
            i=i+1
         
         j=j+1
   except:
      R=[]
      R.append(0)
      R.append(0)
      print("R is  errore\n",R)
   while(j<16):
      x=[]
      i=0
      while(i<len(R[0])):
         x.append(i/(A.rate))
         i=i+1
      j=j+1
   if(plotting):
      plt.plot(x,R[0])
      plt.plot(x,R[1])
      plt.plot(x,R[8])
      plt.show()
   else:
      data=Dataais
      BitQuant=16
      NumeroCiclo=ts
      ciclos=("%d"%ts)
      print("Ciclo is",ciclos)
      kk=0
      while(kk<(15-0+1)):
         DescrizIngresso=NomeA2D[kk]
         filename=NomeTest+"E"+DescrizIngresso+"E"+Articolo+"E"+data+"E"+ciclos+".json"
         z=NomeTest+"E"+DescrizIngresso+"E"+Articolo+"E"+data+"E"+ciclos+".txt"
         print("zzz  complex name",z)
         print("file name is",filename)
         print("Descrizione ingresso",DescrizIngresso)
         print("Numero ciclo",ciclos)
         print("Tabella nome is",NomeTabella)
         Banda=4000 #filtro HW
         Fc=(15000)
         NumeroCampioni=(15000*16*5)
         Errori="OK"
         print("filename is",filename)
         #z="/home/ubuntu/demo%d"%ciclo
         #z=z+".txt"
         f = open(z, "w")
         i=0
         while(i<len(R[kk])):
            f.write(" %f\n" %R[kk][i])
            i=i+1
         f.close()
         print("z is",z)
         pyjson2.TestParameterWr(filename,NomeTest,data,Articolo,Nodo,DescrizIngresso,BitQuant,NumeroCiclo,Banda,Fc,NumeroCampioni,Errori,Dati=R[kk])
         #subprocess.call(["scp", filename, "/home/lab1/Test1"])
         #sftp.put(filename, '/home/lab1/Test1')
         #sftp.put(z, '/home/lab1/Test1')
         print("z is ",z)
         print("filename is ",filename)
         copy_file("10.100.16.40", 22, "lab1", "novello", z, "/home/lab1/Test1/AS000382/"+z)
         copy_file("10.100.16.40", 22, "lab1", "novello", filename, "/home/lab1/Test1/AS000382/"+filename)
         time.sleep(1)
         pathfilename="/home/ubuntu/"+filename
         print("Descrizione ingresso is ",DescrizIngresso)
         print("Nome Tabella",NomeTabella)
         print("FILENAME",pathfilename)
         print(" A2D name k",NomeA2D[kk])
         print(" CICLOS ",ciclos)
         DD.InsertJsonRawInTable(NameTabella1,pathfilename,NomeA2D[kk],ciclos)
         time.sleep(1)
         subprocess.run(['rm','-rf',z])
         subprocess.run(['rm','-rf',filename])
         kk=kk+1
#for i in range(3):
#    t = threading.Thread(target=Analog)
#    t.start()

''' ATTENZIONE PER ABILITARE PIN
#definiamo che pinLedLeft e pinLedRight sono due pin di output
#!/usr/bin/env python3
import signal
import sys
import RPi.GPIO as GPIO
BUTTON_GPIO = 16

def signal_handler(sig, frame):
    GPIO.cleanup()
    sys.exit(0)
    
def button_pressed_callback(channel):
    print("Button pressed!")
    
if __name__ == '__main__':
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(BUTTON_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(BUTTON_GPIO, GPIO.FALLING, callback=button_pressed_callback, bouncetime=100)
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.pause()
'''
class PistoneRPi():
   def __init__(self,Debug=0,S=[1,2],P=[18,17]):
      # Set up GPIO pins
      GPIO.setmode(GPIO.BCM)
      GPIO.setwarnings(False)
      self.S=S
      self.P=P
      print("S[0] is sensore basso")
      print("S[1] is sensore alto")
      i=0
      while(i<len(self.S)):
         GPIO.setup(self.S[i], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
         print("pin In Ingresso is",S[i])
         i=i+1
      i=0
      while(i<len(P)):
         GPIO.setup(self.P[i] , GPIO.OUT)
         #print("PIN IN OUT IS ",P[i])
         i=i+1
      print("iNIZIALIZZO A 0 ")
      self.setPin(self.P[1],0)
      self.setPin(self.P[0],0)
      print("FINE INIT")
      return
      i=0
      '''
      ATTENZIONE SECONDO INDICAZIONI DI GIULIANO LO POSTO PRIMA SU  PERC
      ATTENZIONE NON PARTE BENE...... 
      '''
      if(self.getPin(self.S[1])==0):
         print("UP INIT PHASE ==============>>>>S[1] is 0")
         while(self.getPin(self.S[0])==0):#attenzione magnetico 
            self.setPin(self.P[1],1) ##DOWN
            self.setPin(self.P[0],0)
            time.sleep(1)
            print("Mouvo pistoni test")
            self.setPin(self.P[1],0) ##DOWN
            self.setPin(self.P[0],1)
            time.sleep(1)
            #time.sleep(0.05)
            #print("UP S0 is",self.getPin(self.S[0]))
            #print("UP S1 is",self.getPin(self.S[1]))
            #print("i up is",i)
            #time.sleep(0.3)
            i=i+1
      '''
      # mi devo portare in posizione fissa....
      while((self.getPin(self.S[0])==0)and(self.getPin(self.S[1])==0)):
         self.setPin(self.P[1],1)  #UP
         self.setPin(self.P[0],0)
         time.sleep(0.4)
         self.setPin(self.P[1],0) #DOWN
         self.setPin(self.P[0],1)
         print("S0",self.getPin(self.S[0]))
         print("S1",self.getPin(self.S[1]))
         time.sleep(0.5)
         i=i+1
         print(i)
         print("S0",self.getPin(self.S[0]))
         print("S1",self.getPin(self.S[1]))
      '''
   def Up(self):  #se magnetici
      i=0
      if(self.getPin(self.S[1])==1):
         #print("UP S[1] is 1")
         while(self.getPin(self.S[0])==0):
            #print("===>>>UP S0 is 0")
            self.setPin(self.P[1],1)
            self.setPin(self.P[0],0)
            #print("UP S0 is",self.getPin(self.S[0]))
            #print("UP S1 is",self.getPin(self.S[1]))
            #print("i up is",i)
            #time.sleep(0.3)
            i=i+1
      else:
         print("UP Enabled ? S[1] is 0",self.getPin(self.S[1]))
         return
         self.setPin(self.P[1],1)
         self.setPin(self.P[0],0)
         time.sleep(1)
         self.setPin(self.P[1],0)
         self.setPin(self.P[0],0)
      return(self.getPin(self.S[0]),self.getPin(self.S[1]))

   def Down(self):
      i=0
      if (self.getPin(self.S[0])==1):
         #print("Down s[0]=1")
         while(self.getPin(self.S[1])==0):
            #print("===>>>>>DOWN S1 is 0")
            self.setPin(self.P[1],0)
            self.setPin(self.P[0],1)
            #print("DOWN S0 is",self.getPin(self.S[0]))
            #print("DOWN S1 is",self.getPin(self.S[1]))
            #print(" i down is",i)
            #time.sleep(0.3)
            i=i+1
      else:
         print( "DOWN s[0] is 0=?",self.getPin(self.S[0]))
         return
         self.setPin(self.P[1],0)
         self.setPin(self.P[0],1)
         time.sleep(1)
         self.setPin(self.P[1],0)
         self.setPin(self.P[0],0)
      return(self.getPin(self.S[0]),self.getPin(self.S[1]))

   def Ciclo(self):
      pass
    
   def __del__(self):
      self.setPin(self.P[1],0)
      self.setPin(self.P[0],0)    
      print("Close tasti")
        
   def setPin(self,inp,value):
      if(value==1):
         GPIO.output(inp,GPIO.HIGH)
      else:
         GPIO.output(inp,GPIO.LOW)
            
   def getPin(self,inp):
      if(GPIO.input(inp)==True):
         return 1
      else:
         return 0
        
    # in posizione 0 UP
    # in posizione 1 DOWN
    #attenzzione qui metto le funzioni di test della libreria.
import pytest
def main():
   


def test_func_fast():
    pass


@pytest.mark.slow
def test_func_slow():
    pass
   print("Fine")
#######
if __name__ == '__main__':
    main()
   
