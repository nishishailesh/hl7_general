#!/usr/bin/python3

import socket,time, signal
TCP_IP = '127.0.0.1'
TCP_PORT = 2575
BUFFER_SIZE = 1024

def signal_handler(signal, frame):
  print('signal_handler() is called')
   
def read_input():
  data=input('0. Exit\
  1. Send hello message\
  2.send hl7 message')
  return data
  
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
s.setblocking(0)    
    
while True:
  received_data=''
  data=read_input()
  if(data=='1'):
    MESSAGE=b'Hellow world'
  elif(data=='2'):
    MESSAGE=b"\x0bMSH|^~\&|ADT1|MCM|FINGER|MCM|198808181126|SECURITY|ADT^A01|MSG00001|P|2.3.1\x0dPID|1||PATID1234^5^M11^ADT1^MR^MCM~123456789^^^USSSA^SS||\x1c\x0d"
  elif(data=='0'):
    s.close()
    quit()
  s.send(MESSAGE)
  time.sleep(1)
  try:
    received_data = s.recv(BUFFER_SIZE)
    print ("((((received data:))))", received_data)
  except Exception as my_ex:
    print ("((((received data:))))", "NOTHING")

