import time
import threading


def hello():
    time.sleep(4)
    print("hello, world")


t = threading.Timer(15, hello)
t.start()

var = input("Please enter a string:\n")
if var == 'something':
    print('cancelled')
    t.cancel()
