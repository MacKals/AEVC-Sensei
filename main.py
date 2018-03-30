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

from multiprocessing import Process, Queue

from machine import AEVC
from com_messages import rc

from console import console
import teensy_talker as teensy
import xbox


# async collector of info and placing it in queue

user_queue = Queue()
teensy_queue = Queue()

m = AEVC()
j = xbox.Joystick()


def dequeue():
    while True:
        if not user_queue.empty():
            a = user_queue.get()
            print(a)
            r = m.user_event(a)
            if r:
                user_queue.put(r)

        if not teensy_queue.empty():
            a = teensy_queue.get()
            print(a)
            r = m.teensy_event(a)
            if r:
                teensy_queue.put(r)


p = Process(target=dequeue, args=())
p.start()


def read_from_terminal():
    return console.get_data()


def joysick_action(amount):
    if abs(amount) < 0.3:
        return 0
    elif amount < 0:
        return -1
    else:
        return 1


def read_from_xbox():

    if j.B():
        return 'q'
    if j.Y():
        return 'h'
    if j.A():
        return 'm'
    if j.Start():
        return 'a'

    lx = joysick_action(j.leftX())
    ly = joysick_action(j.leftY())
    rx = joysick_action(j.rightX())
    ry = joysick_action(j.rightY())

    if lx:
        return rc.spin, lx
    if ly:
        return rc.forward, ly
    if rx:
        return rc.spinBase, rx
    if ry:
        return rc.height, ry


def read_from_teensy():
    return teensy.read_line()


def user_push(arg):
    if arg is not None and arg is not False:
        arg = arg.rstrip()
        user_queue.put(arg)


def teensy_push(arg):
    if arg:
        arg = arg[0]
        print(arg)
        teensy_queue.put(arg)
        print(teensy_queue.qsize())


while True:
    teensy_push(read_from_teensy())

    user_push(read_from_terminal())
    user_push(read_from_xbox())
