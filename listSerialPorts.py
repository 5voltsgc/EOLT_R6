import serial.tools.list_ports
import serial
# import time

windowsPort = "COM1"
ports = list(serial.tools.list_ports.comports())

for port in ports:
    # print(p)
    if "Arduino" in port.description:
        # print("This is an Arduino!")
        windowsPort = port.name

arduino = serial.Serial(windowsPort, baudrate=9600, timeout=.1)
while True:
    num = input("Enter a number: ")  # Taking input from user
    arduino.write(bytes(num, 'utf-8'))
