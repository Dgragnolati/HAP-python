import serial

port = serial.Serial("/dev/ttyS0", baudrate=9600, timeout=3.0)

rcv = port.read(10)
print (rcv)

while True:
    port.write('start\n')
    rcv = port.read(10)
    print (rcv)
