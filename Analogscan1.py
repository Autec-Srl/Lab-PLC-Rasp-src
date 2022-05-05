"""
Wrapper call demonstrated:        ai_device.a_in_scan()

Purpose:                          Performs a continuous scan of the range
                                  of A/D input channels

Demonstration:                    Displays the analog input data for the
                                  range of user-specified channels using
                                  the first supported range and input mode

Steps:
1.  Call get_daq_device_inventory() to get the list of available DAQ devices
2.  Create a DaqDevice object
3.  Call daq_device.get_ai_device() to get the ai_device object for the AI
    subsystem
4.  Verify the ai_device object is valid
5.  Call ai_device.get_info() to get the ai_info object for the AI subsystem
6.  Verify the analog input subsystem has a hardware pacer
7.  Call daq_device.connect() to establish a UL connection to the DAQ device
8.  Call ai_device.a_in_scan() to start the scan of A/D input channels
9.  Call ai_device.get_scan_status() to check the status of the background
    operation
10. Display the data for each channel
11. Call ai_device.scan_stop() to stop the background operation
12. Call daq_device.disconnect() and daq_device.release() before exiting the
    process.
"""
from __future__ import print_function
from time import sleep
from os import system
from sys import stdout
import time
import subprocess
import emailpy
import Db7
try:
    import matplotlib.pyplot as plt
except:
    print("NO PLT")
import wave, struct, math
import datetime
from uldaq import (get_daq_device_inventory, DaqDevice, InterfaceType,
                   DigitalDirection, DigitalPortIoType)


'''
NOT USED
sampleRate = 44100.0 # hertz
duration = 1.0 # seconds
frequency = 440.0 # hertz
obj = wave.open('sound.wav','w')
obj.setnchannels(1) # mono
obj.setsampwidth(2)
obj.setframerate(sampleRate)
for i in range(99999):
   value = random.randint(-32767, 32767)
   data = struct.pack('<h', value)
   obj.writeframesraw( data )
obj.close()
'''

from uldaq import (get_daq_device_inventory, DaqDevice, AInScanFlag, ScanStatus,
                   ScanOption, create_float_buffer, InterfaceType, AiInputMode)

'''
  1 self.daq_device.append(DaqDevice(self.devices[i])
  2 self.ai_device.append(self.daq_device[i].get_ai_device())
  3 self.ai_info.append(self.ai_device[i].get_info())
'''
class AnScan:
    def __init__(self,SNRList=["0206AFD9","0206B065","0206B01E"] ,low_channel=0,high_channel=0,rat=15000,samples=15000):
        """Analog input scan example."""
        self.daq_device = None
        self.ai_device = None
        self.status = ScanStatus.IDLE
        self.range_index = 0
        self.interface_type = InterfaceType.ANY
        self.low_channel = low_channel
        self.high_channel = high_channel
        self.samples_per_channel = samples
        self.rate = rat
        #self.scan_options = ScanOption.CONTINUOUS
        self.scan_options = ScanOption.BURSTMODE
        self.flags = AInScanFlag.DEFAULT
        self.x = datetime.datetime.now()
        self.daq_device=[]
        self.ai_device=[]
        self.ai_info=[]
        self.SNR=[]
        self.re=9
        self.NAME=[]
        self.A2DNAME=[]
        try:
            # Get descriptors for all of the available DAQ devices.
            # attenzione devo fare la dista by SNR nel giusto ordine
            self.devices = get_daq_device_inventory(self.interface_type)
            number_of_devices = len(self.devices)
            if number_of_devices == 0:
                raise RuntimeError('Error: No DAQ devices found')
            print('Found', number_of_devices, 'DAQ device(s):')
            for i in range(number_of_devices):
                print(self.devices[i].product_name)
                print(self.devices[i].unique_id)
                print(self.devices[i].dev_string) 
                print(self.devices[i].dev_interface) 
                # Create the DAQ device from the descriptor at the specified index.
                
            k=0
            while(k<3):
                print(self.devices[k].unique_id)
                if(self.devices[k].unique_id==SNRList[0]):
                    self.daq_device.append(DaqDevice(self.devices[k]))
                    self.ai_device.append(self.daq_device[0].get_ai_device())
                    self.ai_info.append(self.ai_device[0].get_info())
                k=k+1
            k=0
            while(k<3):
                print(self.devices[k].unique_id)
                if(self.devices[k].unique_id==SNRList[1]):
                    self.daq_device.append(DaqDevice(self.devices[k]))
                    self.ai_device.append(self.daq_device[1].get_ai_device())
                    self.ai_info.append(self.ai_device[1].get_info())
                k=k+1
            k=0
            while(k<3):
                print(self.devices[k].unique_id)
                if(self.devices[k].unique_id==SNRList[2]):
                    self.daq_device.append(DaqDevice(self.devices[k]))
                    self.ai_device.append(self.daq_device[2].get_ai_device())
                    self.ai_info.append(self.ai_device[2].get_info())
                k=k+1
            k=0    
            for i in range(number_of_devices):
                if self.ai_device[i] is None:
                    raise RuntimeError('Error: The DAQ device does not support analog ''input')
                # Verify the specified device supports hardware pacing for analog input.
                print("B")
                print(self.ai_device[i].get_info())
                if not self.ai_info[i].has_pacer():
                    raise RuntimeError('\nError: The specified DAQ device does not ''support hardware paced analog input')
                print("ciao1")
                # Establish a connection to the DAQ device.
                self.descriptor = self.daq_device[i].get_descriptor()
                dio_device = self.daq_device[i].get_dio_device()
                print('\nConnecting to', self.descriptor.dev_string, '- please wait...')
                # For Ethernet devices using a connection_code other than the default
                # value of zeo, change the line below to enter the desired code.
                self.daq_device[i].connect(connection_code=0)
                print("ciao2")
                ######### DIO CONNESSIONE
                # Get the port types for the device(AUXPORT, FIRSTPORTA, ...)
                dio_info = dio_device.get_info()
                port_types = dio_info.get_port_types()
                port_to_read = port_types[0]
                # Configure the port for input.
                port_info = dio_info.get_port_info(port_to_read)
                if (port_info.port_io_type == DigitalPortIoType.IO or port_info.port_io_type == DigitalPortIoType.BITIO):
                    dio_device.d_config_port(port_to_read, DigitalDirection.INPUT)
                
                print('    Function demonstrated: dio_device.d_in()')
                print('    Port: ', port_to_read.name)
                data = dio_device.d_in(port_to_read)
                res=((data & 0xf0)>>4)
                print(" attenzione è conforme a quanto descritto dal comportamento... altrimenti exit")
                print("0x%x\n"%res)
                print(type(res))
                self.re=res
                
                ###########DIO END
                # The default input mode is SINGLE_ENDED.
                self.input_mode = AiInputMode.SINGLE_ENDED
            
                 # If SINGLE_ENDED input mode is not supported, set to DIFFERENTIAL.
                if self.ai_info[i].get_num_chans_by_mode(AiInputMode.SINGLE_ENDED) <= 0:
                    self.input_mode = AiInputMode.DIFFERENTIAL
                    print("ERRORE NON SINGLE ENDED")

                # Get the number of channels and validate the high channel number.
                print("ciao3")
                number_of_channels = self.ai_info[i].get_num_chans_by_mode(self.input_mode)
                print("ciao4")
                if high_channel >= number_of_channels:
                    high_channel = number_of_channels - 1
                self.channel_count = high_channel - low_channel + 1
                print("ciao 5")

                # Get a list of supported ranges and validate the range index.
                self.ranges = self.ai_info[i].get_ranges(self.input_mode)
                print("ciao 6")
            if self.range_index >= len(self.ranges):
                self.range_index = len(self.ranges) - 1
            print("ciao 7")
                 # Allocate a buffer to receive the data.
            self.data = create_float_buffer(self.channel_count, self.samples_per_channel)
            print("ciao 8")
              
        except:
            print("errore init")
            emailpy.SendMail(   username = "giampiero.novello@office365.com",
                    password = "Autec2025!",
                    mail_from = "   AS000TST@autecsafety.com",
                    mail_to = "giuliano.cristofoli@autecsafety.com",
                    mail_subject = "DAC MESSAGE ",
                    mail_body = "ERRORE DI INIZIALIZZAZIONE DEL DAC ")
       
        #print('\n', self.descriptor.dev_string)
        print('    Function demonstrated: ai_device.a_in_scan()')
        
        self.A2DNAME=self.SetA2d(self.re)
        #print('    Range: ', self.ranges[self.range_index].name)
        #print('    Samples per channel: ', self.samples_per_channel)
        #print('    Rate: ', self.rate, 'Hz')
        #print('    Scan options:', self.display_scan_options(self.scan_options))

    def doScan(self,timeout=1000,i=0):
        #data = create_float_buffer(channel_count, self.samples_per_channel)
        # Start the acquisition.
        k=0
        i=0
        totalR=[]
        Result=[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
        #print(self.channel_count)
        try:
            rate = self.ai_device[i].a_in_scan(self.low_channel, self.high_channel, self.input_mode,self.ranges[self.range_index], self.samples_per_channel,self.rate, self.scan_options, self.flags, self.data)
        except:
            emailpy.SendMail(   username = "giampiero.novello@office365.com",
                    password = "Autec2025!",
                    mail_from = "   AS000382@autecsafety.com",
                    mail_to = "giuliano.cristofoli@autecsafety.com",
                    mail_subject = "DAC MESSAGE ",
                    mail_body = "Problemi nello scan giuliano controlla DAC ")
        index=-1
        T=0
        print("SAMPLES PER CHANNEL IS",self.samples_per_channel)
        while(T<(self.samples_per_channel/16)):#era /16
            # Get the status of the background operation
            self.status, transfer_status = self.ai_device[i].get_scan_status()
            index = transfer_status.current_index
            if(index>0):
                print('currentIndex = ', index, '\n')
                k=0
                try:
                    while(k<=index):
                        j=0
                        while(j<self.channel_count):
                            Result[j].append(self.data[k+j])
                            j=j+1 
                        k=k+j#1
                except:
                    print("errore nei dati ")
            T=len(Result[0])
            time.sleep(1)
            print("len res is",len(Result[0]))
        self.ai_device[i].scan_stop()
        time.sleep(1)
        print("FINE1")
        return Result
    ''' attenzione via USB la scansione non puo partire in contemporanea
        per evidenti problemi di simultaneita
        Mi serve un pin per trigger:
        ____-----________-----_______------_____
           i=0             i=1          i=2  ==> USB 0,1,2
    '''
    def SavedScan(self,DS,NameTabella1,ciclo,j,A2DName,Debug=False):
       
        ''' viene fatto per campionare indice per indice ....
        '''
        #while(j<3): j rapprensenta il DAC selezionato
        if(j>2):
            print("Errore del J Ho al massimo 3 A2D\n")
            j=0
        if(j<3):
            R=self.doScan(i=j)
            if(Debug):
                print("len is",len(R[0]))
                print("A rate is",A.rate)
                print("len is ",len(R))
            i=0
            '''  i rappresenta le trace da 1 a 16 '''
            while(i<len(R)):
                if(A2DName[j*16+i].strip()!="NULL"):
                    nomefile="saved%s-%d.txt"%((A2DName[j*16+i].strip(),ciclo))
                    filename="/home/ubuntu/"+nomefile
                    print("File name is ",filename)
                    f = open(filename, "a")
                    kk=0
                    '''
                    kk raprresentano i segnali ... dati campionati
                    '''
                    while(kk<len(R[i])):
                        f.write(" %f" %R[i][kk])
                        kk=kk+1
                    f.close()
                    print("filename is ",filename)
                    #viene usato per salvare i dati in fomato json 
                    #pyjson2.TestParameterWr(filename,NomeTest,data,Articolo,Nodo,DescrizIngresso,BitQuant,NumeroCiclo,Banda,Fc,NumeroCampioni,Errori,Dati=R[kk])
                    try:
                        #copy_file("10.100.16.40", 22, "lab01", "novello", z, "/home/lab1/Test1/AS000382/"+z)
                        copy_file("10.100.16.40", 22, "lab01", "novello", filename, "/home/lab01/Test1/AS000382/"+nomefile)
                    except:
                        print(" Impossibile salvare sul server")
                        emailpy.SendMail(   username = "giampiero.novello@office365.com",
                        password = "Autec2025!",
                        mail_from = "   AS000382@autecsafety.com",
                        mail_to = "giuliano.cristofoli@autecsafety.com",
                        mail_subject = "Save Scan errore ",
                        mail_body = "SERVER 10.100.16.40 Non raggiungibile ")
                    try:
                        #DatiDatabase.InsertJsonRawInTable(NameTabella1,pathfilename,NomeA2D[kk],ciclo)
                        print("Ciclo is",ciclo)
                        DS(NameTabella1,R[i],A2DName[i+(j*16)],ciclo)
                        time.sleep(1)
                    except:
                        print("DB NON ACCESSIBILE al cilo %d\n"%ciclo)
                        emailpy.SendMail(   username = "giampiero.novello@office365.com",
                        password = "Autec2025!",
                        mail_from = "   AS000382@autecsafety.com",
                        mail_to = "giuliano.cristofoli@autecsafety.com",
                        mail_subject = "DB Message ",
                        mail_body = "Scrittura nel DB Not working ")
                    #subprocess.run(['rm','-rf',z])
                    subprocess.run(['rm','-rf',filename])
                i=i+1
                
            #j=j+1
    
        
    def Sampling(self,Dato):
        R=[]
        step=self.channel_count
        i=0
        while(i<len(Dato)):
            R.append(Dato[i])
            i=i+step
        return R

    def __del__(self):
        if self.daq_device:
            #Stop the acquisition if it is still running.
            #if self.status == ScanStatus.RUNNING:
            #elf.ai_device.scan_stop()
            #if self.daq_device.is_connected():
            #    self.daq_device.disconnect()
            #self.daq_device.release()
            print("end")


    def display_scan_options(self,bit_mask):
        """Create a displays string for all scan options."""
        options = []
        if bit_mask == ScanOption.DEFAULTIO:
            options.append(ScanOption.DEFAULTIO.name)
        for option in ScanOption:
            if option & bit_mask:
                options.append(option.name)
        return ', '.join(options)
    def SetA2d(self,ingresso):
       
        A2DS0=["NULL","NULL","NULL","NULL","NULL","NULL","NULL","NULL","NULL","NULL","NULL","NULL","NULL","NULL","NULL","NULL"]
        A2DS6=["A1","Z1","VTAP1","NULL","H1","L1","Z_H1","Z_L1","A2","Z2","VTAP2","NULL","H2","L2","Z_H2","Z_L2"]
        A2DS4=["A1","Z1","NULL","SAFETY_NC1","H1","L1","Z_H1","Z_L1","A2","Z2","NULL","SAFETY_NC2","H2","L2","Z_H2","Z_L2"]
        A2DS7=["POT_OUT1","COM1","POT_UP_TAP1","POT_DN_TAP1","UP1","DOWN1","ZERO_TAP1","ZERO_ALIGN1","POT_OUT2","COM2","POT_UP_TAP2","POT_DN_TAP2","UP2","DOWN2","ZERO_TAP2","ZERO_ALIGN2"]
        A2DS2=["A1","NULL","VTAP1","NULL","H1","L1","DEAD_MAN1","NULL","A2","NULL","VTAP2","NULL","H2","L2","DEAD_MAN2","NULL"]
        A2DS5=["A1","NULL","NULL","SAFETY_NC1","H1","L1","DEAD_MAN1","NULL","A2","NULL","NULL","SAFETY_NC2","H2","L2","DEAD_MAN2","NULL"]
        A2DS9=["UP_1","DOWN_1","OOZ_1","VCOM","2ND_1","3RD_1","4TH_1","5TH_1","UP_2","DN_2","OOZ_2","DEAD_MAN","2ND_2","3RD_2","4TH_2","5TH_2"]
        self.NAME.append(A2DS0)
        self.NAME.append(A2DS0)
        self.NAME.append(A2DS2)
        self.NAME.append(A2DS0)
        self.NAME.append(A2DS4)
        self.NAME.append(A2DS5)
        self.NAME.append(A2DS6)
        self.NAME.append(A2DS7)
        self.NAME.append(A2DS0)
        self.NAME.append(A2DS9)
        return self.NAME[ingresso]


# Create two threads as follows
#try:
#   _thread.start_new_thread( print_time, ("Thread-1", 2, ) )
#   _thread.start_new_thread( print_time, ("Thread-2", 4, ) )
#except:
import paramiko
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

def main():
    A=AnScan(low_channel=0,high_channel=15,rat=15000,samples=(15000*16))
    j=0
    plotting=False
    k=0
    while(k<1000):
        j=0
        while(j<3):
            R=A.doScan(i=j)
            print("len is",len(R[0]))
            print("A rate is",A.rate)
            x=[]
            i=0
          
            if(plotting):
                while(i<len(R[0])):
                    x.append(i/(A.rate))
                    i=i+1
                
            
                plt.plot(x,R[0])
                plt.plot(x,R[1])
                plt.plot(x,R[8])
                plt.show()
            else:
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
                    #subprocess.run(["scp", filename, "novello@10.100.16.101:/home/novello/lab/plot "])
                    #pyjson2.TestParameterWr(filename,NomeTest,data,Articolo,Nodo,DescrizIngresso,BitQuant,NumeroCiclo,Banda,Fc,NumeroCampioni,Errori,Dati=R[kk])
                    print("filename is ",filename)
                    copy_file("10.100.16.40", 22, "lab01", "novello", filename, "/home/lab01/Test1/AS000TST/"+nomefile)
                    i=i+1
                f.close()
            j=j+1
                
        k=k+1
    return
     
if __name__ == '__main__':
    main()
    
