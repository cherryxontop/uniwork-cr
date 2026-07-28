#---------------------
# #ex 1
r = 5
pi = 3.14

v = 4/3*pi*r**2
print(f"volume of sphere =", v)
print("volume of spehere with radius: " + str(r) + " is " + str(v))

#---------------------
# ex 2
print("what are you doing?")
task = input()

print("enter % complete")
percent = input()

progress_bar = '---------'

print("loading " + task + " ...: " + percent)
print("["+progress_bar+"] " + percent + "%")

#update
filled = 20 * (float(percent)/100)
unfilled = 20 - filled
progress_bar = '#' * int(filled) + '.' * int(unfilled)

print("loading " + task + " ...: " + percent)
print("["+progress_bar+"] " + percent + "%")

#---------------------
# ex 3: importing libraries
import math
print("pi= ", math.pi)

# but i like numpy so
import numpy as np
print("pi= ", np.pi)


#---------------------
# ex 4: defining functions
def change_in_percent(old, new):
    diff = new - old
    return (diff/old)*100
