
import xbox
from com_messages import Commands

j = xbox.Joystick()

# Priority reading from buttons, as they should never be pressed simultaniously with motion.
# When doing multiple identical items, it is ok to queue them up.
# When transitioning from one command to another, it is important that the last command in sompleted before the new is
# initiated for most combinations of commands


def joysick_action(amount):
    if abs(amount) < 0.3:
        return 0
    elif amount < 0:
        return -1
    else:
        return 1


lastCommand = None


def read_command():
    global lastCommand
    new_command = command()
    if new_command is lastCommand:
        return None
    lastCommand = new_command
    return new_command


def command():

    if j.B():
        return Commands.disable
    if j.Y():
        return Commands.stop
    if j.A():
        return Commands.default
    if j.X():
        return Commands.connect
    if j.Start():
        return Commands.init

    return None


def drive_action():

    x = j.leftX()
    y = j.leftY()

    left = y + x
    right = y - x

    return left, right


def turn_action():

    x = j.rightX()
    y = j.rightY()

    left = y + x
    right = y - x

    return left, right


# while True:
#     print(command())

