#!/usr/bin/python3
import sys,time, logging, socket, select, os, signal
import bidirectional_general_conf as conf
from bidirectional_general import bdg, print_to_log

def print_to_log(object1,object2):
  logging.debug('{} {}'.format(object1,object2))
  
class hl7(bdg):
  
  def __init__(self,host_address,host_port,select_timeout,alarm_time):
    super().__init__(host_address,host_port,select_timeout)
    self.alarm_time=alarm_time
    signal.signal(signal.SIGALRM, self.signal_handler)

  def manage_read(self,data):
    print_to_log("hl7::manage_read():",data)
    if(self.is_received_data_MLLP(data)):
      self.write_msg=b'Received data is MLLP'
    else:
      self.write_msg=b'Error: >>>>Received data is NOT MLLP'
    print_to_log('hl7::manage_read(): sending...',self.write_msg)       

  def manage_write(self):
    print_to_log('hl7::manage_write():','I am called by loop()')       
    #Send message in response to write_set->select->writable initiated by manage_read() and initiate_write()
    if(len(self.write_msg)>0):
      print_to_log('hl7::manage_write():Following will be sent',self.write_msg) 
      try:
        self.conn[0].send(self.write_msg)
        self.write_msg='' #not in astm. because status 
      except Exception as my_ex :
        print_to_log("Disconnection from client?",my_ex)                    

  def signal_handler(self,signal, frame):
    print_to_log('Alarm Stopped','Signal:{} Frame:{}'.format(signal,frame))
    print_to_log('Alarm..response NOT received in stipulated time','data receving/sending may be incomplate')


  def is_received_data_MLLP(self,data):
    #MESSAGE=b"\x0bMSH|^~\&|ADT1|MCM|FINGER|MCM|198808181126|SECURITY|ADT^A01|MSG00001|P|2.3.1\x0dPID|1||PATID1234^5^M11^ADT1^MR^MCM~123456789^^^USSSA^SS||\x1c\x0d"
    start_byte=data[0:1]
    end_bytes=data[len(data)-2:]
    print_to_log(b"required start byte is \x0b , data start bye is:",start_byte)
    print_to_log(b"required two end bytes are \x1c\x0d , data end two byes are is:",end_bytes)
    if((start_byte,end_bytes)==(b'\x0b',b'\x1c\x0d')):
      print_to_log((start_byte,end_bytes) , (start_byte,end_bytes))
      return True
    return False

    
if __name__=='__main__':
  logging.basicConfig(filename=conf.log_filename,level=logging.DEBUG,format='%(asctime)s : %(message)s') 

  print('__name__ is ',__name__,',so running code')
  while True:
    m=hl7(conf.host_address,conf.host_port,conf.select_timeout,5)
    m.loop()
    #break; #useful during debugging



