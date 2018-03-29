## AEVC Controller Main
# Coordinates data-streams from user and microcontroller with sensor information
# to determine state and actions to send.
#
# Structure:
# - Two event-streams:
#   - user input
#   - teensy serial
# - Events placed in priority queue
#   - user events have higher priority
#   - statemachine may block events with output
# - Coordinator in main
#   - handles event-streams (places all input in queue)
#   - pops events from queue and sends to state machine

import Queue
from multiprocessing import Process

from console import NonBlockingConsole as console
import teensy_talker as teensy
import xbox
import machine


# async collector of info and placing it in queue

q = queue()
m = machine.AEVC()

def dequeue():
    while True:
        if not q.isEmpty():
            r = m.event(queue.pop())
            if r:
                q.push(r)

info('main line')
p = Process(target=deque, args=())
p.start()


def read_from_terminal():
    return console.get_data()

def read_from_xbox():
    return None # TODO: get data!

def read_from_teensy():
    return teensy.read_line()

def push(arg):
    if arg is not None:
        q.push(arg)

while True:
    push(readFromTerminal())
    push(readFromXbox)
    push(readFromTeensy())
