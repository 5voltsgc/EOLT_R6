# https://towardsdatascience.com/do-not-use-print-for-debugging-in-python-anymore-6767b6f1866d
from icecream import ic
from datetime import datetime
ic.disable()
ic.enable()

def now():
    return f'[{datetime.now()}] '

ic.configureOutput(prefix=now)
# ic('test')

my_dict = {
    'name': 'Chris',
    'age': 33
}

def square_of(num):
    return num * num

print(square_of(2))
print(square_of(3))
print(square_of(4))

print('square of 2:', square_of(2))
print('square of 3:', square_of(3))
print('square of 4:', square_of(4))

ic(square_of(2))
ic(square_of(3))
ic(square_of(4))

ic(my_dict['name'])

class Dog():
    num_legs = 4
    tail = True
    nose = "cold"

dog = Dog()

ic(dog.num_legs)
ic(dog.tail)
ic(dog.nose)
print(dog.tail)

user_name = "Chris"

if user_name == "Chris":
    ic()
else:
    ic()

def check_user(username):
    if username == 'Chris':
        # do something
        ic()
    else:
        # do something else
        ic()
check_user('Chris')
check_user('Jade')

num = 2
square_of_num = square_of(ic(num))

if ic(square_of_num) == pow(num, 2):
    ic('Correct!')
