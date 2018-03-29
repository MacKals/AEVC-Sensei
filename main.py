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

from NonBlockingConsole import NonBlockingConsole as console
import teensy_talker as teensy
import XBoxController as rc

import machine

from queue import queue


# async collector of info and placing it in queue

from multiprocessing import Process

q = queue()
m = machine()

def dequeue():
    while True:
        if not q.isEmpty():
            r = m.event(queue.pop())
            if r:
                q.push(r)

info('main line')
p = Process(target=dequeue, args=())
p.start()


def readFromTerminal():
    return console.get_data()

def readFromRC():
    return None # TODO: get data!

def readFromTeensy():
    return teensy.readLine()

def push(arg):
    if arg is not None:
        q.push(arg)

while True:
    push(readFromTerminal())
    push(readFromRC)
    push(readFromTeensy())
