
import serial
import time
import datetime
import csv

ser = serial.Serial('COM27')
fileName = ("EOLT-" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S") +
            ".csv")

ser.flushInput()
while True:
    try:
        ser_bytes = ser.readline()
        print(ser_bytes)

        with open(fileName, "a", newline='') as f:
            writer = csv.writer(f, delimiter=",")
            writer.writerow([time.time(), ser_bytes])

    except KeyboardInterrupt:
        print("Keyboard interrupt exception caught")
        break
