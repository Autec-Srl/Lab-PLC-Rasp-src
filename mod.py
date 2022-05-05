from modbus.client import *
import struct

class ModClient():
  def __init__(self,ipAdd="10.100.16.41"):
    self.c=client(host=ipAdd)
    
  def Read(self,Add,lung):
    return  self.c.read(FC=3,ADR=Add,LEN=lung)
    
  def Write(self,Add,Data):
    self.c.write(Data,FC=15,ADR=Add)
    return 0


  def ibm_f32s(self,f):
    res=struct.unpack('!I', struct.pack('!f', f))[0]
    print(type(res))
    b=[]
   
    b.append(int((res>>16) & 0x0ffff))
    b.append(int(res & 0x0ffff))
    return b
  '''
    convert 2 in in float
  '''
  def ibm_32sf(self,f):
    #R=struct.pack('<f', f) # little-endian
    raw = struct.pack('>HH', f[0], f[1])    # from two unsigned shorts
    res=struct.unpack('>f', raw)[0]              # to one float
    return res

  
  def IntToBytes(self,f):
    ba = []
    ba.append((f>>16) & 0x0ffff)
    ba.append(f & 0x0ffff)
    return ba

  def BytesToInt(self,h):
    return h[1]+h[0]*(256*256)
  '''
    mi serve per ricalcolare la curva
    se 1 ricalcolo 
  '''
  def GetCaricamentoRicetta(self):
    R=self.Read(Add=0,lung=2)
    if(R[1] & 0x01):
      return True
    else:
      return False
  '''
  '''
    
  def SetCaricamentoRicetta(self):
    self.Write(Add=0,Data=0x01)
  '''
  '''
    
  def GetResetCiclo(self):
    R=self.Read(Add=0,lung=2)
    if(R[1] & 0x02):
      return True
    else:
      return False
  '''
     reset ciclo conteggi per conteggio test .
     equivalente di start nuova misura e voi con i 10000000
  '''
  def SetResetCiclo(self):
    self.Write(Add=0,Data=0x02)
  '''
  '''

  def SetHoming(self,home):
    """
     def SetHoming(self):
     azzeramento asse ... mi mette nella posizione di defoautl

    :param home: viene fornita la posizione in formato float 32 che viene poi convertita.
    
    :return: 0 se tutto Ok  1 se errore
    """ 
    return self.Write(Add=4,Data=self.ibm_f32s(home))

  def GetHoming(self):
    """
     def GetHoming(self):
     does ....

    :param home: null 
    
    :return: ritorna la posizione in float32
    """
    R=self.Read(Add=0,lung=2)
    if(R[1] & 0x04):
      return True
    else:
      return False

  def SetResetrAllarmi(self):
    """
     def SetAllarmi(self):
     does ...

    :param home: Null
    :return: float ritorna la posizione
    reset allarmi se allarme non si muovono più da li 
    e tiene tutto fermo
    """ 
    
    return self.Write(Add=0,Data=0x08)
    
  def GetAllarmi(self):
    """
     def SetHoming(self):
     does ....

    :param home: is a parameter float with the  initial position 
    
    :return: 0 se tutto Ok  1 se errore
    """
    R=self.Read(Add=0,lung=2)
    if(R[1] & 0x08):
      return True
    else:
      return False
  
  def GetSMax(self):
    """
     def GetSMax(self):
     parametri della curva (Ricetta)
     Semicorsa massima salvo su db
     viene  espresso in mm

    :param home: null 
    
    :return: ritorna il parametro sMax in floaT
    """
    R=self.Read(Add=2,lung=2)
    return self.ibm_32sf(R)
    
  def SetSMax(self,d):
    """
     def SetSMax(self):
     does simicorsa massima e viene espresso in float mm

    :param home: Setta Smax  
    
    :return: 0 se tutto Ok  1 se errore
    """
    return  self.Write(Add=2,Data=self.ibm_f32s(d))
    
  def GetA0(self):
    """
     def SetHoming(self):
     Semiangolo in gradi con float  angolo di apertura del joystic

    :param home:
    
    :return: return A0 float 32
    """
    R=self.Read(Add=4,lung=2)
    return self.ibm_32sf(R)
    
  def SetA0(self,d):
    """
     def SetHoming(self):
     does ....

    :param home: is a parameter float A0
    
    :return: 0 se tutto Ok  1 se errore
    """
    return  self.Write(Add=4,Data=self.ibm_f32s(d))
    
  def GetvMax(self):
    """
     def SetHoming(self):
     velocita angolare massima in float


    :param home:
    
    :return: vMax che float 32
    """
    R=self.Read(Add=6,lung=2)
    return self.ibm_32sf(R)
    
  def SetvMax(self,d):
    """
     def SetHoming(self):
     does ....

    :param home: velocità massima
    
    :return: 0 se tutto Ok  1 se errore
    """
    return self.Write(Add=6,Data=self.ibm_f32s(d))

  def GetaMax(self):
    """
     def SetHoming(self):
     aMax accelerazione angolare Massimma raggiunta

    :param home: null
    
    :return: il valore dell' accelerazione massima
    """
    R=self.Read(Add=8,lung=2)
    return self.ibm_32sf(R)
    
  def SetaMax(self,d):
    """
     def SetHoming(self):
     does ....

    :param home: is a parameter float with the  initial position 
    
    :return: 0 se tutto Ok  1 se errore
    """
    self.Write(Add=8,Data=self.ibm_f32s(d))

    
  def Setf(self,d):
    """
     def SetHoming(self):
     Frequenza di test del singolo ciclo.
     Dato Amax /Vmax calcola F e quindi la posso leggere.

    :param home: is f  
    
    :return: 0 se tutto Ok  1 se errore
    """
    return self.Write(Add=10,Data=self.ibm_f32s(d))
    
  def Getf(self):
    """
     def SetHoming(self):
     does ....

    :param home: null 
    
    :return: 0 se tutto Ok  1 se errore
    """
    R=self.Read(Add=10,lung=2)
    return self.ibm_32sf(R)

    
  def Setsel(self,d):
    """
     def Setsel(self):
     sel è selettore 0,1,2 
     0==> guado Vmax e calcolo tutto in funzione dei Vmax
     1==> Guardo Amax calcolo la curva in funzione di Amax accelezarione massima
     2=>> guardo il parametro f frequenza
     
    :param home:  
    
    :return: 0 se tutto Ok  1 se errore
    """
    self.Write(Add=12,Data=self.IntToBytes(d))

  def Getsel(self):
    """
     def SetHoming(self):
     does ....

    :param home: Null
    
    :return: sel
    """
    R=self.Read(Add=12,lung=2)
    return self.BytesToInt(R)

  def SetPausa(self,d):
    """
     def SetPausa(self):
     pausa tra semicicli in ms ogni 5 semicicli  tipo 1000 

    :param home: is a parameter float with the  initial position 
    
    :return: 0 se tutto Ok  1 se errore
    """
    self.Write(Add=14,Data=self.ibm_32sf(d))
  
  def GetPausa(self):
    """
     def GetPausa(self):
     .does ....

    :param home: Null
    
    :return: int
    """
    R=self.Read(Add=14,lung=2)
    return self.BytesToInt(R)

  def GetNumSemiCicli(self):
    """
     def GetNumSemiCicli(self):
     numero simicicli tra pausa e altra 
     tutto da destra a sinistra.(5) più mezzo secondo e via...

    :param home:  
    
    :return: Numero di Semiclicli
    """
    R=self.Read(Add=16,lung=2)
    return self.BytesToInt(R)

  def SetNumSemiCicli(self,d):
    """
     def SetNumSemiCicli(self):
     does ....

    :param : Numero di Semicicli
    
    :return: 0 se tutto Ok  1 se errore
    """
    return self.Write(Ass=16,Data=self.IntToBytes(d))

  def SetCicliTotali(self,d):
    """
     def SetCicliTotali(self):
     sono i cicli totali che devo fare complessivamente...

    :param home: Cicli Totali 
    
    :return: 0 se tutto Ok  1 se errore
    """
    return self.Write(Ass=18,Data=self.IntToBytes(d))
    
  def GetCicliTotali(self):
    """
     def GetCicliTotali(self):
     does ....

    :param home: null
    
    :return: ritorna numero di cicli totali
    """
    R=self.Read(Add=18,lung=2)
    return self.BytesToInt(R)

  def SetCicliTraAcq(self,d):
    """
     def SetHoming(self):
     numero cicli tra acquisizioni
     tra a2d 2 a2d lettura

    :param home: is a parameter float with the  initial position 
    
    :return: 0 se tutto Ok  1 se errore
    """
    return self.Write(Ass=20,Data=self.IntToBytes(d))

  def GetCicliTraAcq(self):
    """
     def GetCicliTraAcq(self):
     does ....

    :param home: null
    
    :return: numero cicli 
    """
    R=self.Read(Add=20,lung=2)
    return self.BytesToInt(R)

  def SetCicliTraPause(self,d):
    """
     def SetCicliTraPause(self):
     does ....

    :param home: is a paramet
    
    :return: 0 se tutto Ok  1 se errore
    """
    return self.Write(Add=22,Data=self.IntToBytes(d))
    
  def GetCicliTraPause(self):
    """
     def SetHoming(self):
     pause meccaniche pausa meccanica a 500kcicli
     di controllo per lo stato del test meccanico
     si aspetta un email

    :param home: null
    
    :return: numero cicli tra le pause
    """
    R=self.Read(Add=22,lung=2)
    return self.BytesToInt(R)

#READ only 
  def GeManuale(self):
    """
     def GetMa(self):
     

    :param home: is a parameter float with the  initial position 
    
    :return: 0 se tutto Ok  1 se errore
    """
    R=self.Read(Add=40,lung=2)
    print("%x"%R[0])
    print("%x"%R[1])
    if(R[0] & 0x0100):
      return True  #automatico
    else:
      return False #
    
  def GetStart(self):
    """
     def SetHoming(self):
      mi dice se sono in start o stop

    :param home: is a parameter float with the  initial position 
    
    :return: 0 se tutto Ok  1 se errore
    """
    R=self.Read(Add=40,lung=2)
    print("%x"%R[0])
    print("%x"%R[1])
    if(R[0] & 0x0100):
      return True  #automatico
    else:
      return False #
    return R

  def GeEmergenze(self):
    """
     def SetHoming(self):
    spedisce email in caso di allarme

    :param home: is a parameter float with the  initial position 
    
    :return: 0 se tutto Ok  1 se errore
    """
    R=self.Read(Add=84,lung=2)

  def GetCicliAttuali(self):
    """
     def GetCicliAttuali(self):
     ciclo in avanzamento

    :param home: is a parameter float with the  initial position 
    
    :return: 0 se tutto Ok  1 se errore
    """
    R=self.Read(Add=44,lung=2)
    return self.BytesToInt(R)#############

  def GeCodiceAllarmeDriver(self):
    """
     def GeCodiceAllarmeDriver(self):
     il codice da manuale possono essere un 100

    :param home: is a parameter float with the  initial position 
    
    :return: 0 se tutto Ok  1 se errore
    """
    R=self.Read(Add=46,lung=2)
    return self.ibm_32sf(R) ###########
  def GePosizioneAttuale(self):
    """
     def SetHoming(self):
     instantanea posizione

    :param home: is a parameter float with the  initial position 
    
    :return: 0 se tutto Ok  1 se errore
    """
    R=self.Read(Add=51,lung=2)
    return self.ibm_32sf(R)

  def GetVelocitaAttuale(self):
    """
     def SetHoming(self):
     velocità istantanea

    :param home: is a parameter float with the  initial position 
    
    :return: 0 se tutto Ok  1 se errore
    """
    R=self.Read(Add=53,lung=2)
    return self.ibm_32sf(R)

  def GetCorrenteAttuale(self):
    """
     def SetHoming(self):
     corrente istantanea

    :param home: is a parameter float with the  initial position 
    
    :return: 0 se tutto Ok  1 se errore
    """
    R=self.Read(Add=55,lung=2)
    return self.ibm_32sf(R)

  def GetPosizione1(self):
    """
     def GetPosizione1(self):
     does ....

    :param home: is a parameter float with the  initial position 
    
    :return: 0 se tutto Ok  1 se errore
    """
    R=self.Read(Add=57,lung=2)
    return self.ibm_32sf(R)

  def GetPosizione2(self):
    """
     def SetHoming(self):
     does ....

    :param home: is a parameter float with the  initial position 
    
    :return: 0 se tutto Ok  1 se errore
    """
    R=self.Read(Add=59,lung=2)
    return self.ibm_32sf(R)
    
  def GetCalcoloCurva(self):
    """
     def SetHoming(self):
     does ....

    :param home: is a parameter float with the  initial position 
    
    :return: 0 se tutto Ok  1 se errore
    """
    R=self.Read(Add=42,lung=2)
  def GetEmergenza(self):
    """
     def SetHoming(self):
     does ....

    :param home: is a parameter float with the  initial position 
    
    :return: 0 se tutto Ok  1 se errore
    """
    R=self.Read(Add=42,lung=2)
  def GetErroriAssi(self):
    """
     def GetErroriAsse(self):
     does ....

    :param home: is a parameter float with the  initial position 
    
    :return: 0 se tutto Ok  1 se errore
    """
    R=self.Read(Add=42,lung=2)
  def GetAnomaliaRecuperoCurva(self):
    """
     def SetHoming(self):
     does ....

    :param home: is a parameter float with the  initial position 
    
    :return: 0 se tutto Ok  1 se errore
    """
    R=self.Read(Add=42,lung=2)
  def GetAnomaliaCaricoCurva(self):
    """
     def SetHoming(self):
     does ....

    :param home: is a parameter float with the  initial position 
    
    :return: 0 se tutto Ok  1 se errore
    """
    R=self.Read(Add=42,lung=2)
  def GetAllarmiindiceCarico(self):
    """
     def SetHoming(self):
     does ....

    :param home: is a parameter float with the  initial position 
    
    :return: 0 se tutto Ok  1 se errore
    """
    R=self.Read(Add=42,lung=2)

print("Starting")

#import RPi.GPIO as GPIO
import time
import sys
#import lablib
def main_ref():
  A=ModClient(ipAdd="10.100.16.41")
  print(A.ibm_32sf(A.ibm_f32s(1.25)))
  print(A.ibm_32sf(A.ibm_f32s(10.25)))
  print(A.ibm_32sf(A.ibm_f32s(1000.25)))
  print(A.ibm_32sf(A.ibm_f32s(10000.25)))
  print(A.ibm_32sf(A.ibm_f32s(-12345.25)))
  print(A.ibm_32sf(A.ibm_f32s(-12345789.25)))
  print(A.GetSMax())
  print(A.GetA0())
  print(A.GetvMax())
  print(A.GetaMax())
  print(A.Getf())
  print(A.Getsel())
  print(A.GetPausa())
  print(A.GetNumSemiCicli())
  print(A.GetHoming())
  print(A.GetCicliTraAcq())
  print(A.GetCicliTotali())
  print(A.BytesToInt(A.IntToBytes(10)))
  print(A.BytesToInt(A.IntToBytes(100)))
  print(A.BytesToInt(A.IntToBytes(1000)))
  print(A.BytesToInt(A.IntToBytes(10000)))
  print(A.BytesToInt(A.IntToBytes(100000)))
  print(A.BytesToInt(A.IntToBytes(1000000)))
  print(A.BytesToInt(A.IntToBytes(10000000)))
  print(A.GetCaricamentoRicetta())
  print(A.GetResetCiclo())
  print(A.GetHoming())
  print(A.GetAllarmi())
  print("FINE")


import os
import unittest
class MODTestCase(unittest.TestCase):
    
    def setUp(self):
      self.A=ModClient(ipAdd="10.100.16.41")

    def test_param2(self):
      self.assertEqual(self.A.ibm_32sf(self.A.ibm_f32s(1.25)),1.25)
      self.assertEqual(self.A.ibm_32sf(self.A.ibm_f32s(10.25)),10.25)
      self.assertEqual(self.A.ibm_32sf(self.A.ibm_f32s(1000.25)),1000.25)
      self.assertEqual(self.A.ibm_32sf(self.A.ibm_f32s(10000.25)),10000.25)
      self.assertEqual(self.A.ibm_32sf(self.A.ibm_f32s(-12345.25)),-12345.25)
      self.assertEqual(self.A.ibm_32sf(self.A.ibm_f32s(-12345789.25)),-12345789.0)
    def test_param1(self):
      self.assertEqual(self.A.ibm_32sf(self.A.ibm_f32s(1.25)),1.25)
      self.assertEqual(self.A.BytesToInt(self.A.IntToBytes(10)),10)
      self.assertEqual(self.A.BytesToInt(self.A.IntToBytes(100)),100)
      self.assertEqual(self.A.BytesToInt(self.A.IntToBytes(1000)),1000)
      self.assertEqual(self.A.BytesToInt(self.A.IntToBytes(10000)),10000)
      self.assertEqual(self.A.BytesToInt(self.A.IntToBytes(100000)),100000)
      self.assertEqual(self.A.BytesToInt(self.A.IntToBytes(1000000)),1000000)
      self.assertEqual(self.A.BytesToInt(self.A.IntToBytes(10000000)),10000000)

if __name__ == "__main__":
    unittest.main()
    #main_ref()

                                  



