
import xbox
from com_messages import Commands


class RemoteController(object):

    def __init__(self, joystick_array):

        self.joystick_array = joystick_array

        self.j = xbox.Joystick()
        self.lastCommand = None

    # Priority reading from buttons, as they should never be pressed simultaniously with motion.
    # When doing multiple identical items, it is ok to queue them up.
    # When transitioning from one command to another, it is important that the last command in sompleted before the new is
    # initiated for most combinations of commands

    def read_command(self):

        new_command = self.command()
        if new_command is self.lastCommand:
            return None
        self.lastCommand = new_command
        return new_command

    def command(self):
        # update joystick motion
        self.store_drive_action()

        if self.j.B():
            return Commands.disable
        if self.j.Y():
            return Commands.stop
        if self.j.A():
            return Commands.manual
        if self.j.X():
            return Commands.connect
        if self.j.Start():
            return Commands.init
        if self.j.Back():
            return Commands.to_home_position
        if self.j.dpadLeft():
            return Commands.base_to_left
        if self.j.dpadRight():
            return Commands.base_to_right
        if self.j.dpadUp():
            return Commands.base_to_front
        if self.j.dpadDown():
            return Commands.base_to_back

        return None

    def store_drive_action(self):

        x, y = self.j.leftStick(2*4000)

        # Scale down input
        x = 0.3 * x
        y = 0.3 * y

        left = y + x
        right = y - x

        self.joystick_array[0] = left
        self.joystick_array[1] = right

        theta, h = self.j.rightStick(2*4000)

        # Scale down input
        theta = 0.4 * theta
        h = 0.8 * h
        self.joystick_array[2] = theta
        self.joystick_array[3] = h


    # def turn_action(self):
    #
    #     x = j.rightX()
    #     y = j.rightY()
    #
    #     left = y + x
    #     right = y - x
    #
    #     return left, right


    #while True:
    #    c = read_command()
    #    if c:
    #        print(c)
    #    left, right = drive_action()
    #    print(str(left) + " " + str(right))

