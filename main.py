# AEVC Controller Main
# Coordinates data-streams from user and microcontroller with sensor information
# to determine state and actions to send.
#
# Structure:
# - Two event-streams:
#   - user input
#   - Teensy serial
# - Events placed in priority queue
#   - user events have higher priority
#   - state-machine may block events with output
# - Coordinator in main
#   - handles event-streams (places all input in queue)
#   - pops events from queue and sends to state machine

from multiprocessing import Process, Queue, Array
import time

from machine import AEVC

from console import console
import teensy_talker as teensy
from remote_controller import RemoteController

# async collector of info and placing it in queue

direct_queue = Queue()
user_queue = Queue()
teensy_queue = Queue()

m = AEVC()

joystickArray = Array('d', [0.0] * 4)
xbox = RemoteController(joystickArray)


def dequeue(ja):

    m.set_joystick_array(ja)

    wait_time = time.time() + 2
    manual_refresh_rate = 15
    manual_refrash_delay = 1.0 / manual_refresh_rate

    while True:

        if not direct_queue.empty():
            a = direct_queue.get()
            print(a)
            m.direct_event(a)

        if not user_queue.empty():
            a = user_queue.get()
            print(a)
            m.user_event(a)

        if not teensy_queue.empty():
            a = teensy_queue.get()
            print(a)
            r = m.teensy_event(a)
            if r:
                teensy_queue.put(r)

        if wait_time < time.time():
            wait_time = time.time() + manual_refrash_delay
            m.timer_event()


p = Process(target=dequeue, args=(joystickArray, ))
p.start()


def read_from_terminal():
    return console.get_data()


def read_from_xbox():
    return xbox.read_command()


def read_from_teensy():
    return teensy.read_line()


def terminal_push(arg):
    if arg:
        direct_queue.put(arg)


def user_push(arg):
    if arg:
        user_queue.put(arg)


def teensy_push(arg):
    if arg:
        print(arg)
        arg = arg[0]
        teensy_queue.put(arg)


while True:
    teensy_push(read_from_teensy())
    user_push(read_from_xbox())
    terminal_push(read_from_terminal())
