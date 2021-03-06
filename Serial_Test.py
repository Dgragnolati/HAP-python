import serial
import sys
from time import sleep

port = serial.Serial("/dev/ttyS0", baudrate=9600, timeout=6.0)


def send_command(command):
    #self.blocking=1
    command_string=command+'\n'
    port.write(str.encode(command_string))
    rcv = port.readline()
    port.flushInput()
    #self.blocking=0
    return int(rcv.decode('utf-8'))


print ("Light On")
print(send_command("light_on"))
sleep(1)
print ("Pump On")
print(send_command("pump_on"))
sleep(1)
print ("Moisture Value")
print(send_command("moisture"))
sleep(1)
print ("Light Value")
print(send_command("light"))
sleep(1)
print ("Light Off")
print(send_command("light_off"))
