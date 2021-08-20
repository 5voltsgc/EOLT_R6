import sys
import time
import serial
import matplotlib.pyplot as plt

def getdata():
    arduino.write(str.encode("getdata?\n"))
    resposta=arduino.readline()
    decoded_bytes = str(resposta[0:len(resposta)-2].decode("utf-8"))
    resposta=decoded_bytes
    #print (resposta)
    return resposta

plt.ion()
plt.xlabel('Time (sec)')
plt.ylabel('Temperature (deg C)')
arduino = serial.Serial('/dev/ttyUSB0',9600,timeout=2)
tempo_total=100
intervalo_tempo=3
relogio_start = time.time()
relogio_final = relogio_start + tempo_total
now=time.time()
i=0
while (now < relogio_final):
    if (now > relogio_start+(intervalo_tempo*i)):
        data_collected=getdata()
        tempo_now = (time.time()-relogio_start)
        data_to_save=str(tempo_now) + "," + data_collected
        #print (data_to_save)
        data=data_to_save.split(',')
        plt.plot(float(data[0]),float(data[1]), 'og')
        plt.show
        plt.pause(0.0001)
        i = i + 1
        now=time.time()