#!/usr/bin/python3
import sys,time, logging, socket, select, os
import bidirectional_general_conf as conf
from bidirectional_general import bdg

def print_to_log(object1,object2):
  logging.debug('{} {}'.format(object1,object2))
  
class hl7(bdg):
  def manage_read(self,data):
    self.write_set.add(self.conn[0])                      #Add in write set, for next select() to make it writable
    self.error_set=self.read_set.union(self.write_set)    #update error set
    #demo reply for apple and pineapple, use socat - tcp:127.0.0.1:2576
    if(data==b'pineapple\n'):
      self.write_msg=b'Demo manage_read() override me. \033[1;33mpinapple is yellow\033[0m\n'  
    if(data==b'apple\n'):
      self.write_msg=b'Demo manage_read() override me. \033[1;31mapple is Red\033[0m\n' 
    if(data==b'mango\n'):
      self.write_msg=b'Demo manage_read() override me. \033[1;32mmango is Red\033[0m\n'   


if __name__=='__main__':
  logging.basicConfig(filename=conf.log_filename,level=logging.DEBUG,format='%(asctime)s : %(message)s') 

  print('__name__ is ',__name__,',so running code')
  while True:
    m=hl7(conf.host_address,conf.host_port,conf.select_timeout)
    m.loop()
    #break; #useful during debugging
