
import tkinter as tk
from tkinter.ttk import Combobox
from PIL import Image, ImageTk
import numpy as np
from tkinter.font import Font
from time import sleep
import RPi.GPIO as GPIO
import board
import busio
import adafruit_ads1x15.ads1015 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

from fpdf import FPDF
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

window = tk.Tk()
window.title('EOLT')
# window.iconbitmap('TDWicon2.ico')
window.geometry('1400x600')
myFont = Font(family="Times New Roman", size=12)

# test Varibles held in a list
UUT_config = []
HALLS = 6
HEADS = 3
# Create the I2C bus
i2c = busio.I2C(board.SCL, board.SDA)

# Create the ADC object using the I2C bus
ads = ADS.ADS1015(i2c)

DIR = 27   # Direction GPIO Pin
STEP = 17  # Step GPIO Pin
CW = 1     # Clockwise Rotation Plate towards home
CCW = 0    # Counterclockwise Rotation Plate away from home
ENB = 22   # the enable pin - this pin is inverted
head_select_0 = 23
head_select_1 = 24
head_select_2 = 25
head_select_3 = 12

ads0 = AnalogIn(ads, ADS.P0)
ads1 = AnalogIn(ads, ADS.P1)
ads2 = AnalogIn(ads, ADS.P2)
ads3 = AnalogIn(ads, ADS.P3)


GPIO.setmode(GPIO.BCM)
GPIO.setup(head_select_0, GPIO.OUT)
GPIO.setup(head_select_1, GPIO.OUT)
GPIO.setup(head_select_2, GPIO.OUT)
GPIO.setup(head_select_3, GPIO.OUT)
GPIO.setup(STEP, GPIO.OUT)
GPIO.setup(DIR, GPIO.OUT)
GPIO.output(DIR, CW)
GPIO.setup(5, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Set pin 5 to be an input pin and set initial value to be pulled low (off)
GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Set pin 21 to be an input pin and set initial value to be pulled low (off)
pin5 = GPIO.input(5)
pin21 = GPIO.input(21)
GPIO.setup(ENB, GPIO.OUT)
HALLS = 6
HEADS = 3
delay = .015
readings_table = []
plotlegend = []
# ##################################################################
# ###################TESTING########################################
# ##################################################################



def addressed_read_all_halls():
    
    
    hall_readings = []
    
#     print("heads: " + str(HEADS))
#     print("heads: " + str(HALLS))
    for i in range(HEADS):
        for j in range(HALLS):
            addressed_hall_number = i * HALLS + j
            
            if j == 0:
#                 print("Hall_0")
                GPIO.output(head_select_0, GPIO.LOW)
                GPIO.output(head_select_1, GPIO.LOW)
                GPIO.output(head_select_2, GPIO.LOW)
                GPIO.output(head_select_3, GPIO.LOW)
            elif j == 1:
#                 print("Hall_1")
                GPIO.output(head_select_0, GPIO.HIGH)
                GPIO.output(head_select_1, GPIO.LOW)
                GPIO.output(head_select_2, GPIO.LOW)
                GPIO.output(head_select_3, GPIO.LOW)
                
            elif j == 2:
#                 print("Hall_2")
                GPIO.output(head_select_0, GPIO.LOW)
                GPIO.output(head_select_1, GPIO.HIGH)
                GPIO.output(head_select_2, GPIO.LOW)
                GPIO.output(head_select_3, GPIO.LOW)
            elif j == 3:
#                 print("Hall_3")
                GPIO.output(head_select_0, GPIO.HIGH)
                GPIO.output(head_select_1, GPIO.HIGH)
                GPIO.output(head_select_2, GPIO.LOW)
                GPIO.output(head_select_3, GPIO.LOW)
            elif j == 4:
#                 print("Hall_4")
                GPIO.output(head_select_0, GPIO.LOW)
                GPIO.output(head_select_1, GPIO.LOW)
                GPIO.output(head_select_2, GPIO.HIGH)
                GPIO.output(head_select_3, GPIO.LOW)
            else:
#       import csv           print("Hall_5")
                GPIO.output(head_select_0, GPIO.HIGH)
                GPIO.output(head_select_1, GPIO.LOW)
                GPIO.output(head_select_2, GPIO.HIGH)
                GPIO.output(head_select_3, GPIO.LOW)
            
            if i == 0:
#                 print("0 - Hall Number: " + str(addressed_hall_number))
                hall_readings.append(ads0.value)
                
            elif i == 1:
#                 print("1 - Hall Number: " + str(addressed_hall_number))
                hall_readings.append(ads1.value)
                
            elif i == 2:
#                 print("2 - Hall Number: " + str(addressed_hall_number))
                hall_readings.append(ads2.value)
            
            else:
#                 print("3 - Hall Number: " + str(addressed_hall_number))
                hall_readings.append(ads3.value)
     
#     print(hall_readings)
    return(hall_readings)

def testing():

    

    for h in range(HALLS * HEADS):
        plotlegend.append("hall: "+ str(h))


    noise_readings = 100 # how many readings for the noise check
    #Move plate to Home position while the button is not pressed
    GPIO.output(ENB, True)
    pin5 = 0
    while pin5 == 0:
       
        GPIO.output(STEP, GPIO.HIGH)
        sleep(delay)
        GPIO.output(STEP, GPIO.LOW)
        pin5 = GPIO.input(5)

    # rapid move to starting
    GPIO.output(DIR, CCW)
    for s in range(500):
        GPIO.output(STEP, GPIO.HIGH)
        sleep(delay/10)
        GPIO.output(STEP, GPIO.LOW)


    #Read sesnors once to prime, or noise reduction, of the ADS1X15 sensor
    addressed_read_all_halls()

    # Noise Check
    for n in range(noise_readings):
        readings_table.append(addressed_read_all_halls())

    # testing steps
    for s in range(1100-500):
        GPIO.output(STEP, GPIO.HIGH)
        sleep(delay/10)
        GPIO.output(STEP, GPIO.LOW)
    #     sleep(delay/5)
        step = int(round(s/18,0))    
    #     print(s)
        
        readings_table.append(addressed_read_all_halls())

    # print(readings_table)
    df = pd.DataFrame(readings_table)
    noise_results = df.iloc[:noise_readings, 0:((HALLS * HEADS))].diff(axis=0, periods = 1).abs().max().to_frame()
    noise_results.columns = ['Noise']
    noise_results["Halls"] = plotlegend
    noise_results.to_csv('noise_results.csv', sep=',')

    GPIO.output(DIR, CW)    
    for r in range(1100):
        GPIO.output(STEP, GPIO.HIGH)
        sleep(delay/10)
        GPIO.output(STEP, GPIO.LOW)
        step = int(60-round(r/18,0))  

    GPIO.output(ENB, False)
    GPIO.cleanup()

    plt.plot(readings_table)
    plt.rcParams["figure.figsize"] = [4.00, 3.00]
    plt.xlabel('Steps')
    plt.ylabel('Counts')
    plt.savefig('Counts_400x300.png')

    #https://www.tutorialspoint.com/how-to-create-a-matplotlib-bar-chart-with-a-threshold-line
    plt.rcParams["figure.figsize"] = [4.00, 3.00]
    threshold = 200

    a_threshold = np.maximum(noise_results["Noise"] - threshold, 0)
    b_threshold = np.minimum(noise_results["Noise"], threshold)
    x = range(HALLS * HEADS)
    print(x)
    fig, ax = plt.subplots()
    ax.bar(x, b_threshold, 0.35, color="green")
    ax.bar(x, a_threshold, 0.35, color="red", bottom=b_threshold)
    plt.axhline(threshold, color='red', ls='dotted')
    plt.savefig('Noise_400x300.png')
    


    pdf = FPDF('P', 'mm', 'letter')
    pdf.add_page()
    pdf.image('EOLT_report.png', x = 0, y = 0, w = 203, h = 279, type = 'PNG')
    pdf.image('Noise.png', x = 0, y = 55, w = 97, h = 82, type = 'PNG')
    pdf.image('Counts.png', x = 100, y = 55, w = 97, h = 82, type = 'PNG')
    pdf.set_font('helvetica', 'B', 16)
    pdf.text(23, 40, '121250')
    pdf.text(23, 51.5, 'January 3, 2022')
    pdf.text(127, 40, 'B12345')
    pdf.text(127, 51.5, '01032022r12m3')

    results = noise_results[['Halls', 'Noise']]
    print("The results were:")
    print(type(results))
    print(results)
    pdf.ln(10)
    pdf.write(5, str(results))
    pdf.output('tuto1.pdf', 'F')
    



def comboclick(event):
    index = items.index(int(drop_item_number.get()))
    global UUT_config
    UUT_config = item_numbers[index]
    print(UUT_config)
    lbl_fixtures.config(text=UUT_config[6])
    txt_harn = "f-" + str(UUT_config[6])
    lbl_harness.config(text=txt_harn)
    # The command buttons active only after chooseing an Item Number
    btn_begin.config(state=tk.NORMAL)
    btn_save.config(state=tk.NORMAL)
    btn_print.config(state=tk.NORMAL)


def test():
    print("Begin testing loop")
    print(UUT_config)
    testing()
    counts_chart_large = ImageTk.PhotoImage(Image.open('Counts_400x300.png'))
    counts_btn.config(image=counts_chart_large)
    # update charts on buttons
    noise_chart_large = ImageTk.PhotoImage(Image.open('Noise_400x300.png'))
    noise_btn.config(image=noise_chart_large)

def save_results():
    # print("save results was clicked")
    print(drop_item_number.get())
    print(item_numbers[:, 0])
    # print(f.index(121250))

def print_results():
    print('Print results was clicked')
    # lbl_fixtures.config(text = str(selected_item_number))

item_numbers = np.array([[107287, 8, 2, 4, 1, 0, 12345],
                        [107297, 8, 2, 4, 1, 0, 23456],
                        [108144, 8, 2, 4, 1, 0, 34567],
                        [108150, 8, 2, 4, 1, 0, 45677],
                        [108283, 18, 6, 3, 0, 1, 76543],
                        [112497, 6, 2, 3, 1, 0, 865324],
                        [121248, 12, 3, 4, 1, 0, 7654367],
                        [121250, 18, 6, 3, 0, 1, 6543456],
                        [121334, 15, 5, 3, 0, 1, 6543234],
                        [121335, 15, 5, 3, 0, 1, 876765],
                        [121791, 12, 6, 2, 0, 1, 5643322]])

# Create the item numbers for the Combobox
items =[]
for column in item_numbers:
    items.append(column[0])

selected_item_number = tk.IntVar()
selected_item_number.set(121250)

# input frame
input_frame = tk.Frame(window, width=100, highlightbackground='blue', highlightthickness=3)

# input_frame=Frame(window, width=100, highlightbackground='blue', highlightthickness=3)
input_frame.grid(row=0, column=0, padx=20, pady=20, ipadx=20, ipady=20)

# ItemNumbers
tk.Label(input_frame, text='Item Number #:', fg='blue', font=myFont, foreground="black").grid(row=0, column=0, sticky=tk.E)
# drop_item_number = tk.OptionMenu(input_frame, selected_item_number, * item_numbers)

# ComboBox
drop_item_number = Combobox(input_frame, 
values=items, 
state='readonly', 
width=8, 
font=myFont,
foreground="black"
)
drop_item_number.bind("<<ComboboxSelected>>", comboclick)

drop_item_number.grid(row=0, column=1, columnspan=2, sticky=tk.W)

# Serial Number
tk.Label(input_frame, text='Serial #:', fg='black', font=myFont).grid(row=1, column=0, sticky=tk.E)

ent_serial_num = tk.Entry(input_frame, textvariable=selected_item_number, fg='black', font=myFont, width=10)
ent_serial_num.grid(row=1, column=1, columnspan=2, sticky=tk.W)

# Harness and Fixture
tk.Label(input_frame, text='Use Harness:', fg='black', font=myFont).grid(row=2, column=0, sticky=tk.E)
lbl_harness = tk.Label(input_frame, text=str(selected_item_number.get()), fg='black', font=myFont)
lbl_harness.grid(row=2, column=1, sticky=tk.E)
tk.Label(input_frame, text='Use Fixture:', fg='black', font=myFont).grid(row=3, column=0, sticky=tk.E)
lbl_fixtures = tk.Label(input_frame, text=str(selected_item_number.get()), fg='black', font=myFont)
lbl_fixtures.grid(row=3, column=1, sticky=tk.E)

# Buttons
btn_begin = tk.Button(input_frame, command=test, text='Begin\nTest', fg='blue', font=myFont, state=tk.DISABLED)
btn_begin.grid(row=4, column=0, sticky=tk.E)
btn_save = tk.Button(input_frame, command=save_results, text='Save\nresults', fg='blue', font=myFont, state=tk.DISABLED)
btn_save.grid(row=4, column=1, sticky=tk.W)
btn_print = tk.Button(input_frame, command=print_results, text='Print\nResults', fg='blue', font=myFont, state=tk.DISABLED)
btn_print.grid(row=4, column=2, sticky=tk.W)

# Chart frame
noise_frame = tk.Frame(window, width=100, highlightbackground='blue', highlightthickness=3)
noise_frame.grid(row=0, column=1, padx=20, pady=20, ipadx=20, ipady=20)
noise_chart_large = ImageTk.PhotoImage(Image.open('Noise_400x300.png'))
counts_chart = ImageTk.PhotoImage(Image.open('Counts_400x300.png'))
noise_btn = tk.Button(noise_frame, text="open plot", image=noise_chart_large).pack(side=tk.LEFT)
counts_btn = tk.Button(noise_frame, text="open plot", image=counts_chart).pack(side=tk.RIGHT)

window.mainloop()

