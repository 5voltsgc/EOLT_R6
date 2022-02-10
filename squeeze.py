from random import random
from timeit import repeat
from tkinter import font

from cv2 import CAP_MSMF
from guizero import App, Text, PushButton, TextBox, info
from matplotlib.pyplot import text, title
import numpy as np
from time import sleep, strftime
from datetime import datetime
from random import randint
current_limit = 0.13
failed = False
prox_retract = True
prox_extend = False
valve_extend = False
cycles = 0
def monitor_dmm():
    set_current_txt.value = str(randint(45, 55))

def get_file_name():
    current_datetime = datetime.now().strftime("%Y_%m_%d-%I_%M_%S_%p")
    filename = "Squeeze_" + str(current_datetime) + ".csv"
    return filename

def start_test():

    global cycles
    cycles = 0
    state = start_button.text
    if state == "Pause":
        start_button.text = "Start"
    else:
        start_button.text = "Pause"
    set_baseline.disable()

def stop():
    # Not sure I need this button
    stop_test = app.yesno("Stop Test?", "Do you want to stop the test?")
    if stop_test is True:
        print("Test has stopped")
        start_button.text = "Start"

    else:
        print("The test is continuing")


def test_loop():
    testing = start_button.text
    global failed
    global prox_extend
    global prox_retract
    global cycles
    global valve_extend
    global current_limit

    if testing == "Pause" and failed is False:
        print("testing loop")
        # check the state of the cylinder, and switch
        if valve_extend is True & prox_extend is True:
            # the cylinder and the air valve are correct
            prox_extend = False
            prox_retract = True
            valve_extend = False
            print("extend cylinder")

        elif valve_extend is False & prox_extend is False:
            # the cylinder and the air valve are correct
            prox_extend = True
            prox_retract = False
            valve_extend = True
            print("Retract cylinder")

        else:
            print("In the wrong state error")

        # Check DMM
        dmm_read = 0.503456433224  # "float(my_instrument.read_bytes(15))" # my_instrument.write('MEAS:CURR? 1')
        curnt_msrmt = randint(45, 55)
        current_current_txt.value = curnt_msrmt
        dmm_set_current = float(set_current_txt.value)
        current_diff_txt.value = dmm_set_current - curnt_msrmt
        current_limit = 0.13
        cycles = cycles + 1
        cycles_txt.value = cycles

        if current_limit < (dmm_read - dmm_set_current):
            print(f"test sample has failed at {cycles} squeezes")
            failed = True 

uut_filename = get_file_name()
app = App(layout="grid", width=900, height=650, title="Technology Realization: Squeeze-O-Matic")
app.repeat(500, test_loop)
sample_name_lbl = Text(app, grid=[0, 0], text="Sample Name:")
sample_name_lbl.text_size = 20
sample_name_txt = TextBox(app, grid=[1, 0])
sample_name_txt.text_size = 20
file_name_lbl = Text(app, grid=[2, 0], text="   File Name:")
file_name_lbl.text_size = 12
file_name_txt = Text(app, grid=[3, 0], text=uut_filename)
file_name_txt.text_size = 10

set_current_lbl = Text(app, grid=[0, 2], text="Baseline set at (mA):")
set_current_lbl.text_size = 20
set_current_txt = TextBox(app, grid=[1, 2], text="50mA")
set_current_txt.text_size = 20
set_baseline = PushButton(app, grid=[2, 2], text="Set Baseline", command=monitor_dmm)


start_button = PushButton(app, grid=[0, 5], text="Start", command=start_test)
start_button.text_size = 20
stop_button = PushButton(app, grid=[1, 5], text="Stop", command=stop)
stop_button.text_size = 20
results_lbl = Text(app, grid=[0, 6], text="Results:")
results_lbl.text_size = 20
cycles_lbl = Text(app, grid=[0, 7], text="Cycles:")
cycles_lbl.text_size = 20
cycles_txt = Text(app, grid=[1, 7], text="0")
cycles_txt.text_size = 20
current_currnet_lbl = Text(app, grid=[0, 8], text="Measured Current:")
current_currnet_lbl.text_size = 20
current_current_txt = Text(app, grid=[1, 8], text="0")
current_current_txt.text_size = 20
current_diff_lbl = Text(app, grid=[0, 9], text="Difference:")
current_diff_lbl.text_size = 20
current_diff_txt = Text(app, grid=[1, 9], text="0")
current_diff_txt.text_size = 20
lmt = f" < {current_limit}"
current_limit_lbl = Text(app, grid=[2, 9], text=lmt)
current_limit_lbl.text_size = 20

app.display()
