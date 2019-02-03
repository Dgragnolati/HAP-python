import serial
import sys

port = serial.Serial("/dev/ttyS0", baudrate=9600, timeout=3.0)




port.write(str.encode('light\n'))
rcv = port.readline()

print (str(rcv)[-4])
