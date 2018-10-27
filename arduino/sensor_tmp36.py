#!/usr/bin/python3
#-*-coding: utf-8-*-

import serial
import re


def readSerialPort(): 
   ser = serial.Serial('/dev/ttyACM0', 9600, 8, 'N', 1, timeout=10)
   output = ser.readline()
   b = bytearray(output)
   return b.decode()


def getTemp(unit="F"):
   temps = re.compile('\d+\.\d+')
   st = temps.findall(readSerialPort())
   if st and len(st)>2:
      if unit=="F":  
         return st[2]
      elif len(st)>1:
         return st[1]
   return

   
def testHarness():
   while True:
      print(readSerialPort())
      print('{} F'.format(getTemp()))
      print('{} C'.format(getTemp("C")))

