import time
from com_messages import rc


from state_template import AEVCState

import teensy_talker as teensy
import seer


returnMessages = []


def execute(rm):
    returnMessages.extend('k')
    if rm:
        returnMessages.extend(rm)


class Initialize(AEVCState):

    def on_event(self, event):
        execute(teensy.enable())
        time.sleep(1)
        execute(teensy.home())
        return Idle()


class Idle(AEVCState):
    def on_event(self, event):
        if event is 'd':
            return Detecting()
        if event is 'm':
            return Manual()


class Sleep(AEVCState):
    def on_entry(self):
        execute(teensy.disable())

    def on_event(self, event):
        if event is 'a':
            return Initialize()


# Manual Control

class Manual(AEVCState):

    # In this state we are not requiring one command to be completed before
    # the next is initialized, but we still want to keep track

    def on_event(self, event):

        command, value = event

        if command is rc.forward:
            execute(teensy.move_forward(value))

        elif command is rc.spin:
            execute(teensy.spin(value))

        elif command is rc.spinBody:
            execute(teensy.spin_body(value))

        elif command is rc.spinBase:
            execute(teensy.spin_base(value))

        elif command is rc.height:
            execute(teensy.height(value))


# Automated workflow states:

class Detecting(AEVCState):
    def on_event(self, event):
        # Take picture, see if port there,
        #  - return centering if detected
        #  - loop otherwise

        if seer.port_present():
            return Centering()
        else:
            return self


class Centering(AEVCState):

    lastControlVariable = None

    phiErrorLimit = 1  # degree
    xError = 0.005     # m
    yError = 0.005     # m
    zError = 0.005     # m
    yDistance = 2      # m
    roughYError = 0.5  # m

    # Mapping relative position from camera and LIDAR distance information to robot motion.
    #
    # Order of precedence for motion:
    #  - rotation (phi) (AEVC facing vehicle straight)
    #  - height (camera on level with port)
    #  - y position (approximately far enough away so as not to collide)
    #  - x position (centered in front of vehicle port)
    #  - y position (precise positioning in front of port)
    #
    # All quantities but x position is known fully, but the sign for x-position is ambiguous.
    # Therefore, we need to implement a strategy in which two data-points are collected in order
    # to assertion whether we need to move left or right in order to get in front of the port.

    def on_event(self, event):

        if not seer.port_present():
            print("Cannot find port.")
            return Detecting()

        x, y, z, phi = seer.pos_from_image(seer.image_name)

        if abs(phi) > self.phiErrorLimit:
            execute(teensy.spin(phi))

        elif abs(z) > self.zError:
            execute(teensy.height(-z))

        elif abs(y-self.yDistance) > self.roughYError:
            execute(teensy.move_forward(y - self.yDistance))

        elif abs(x) > self.xError:
            execute(teensy.spin_base(-90))
            time.sleep(1)
            execute(teensy.move_forward(x))

            # TODO: better motion, ascertain sign of x error

        elif abs(y - self.yDistance) > self.yError:
            execute(teensy.move_forward(y - self.yDistance))


class Approaching(AEVCState):
    def on_event(self, event):
        pass


class Connecting(AEVCState):
    def on_event(self, event):
        pass


class Connected(AEVCState):
    def on_event(self, event):
        pass


class Disconnecting(AEVCState):
    def on_event(self, event):
        pass


class Returning(AEVCState):
    def on_event(self, event):
        pass
