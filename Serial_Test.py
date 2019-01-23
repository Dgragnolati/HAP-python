import serial
import sys

port = serial.Serial("/dev/ttyS0", baudrate=9600, timeout=3.0)

rcv = port.read(17)
print (rcv)
print ("Requesting a Start")
port.write(str.encode('start\n'))
rcv = port.read(22)
port.write(str.encode('light_on\n'))
rcv = port.read(4)
port.write(str.encode('pump_on\n'))
rcv = port.read(4)
port.write(str.encode('light_off\n'))
rcv = port.read(4)
port.write(str.encode('light\n'))
rcv = port.read(4)
port.write(str.encode('moisture\n'))
rcv = port.read(4)
