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

from console import console
import teensy_talker as teensy
import xbox


# async collector of info and placing it in queue

print("Starting")


user_queue = Queue()
teensy_queue = Queue()

m = AEVC()


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


def read_from_xbox():
    return None  # TODO: get data!


def read_from_teensy():
    return teensy.read_line()


def user_push(arg):
    if arg is not None and arg is not False:
        arg = arg.rstrip()
        user_queue.put(arg)


def teensy_push(arg):
    if arg:
        print(arg)
        teensy_queue.put(arg)
        print(teensy_queue.qsize())


print("Into loop")
m.user_event('s')

while True:

    user_push(read_from_terminal())
    teensy_push(read_from_teensy())

    # push(read_from_xbox())
