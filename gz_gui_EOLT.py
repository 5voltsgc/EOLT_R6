from guizero import App, Text, TextBox, Combo, PushButton, Box, Picture
import numpy as np
import csv

item_numbers = np.array([[107287,8,2,4,1,0,204109,124458],
                        [107297,8,2,4,1,0,204109,124458],
                        [108144,8,2,4,1,0,204109,124458],
                        [108150,8,2,4,1,0,204109,124458],
                        [108283,18,6,3,0,1,204109,124458],
                        [112497,6,2,3,1,0,301404,124734],
                        [121248,12,3,4,1,0,301393,124393],
                        [121250,18,6,3,0,1,301400,124394],
                        [121334,15,5,3,0,1,301401,124742],
                        [121335,15,5,3,0,1,301401,124740],
                        [121791,12,6,2,0,1,301400,124394]])
    
print(item_numbers)
# Create the item numbers for the Combobox
items =[]
for column in item_numbers:
    items.append(column[0])
print(items)

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

users = []
# if file missing got error FileNotFoundError: [Errno 2] No such file or directory: 'users.csv'
with open('Users.csv', newline='') as FR:
    reader = csv.reader(FR, delimiter =',')
    # this brings in a list of list of names as such [["John"], ["Julie"]]
    for row in reader:
        users.append(row)
    # but I only want only a list as such ["John", "Julie"]
    # So this will flatten the list
    print(f"unsorted:{users}")
    users = flatten_list(users)
    # sort the list of names alphabetically with sorted()
    users=sorted(users)
    print(users)

def double_click():
    print("Double Clicked")
    
#     name = app.question("Hello", "What name do you want to add to the list?")
#     # If cancel is pressed, None is returned
#     # so check a name was entered
#     if name is not None:
#         print(name)
#         users.append(str(name))
#     with open("Users.csv", 'w', newline='') as f:
#         writer = csv.writer(f)
#         writer.writerow([users])

def update_harnes_fixture_lbl():
    print(selected_item.value)
    item_num_indx = items.index(int(selected_item.value))
    harness = str(item_numbers[item_num_indx][6])
    fixture = str(item_numbers[item_num_indx][7])
    use_harness.value = harness
    use_fixture.value = fixture
    save_btn.enabled=True
    tst_btn.enabled = True

    
def save_test():
    print("Save Test")

def begin_test():
    print("begin test")
    
def plot_noise():
    print("Noise Plot")

def plot_counts():
    print("plot_counts")



app = App(layout="grid", title = "EOLT", width = 1500, height = 650)
button_box=Box(app, layout="grid",  grid=[0, 0, 3, 6], border=2)

# Item Numbers
itm_num_lbl = Text(button_box, text="1. Choose - Item Number:", size=20, grid=[0,1], align="left")
selected_item = Combo(button_box, grid=[1, 1, 2, 1], width=15, options=items, command=update_harnes_fixture_lbl)
selected_item.text_size=20
# Serial Numbers
serial_label = Text(button_box, text="2. Enter - Serial Number:", size=20, grid=[0,2], align="left")
serial_num_txtbox = TextBox(button_box, grid=[1, 2, 2, 1], width=17, command=update_harnes_fixture_lbl)
serial_num_txtbox.text_size = 20
# User 
user_lbl = Text(button_box,text="3. Select - User:", size=20, grid=[0, 3], align="left" )
user_lbl.when_double_clicked = double_click
user_name_cmb = Combo(button_box,options=users, grid=[1,3, 2, 1], align="left", width=15)
user_name_cmb.text_size=20
# Use fixture and harness
harness_lbl = Text(button_box, text="4. Use Harness:", size=20, grid=[0, 4], align="left")
use_harness = TextBox(button_box, enabled=True, width=17, grid=[1, 4, 2, 1])
use_harness.text_size=20
use_harness.bg = "#999999"
fixture_lbl = Text(button_box, text="5. Use Fixture:", size=20, grid=[0,5], align="left")
use_fixture = TextBox(button_box, enabled=True, width=17, grid=[1, 5, 2, 1])
use_fixture.bg = "#999999"
use_fixture.text_size=20
# Buttons
tst_btn = PushButton(button_box, command=begin_test, text = "6. Begin Test", grid=[0,6])
tst_btn.text_size = 30
tst_btn.enabled = False
save_btn = PushButton(button_box, command=save_test, text = "7. Save Test", grid=[1,6])
save_btn.text_size = 30
save_btn.enabled = False
graph_box = Box(app, layout="grid", grid=[6,0,6,6], border=2)
noise_btn = PushButton(graph_box, command=plot_noise, image="Noise_400x300.png", grid=[0,0])
counts_btn = PushButton(graph_box, command=plot_counts, image="Counts_400x300.png", grid=[1,0])

results_box = Box(app, layout='grid', grid=[0,6, 7,6], border=2)
results_lbl = Text(results_box, grid=[0,0], text="Test Results: Passed")
results_lbl.text_size = 30
results_lbl.bg='green'

# make a multiline test from list
fill = ""
for l in item_numbers:
    fill += str(l) +"\n"
    

result_txtbox=TextBox(results_box, grid=[0,1], text=fill, align="left", multiline=True, scrollbar=True)
result_txtbox.height = 15
result_txtbox.width = 175

app.display()

