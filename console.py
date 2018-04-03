# Class for taking console input from user without blocking execution
# Found implementation found here: https://stackoverflow.com/questions/2408560/python-nonblocking-console-input

import sys
import select
import tty
import termios


class console(object):

    def __enter__(self):
        self.old_settings = termios.tcgetattr(sys.stdin)
        tty.setcbreak(sys.stdin.fileno())

    def __exit__(self, type_, value, traceback):
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self.old_settings)

    @staticmethod
    def get_data():
        if select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], []):
            return sys.stdin.readline().rstrip()
        return False



# Example:
# with NonBlockingConsole() as nbc:
#     i = 0
#     while 1:
#         print i
#         i += 1
#         if nbc.get_data() == '\x1b':  # x1b is ESC
#             break
#
# import time
# con = console()
# while True:
#     time.sleep(0.1)
#     d = con.get_data()
#     if d:
#         print(d)
#     if d == 'w':
#         print('up')
#     elif d == 's':
#         print('down')
#     elif d == 'a':
#         print('right')
#     elif d == 'd':
#         print('left')
