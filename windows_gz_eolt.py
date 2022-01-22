import csv
from guizero import App, Text, TextBox, Combo, PushButton, Box
import numpy as np
from time import sleep, strftime
from datetime import datetime
# import RPi.GPIO as GPIO
# import board
# import busio
# import adafruit_ads1x15.ads1015 as ADS
# from adafruit_ads1x15.analog_in import AnalogIn
from fpdf import FPDF
import matplotlib.pyplot as plt
import pandas as pd
import random
from PIL import Image
import os
# Create the I2C bus
# i2c = busio.I2C(board.SCL, board.SDA)

# Create the ADC object using the I2C bus
# ads = ADS.ADS1015(i2c)
# Stepper Motor and Sensor head GPIO addresses
DIR = 27   # Direction GPIO Pin
STEP = 17  # Step GPIO Pin
CW = 1     # Clockwise Rotation Plate towards home
CCW = 0    # Counterclockwise Rotation Plate away from home
ENB = 22   # the enable pin - this pin is inverted
head_select_0 = 23
head_select_1 = 24
head_select_2 = 25
head_select_3 = 12
#Set up the analog to digital pins
# ads0 = AnalogIn(ads, ADS.P0)
# ads1 = AnalogIn(ads, ADS.P1)
# ads2 = AnalogIn(ads, ADS.P2)
# ads3 = AnalogIn(ads, ADS.P3)

# GPIO.setmode(GPIO.BCM)
# GPIO.setup(head_select_0, GPIO.OUT)
# GPIO.setup(head_select_1, GPIO.OUT)
# GPIO.setup(head_select_2, GPIO.OUT)
# GPIO.setup(head_select_3, GPIO.OUT)
# GPIO.setup(STEP, GPIO.OUT)
# GPIO.setup(DIR, GPIO.OUT)
# GPIO.output(DIR, CW)
# GPIO.setup(5, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Set pin 5 to be an input pin and set initial value to be pulled low (off)
# GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Set pin 21 to be an input pin and set initial value to be pulled low (off)

# Initiallizing the Home Switch on pin 5
# pin5 = GPIO.input(5)

# pin21 = GPIO.input(21) # to be used for the power down Raspberry Pi

# GPIO.setup(ENB, GPIO.OUT)
# HALLS = 6
# HEADS = 3
delay = .015
readings_table = []
plotlegend = [] 
users=[] # list to hold users - purhapse will change to Dictionary to make easier to add
item_num_indx = 0 # used as a global index for which test
noise_readings = 100 # how many readings for the noise check
count_readings = 350 # how many steps and readings for counts check
start_position = 500
item_numbers = np.array([])
items = []
test_fixture = "A" #a unique identify for which machine this is when we have three there will be A, B & C

def load_item_numbers():
    global item_numbers
    # global items
    # Item number column headers
    # 0-Part Numbers,
    # 1-Count Halls,
    # 2-halls/head,
    # 3-# heads,
    # 4-Selected,
    # 5-addressed,
    # 6-highMax,
    # 7-highMin,
    # 8-lowMax,
    # 9-lowMin,
    # 10-diffMax,
    # 11-diffmin
    # 12-Harness item number
    # 13-Fixture item number
    # 14-Noise Threshold
    item_numbers = np.array([[107287,8,2,4,1,0,1000,700,-600,-900,1000,-50,204109,124458,200],
                            [107297,8,2,4,1,0,1000,700,-600,-900,818,560,204109,124458,200],
                            [108144,8,2,4,1,0,1000,700,-600,-900,1000,-50,204109,124458,200],
                            [108150,8,2,4,1,0,1000,700,-600,-900,885,654,204109,124458,200],
                            [112497,6,2,3,1,0,1000,700,-600,-900,1000,-50,301404,124734,200],
                            [121248,12,3,4,1,0,1000,700,-600,-900,728,460,301393,124393,200],
                            [121250,18,6,3,0,1,1000,700,-600,-900,14000,8000,301400,124394,200],
                            [121334,15,5,3,0,1,1000,700,-600,-900,1000,-50,301401,124742,200],
                            [121335,15,5,3,0,1,1000,700,-600,-900,1000,-50,301401,124740,200],
                            [121791,12,6,2,0,1,1000,700,-600,-900,1000,-50,301400,124394,200]])

    # print(item_numbers)
    # Create the item numbers for the Combobox
    for column in item_numbers:
        items.append(column[0])
    # print(items)

def flatten_list(_2d_list):
    flat_list = []
    # Iterate through the outer list
    for element in _2d_list:
        if type(element) is list:
            # If the element is of type list, iterate through the sublist
            for item in element:
                flat_list.append(item)
        else:
            flat_list.append(element)  
    return flat_list

def load_users():
    """Open the users.csv file and reads into a list for the options dropdown"""
    global users
    with open('Users.csv', newline='', encoding='utf-8-sig') as FR:    
        reader = csv.reader(FR, delimiter =',')
        users = list(reader)
        # print(users)
        users = flatten_list(users)
        users=sorted(users)
#         print(users)
    return

def home():
    # enable the stepper motor control - don't leave on since the motor heats up
    # GPIO.output(ENB, True)
    # GPIO.output(DIR, CW) #Set dir of travel towards home switch
    # Read current state of home sensor
    # home_sensor = GPIO.input(5)
#     print("Homing plate")
    # while home_sensor == 0:
    #     GPIO.output(STEP, GPIO.HIGH)
    #     sleep(delay)
    #     GPIO.output(STEP, GPIO.LOW)
    #     home_sensor = GPIO.input(5)
    return

def rapid_start_pos():    
# rapid move to starting
    # GPIO.output(DIR, CCW) # Set dir of travel away home switch
    # for _ in range(500):
    #     GPIO.output(STEP, GPIO.HIGH)
    #     sleep(delay/10)
    #     GPIO.output(STEP, GPIO.LOW)
    # print('Rapid move to start postion')
    return


def selected_read_all_halls(heads, halls_per_head):
    # TODO
    # print(" you selected a selected type sensor set but the function has not been created")
    total_halls = heads * halls_per_head
    selected = []
    for _ in range(total_halls):
        selected.append(random.randint(8000,8005))    

    return selected

def addressed_read_all_halls(heads, halls_per_head):
    """Function to read a addressed type sensor set, like SMFL
        input is= heads, halls per head
        output is a list of values of heads * halls_per_head length
        this is not an actual funtion as it needs to run on rpi hardware"""
    
    hall_readings = []
    for i in range(heads):
        for j in range(halls_per_head):
            hall_readings.append(random.randint(8000, 8005))
  
    return hall_readings

def double_click():
    print("Double Clicked")
    global users
    name = app.question("Hello", "What name do you want to add to the list? (note: please restart program to load new name)")
    # If cancel is pressed, None is returned
    # so check a name was entered
    if name is not None:
        print(name)
        users.insert(len(users), name)
        print(users)
        users=sorted(users)
    with open("Users.csv", 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.writer(f)
        writer.writerows([users])
    # user_name_cmb.options=users  #can't do this?

# def create_pdf():
    
    # pdf report
    

def update_harnes_fixture_lbl():
    # print(selected_item.value)
    indx = items.index(int(selected_item.value))
    harness = str(item_numbers[indx][12])
    fixture = str(item_numbers[indx][13])
    use_harness.value = harness
    use_fixture.value = fixture
    tst_btn.enabled = True
    #remove any illigel characters for file names and make upper case
    # initializing bad_chars_list
    bad_chars = [';', ':', '!', "*", "[", "]", "=", "$", "!", "@", "#", "&", "^", "%"]
    original_text = serial_num_txtbox.value
    corrected_text = ''.join(i for i in original_text if not i in bad_chars).upper()
    serial_num_txtbox.value = corrected_text
 
def save_test():
    print("Save Test")

def begin_test():
    # print("begin test")

    # TODO set Neopixels white
    home()
    rapid_start_pos()

#     Obtain the data needed for the test

    uut_index = items.index(int(selected_item.value))
    uut_itemnumber = item_numbers[uut_index][0]
    uut_heads = item_numbers[uut_index][3]
    uut_halls_per_head = item_numbers[uut_index][2]
    uut_total_halls = uut_halls_per_head * uut_heads
    uut_selected = item_numbers[uut_index][4]
    uut_user = user_name_cmb.value #String
    uut_serial_num = serial_num_txtbox.value
    uut_plotlegend = []
    uut_noise_threshold = item_numbers[uut_index][14]
    uut_max_diff = item_numbers[uut_index][10]
    uut_min_diff = item_numbers[uut_index][11]
    
    for h in range(uut_halls_per_head * uut_heads):
        uut_plotlegend.append("hall: "+ str(h))
    
    current_datetime = datetime.now().strftime("%Y_%m_%d-%I_%M_%S_%p")
    str_current_datetime = str(current_datetime)
    uut_filename = str(uut_itemnumber) + "_" + uut_serial_num + "_" + str_current_datetime + test_fixture

#   print(uut_plotlegend)
    
    #prime ads sensor by calling it once without doing anything with the returned list
    addressed_read_all_halls(uut_heads, uut_halls_per_head)
    
    uut_noise=[]
    # Noise Check
    for n in range(noise_readings):
        if uut_selected:
            uut_noise.append(selected_read_all_halls(uut_heads, uut_halls_per_head))
        else:
            uut_noise.append(addressed_read_all_halls(uut_heads, uut_halls_per_head))
            
#     print(f"the current reading list has rows: {len(uut_noise)}")
#     print(f"the current reading list has columns: {len(uut_noise[0])}")
    noise_df = pd.DataFrame(uut_noise, columns = uut_plotlegend)
    noise_df.to_csv("noise.csv", index = True)
    results = noise_df.iloc[:, 0:(uut_total_halls)].diff(axis=0, periods = 1).abs().max().to_frame()
    results.columns = ['noise']
    results = results.assign(noise_result = results.loc[:,'noise'] < uut_noise_threshold)
    results['Noise_Threshold'] = uut_noise_threshold


    
    # Counts Check create a list to put all readings until last step
    uut_counts = []
    # GPIO.output(DIR, CCW) 
    for n in range(count_readings):
        if uut_selected:
            uut_counts.append(selected_read_all_halls(uut_heads, uut_halls_per_head))
        else:
            uut_counts.append(addressed_read_all_halls(uut_heads, uut_halls_per_head))
        # Move one step
        # GPIO.output(STEP, GPIO.HIGH)
        # sleep(delay/10)
        # GPIO.output(STEP, GPIO.LOW)

        
# return home
    # GPIO.output(DIR, CW)    
    # for r in range(count_readings + start_position):
    #     GPIO.output(STEP, GPIO.HIGH)
    #     sleep(delay/10)
    #     GPIO.output(STEP, GPIO.LOW)
    # #     sleep(delay/5)
    #     step = int(60-round(r/18,0))
    #     print(step)

    # GPIO.output(ENB, False)
    # GPIO.cleanup()
 
    counts_df = pd.DataFrame(uut_counts, columns = uut_plotlegend)
    # print(counts_df.max())
    results = results.assign(count_max = counts_df.max())
    results = results.assign(count_min = counts_df.min())
    results['count_diff'] = results['count_max']-results['count_min']
    results['count_results'] = results['count_diff'].between(uut_min_diff, uut_max_diff)
    results['Target_Max'] = uut_max_diff
    results['Target_Min'] = uut_min_diff
    # print(results)

    save_btn.enabled = True
# create counts plot
    plt.plot(uut_counts)
    # plt.legend(plotlegend,loc='upper left')
    plt.xlabel('Steps')
    plt.ylabel('Counts')
    counts_plt_fn = str(uut_filename) + "_counts.png"
    plt.savefig(counts_plt_fn)
    im = Image.open(counts_plt_fn)
    size=(400,300)
    out = im.resize(size)
    out.save(counts_plt_fn)

# create noise plot
    a_threshold = np.maximum(results["noise"] - uut_noise_threshold, 0)
    b_threshold = np.minimum(results["noise"], uut_noise_threshold)
    x = range(uut_total_halls)
    fig, ax = plt.subplots()
    ax.bar(x, b_threshold, 0.35, color="green")
    ax.bar(x, a_threshold, 0.35, color="red", bottom=b_threshold)
    plt.axhline(uut_noise_threshold, color='red', ls='dotted')
    noise_plt_fn = str(uut_filename) + "_noise.png"
    plt.savefig(noise_plt_fn)
    im = Image.open(noise_plt_fn)
    size=(400,300)
    out = im.resize(size)
    out.save(noise_plt_fn)
    
    # Update GUI
    noise_btn.image = noise_plt_fn
    counts_btn.image = counts_plt_fn
    pf_noise = results["noise_result"].all()
    pf_counts = results["count_results"].all()
#     print(f"the pass fail results for noise is: {pf_noise}")
#     print(f"the pass fail results for counts is: {pf_counts}")
    
    result_txtbox.value = str(results)
    
    uut_results = "N/a"
    if pf_counts and pf_noise:
        results_lbl.bg='green'
        results_lbl.value = 'Test Results: Passed'
        uut_results = "Pass"

    else:
        results_lbl.bg='red'
        results_lbl.value = 'Test Results: Failed'
        uut_results = "Fail"

    # create PDF report
    pdf = FPDF('P', 'mm', 'letter')
    pdf.add_page()
    pdf.image('tdw-LOGO.PNG', x=0, y = 0, w = 30, h = 30, type = 'PNG' )
    pdf.set_font('helvetica', 'B', 35)
    pdf.text(40, 25, "End of Line Test Report")
    pdf.image(noise_plt_fn, x = 0, y = 55, w = 97, h = 82, type = 'PNG')
    pdf.image(counts_plt_fn, x = 100, y = 55, w = 97, h = 82, type = 'PNG')
    pdf.set_font('helvetica', 'B', 16)
    
    pdf.set_line_width(0.5)
    pdf.set_draw_color(r=0, g=0, b=0)
    pdf.line(x1=8, y1=42, x2=200, y2=42)
    pdf.line(x1=8, y1=56, x2=200, y2=56)

    line1 = "Item #: " + str(uut_itemnumber) + "     Serial #: " + str(uut_serial_num) + "     User: " + uut_user
    pdf.text(8, 40, line1)
    line2 = "Date/ID: " + current_datetime +"_" + test_fixture + "     Result: " + uut_results
    pdf.text(8,54, line2)

    lst_results = results.values.tolist()
    

    pdf.line(x1=8, y1=140, x2=200, y2=140)
    pdf.text(8,146, "Results Table:")
    pdf.set_font('helvetica','B', 12)    
    pdf.text(8, 152, " 1. Noise, 2. Noise Result 3. Max 4. Min 5. Diff 6. Diff Result 7. Diff Max 8. Diff Min")
    pdf.set_font('helvetica','', 12)  
    y = 158
    for i in range(uut_total_halls):
        t = "Hall: " + str(i) + " - " + str(lst_results[i])
        pdf.text(8, y, t)
        y = y + 6

    # pdf.text(8, 152, str(item_numbers[0]))
    # pdf.text(8, 156, str(item_numbers[1]))
    pdf_filename = uut_filename + ".pdf" # for some reason it doesn't add the extension
#     print(f"Printed PDF with filename: {pdf_filename}")
    pdf.output(uut_filename)
    os.rename(uut_filename, pdf_filename)

def plot_noise():
    print("Noise Plot")

def plot_counts():
    print("plot_counts")

load_item_numbers()
load_users()

app = App(layout="grid", title = "EOLT", width = 1500, height = 650)
button_box=Box(app, layout="grid",  grid=[0, 0, 3, 6], border=3)

# Item Numbers
itm_num_lbl = Text(button_box, text="1. Choose - Item Number:", size=20, grid=[0,1], align="left")
selected_item = Combo(button_box, grid=[1, 1, 2, 1], width=15, options=items, command=update_harnes_fixture_lbl)
selected_item.text_size=20
# Serial Numbers
serial_label = Text(button_box, text="2. Enter - Serial Number:", size=20, grid=[0,2], align="left")
serial_num_txtbox = TextBox(button_box, grid=[1, 2, 2, 1], width=17, command=update_harnes_fixture_lbl)
serial_num_txtbox.value = "B00000"
serial_num_txtbox.text_size = 20
# User 
user_lbl = Text(button_box,text="3. Select - User:", size=20, grid=[0, 3], align="left" )
user_lbl.when_double_clicked = double_click
user_name_cmb = Combo(button_box,options=users, grid=[1,3, 2, 1], align="left", width=25)
user_name_cmb.text_size=12
# Use fixture and harness
harness_lbl = Text(button_box, text="4. Use Harness:", size=20, grid=[0, 4], align="left")
use_harness = TextBox(button_box, enabled=True, width=17, grid=[1, 4, 2, 1])
use_harness.text_size=20
use_harness.bg = (192,192,192)
fixture_lbl = Text(button_box, text="5. Use Fixture:", size=20, grid=[0,5], align="left")
use_fixture = TextBox(button_box, enabled=True, width=17, grid=[1, 5, 2, 1])
use_fixture.bg = (192,192,192) #"FFFDF5"
use_fixture.text_size=20
# Buttons
tst_btn = PushButton(button_box, command=begin_test, text = "6. Begin Test", grid=[0,6])
tst_btn.text_size = 30
tst_btn.enabled = False
save_btn = PushButton(button_box, command=save_test, text = "7. Save Test", grid=[1,6])
save_btn.text_size = 30
save_btn.enabled = False
graph_box = Box(app, layout="grid", grid=[6,0,6,6], border=3)
noise_btn = PushButton(graph_box, command=plot_noise, image="Noise_400x300.png", grid=[0,0])
counts_btn = PushButton(graph_box, command=plot_counts, image="Counts_400x300.png", grid=[1,0])

results_box = Box(app, layout='grid', grid=[0,6, 7,6], border=3)
results_lbl = Text(results_box, grid=[0,0], text="Test Results: N/a")
results_lbl.text_size = 30
# results_lbl.bg='green'

result_txtbox=TextBox(results_box, grid=[0,1], text="", align="left", multiline=True, scrollbar=True)
result_txtbox.height = 15
result_txtbox.width = 175
# for l in item_numbers:
#     result_txtbox.append(l)
    
app.display()