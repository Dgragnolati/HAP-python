import serial
import sys

port = serial.Serial("/dev/ttyS0", baudrate=9600, timeout=3.0)


def send_command(command):
    #self.blocking=1
    command_string=command+'\n'
    port.write(str.encode(command_string))
    rcv = port.readline()
    port.flushInput()
    #self.blocking=0
    return int(rcv.decode('utf-8'))

print(send_command("light"))
