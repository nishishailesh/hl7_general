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
    #self.write_set.add(self.conn[0])                      #Add in write set, for next select() to make it writable
    #self.error_set=self.read_set.union(self.write_set)    #update error set
    #demo reply for apple and pineapple, use socat - tcp:127.0.0.1:2576
    print_to_log("hl7::manage_read():",data)
    self.write_msg=data[0:5]

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
      #self.write_set.remove(self.conn[0])                   #now no message pending, so remove it from write set
      #self.error_set=self.read_set.union(self.write_set)    #update error set


  def signal_handler(self,signal, frame):
    print_to_log('Alarm Stopped','Signal:{} Frame:{}'.format(signal,frame))
    print_to_log('Alarm..response NOT received in stipulated time','data receving/sending may be incomplate')

if __name__=='__main__':
  logging.basicConfig(filename=conf.log_filename,level=logging.DEBUG,format='%(asctime)s : %(message)s') 

  print('__name__ is ',__name__,',so running code')
  while True:
    m=hl7(conf.host_address,conf.host_port,conf.select_timeout,5)
    m.loop()
    #break; #useful during debugging



