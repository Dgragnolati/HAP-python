import serial
import sys

port = serial.Serial("/dev/ttyS0", baudrate=9600, timeout=3.0)

rcv = port.read(17)
print (rcv)
print ("Requesting a Start")
port.write(str.encode('start\n'))
rcv = port.read(22)

while True:
    command=input("Enter Command")
    command_newline=str(command)+'\n'
    port.write(str.encode('command_newline'))
    rcv = port.read(1)
    print (rcv)
