import serial
import sys

port = serial.Serial("/dev/ttyS0", baudrate=9600, timeout=3.0)



port.write(str.encode('light_on\n'))
rcv = port.readline()
print (rcv)
port.write(str.encode('pump_on\n'))
rcv = port.readline()
print (rcv)
port.write(str.encode('light_off\n'))
rcv = port.readline()
print (rcv)
port.write(str.encode('light\n'))
rcv = port.readline()
print (rcv)
port.write(str.encode('moisture\n'))
rcv = port.readline()
print (rcv)
