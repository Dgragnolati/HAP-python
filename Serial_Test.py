import serial

port = serial.Serial("/dev/ttyS0", baudrate=9600, timeout=3.0)

rcv = port.read("17")
print (rcv)

while True:
    port.write(str.encode('start\n'))
    rcv = port.read(10)
    print (rcv)
    command=raw_input("Enter Command")
    command_newline=command+\n'
    port.write(str.encode('command_newline'))
