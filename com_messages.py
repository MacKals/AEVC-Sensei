from enum import Enum


class Control(Enum):
    forward = 0
    spin = 1
    spinBody = 2
    spinBase = 3
    height = 4


class Commands(Enum):
    disable = 'b'
    stop = 'y'
    init = 's'
    connect = 'x'
    manual = 'a'
    to_home_position = 'h'
