import time
from com_messages import Commands

from state_template import AEVCState

import teensy_talker as teensy
#import seer

joystickArray = None
returnMessages = []


def execute(rm):
    returnMessages.extend('k')
    if rm:
        returnMessages.extend(rm)


class Initialize(AEVCState):
    def on_entry(self):
        execute(teensy.enable())
        time.sleep(1)
        execute(teensy.home())

    def on_event(self, event):
        return Idle()


class Idle(AEVCState):
    def on_entry(self):
        execute(teensy.move_forward(0))

    def on_event(self, event):
        if event is Commands.connect:
            return Detecting()
        if event is Commands.manual:
            return Manual()
        if event is Commands.disable:
            return Sleep()
        if event is Commands.init:
            return Initialize()


class Sleep(AEVCState):
    def on_entry(self):
        execute(teensy.disable())

    def on_event(self, event):
        if event is Commands.init:
            return Initialize()
        if event is Commands.manual:
            return Manual()


# Manual Control

class Manual(AEVCState):

    # In this state we are not requiring one command to be completed before
    # the next is initialized, but we still want to keep track
    def on_entry(self):
        teensy.set_velocity(0, 0, 0, 0)

    def on_event(self, event):
        
        if event is Commands.connect:
            return Detecting()
        if event is Commands.stop:
            return Idle()
        if event is Commands.disable:
            return Sleep()
        if event is Commands.to_home_position:
            teensy.home_to_home_position()
        if event is Commands.init:
            return Initialize()

    def tick(self):
        left = joystickArray[0]
        right = joystickArray[1]
        theta = joystickArray[2]
        h = joystickArray[3]
        teensy.set_velocity(left, right, theta, h)

    def on_exit(self):
        teensy.set_velocity(0, 0, 0, 0)


# Automated workflow states:

class Detecting(AEVCState):
    def on_event(self, event):
        # Take picture, see if port there,
        #  - return centering if detected
        #  - loop otherwise
        pass
        #if seer.port_present():
        #    return Centering()
        #else:
        #    return self


# class Centering(AEVCState):
#
#     lastControlVariable = None
#
#     phiErrorLimit = 1  # degree
#     xError = 0.005     # m
#     yError = 0.005     # m
#     zError = 0.005     # m
#     yDistance = 2      # m
#     roughYError = 0.5  # m
#
#     # Mapping relative position from camera and LIDAR distance information to robot motion.
#     #
#     # Order of precedence for motion:
#     #  - rotation (phi) (AEVC facing vehicle straight)
#     #  - height (camera on level with port)
#     #  - y position (approximately far enough away so as not to collide)
#     #  - x position (centered in front of vehicle port)
#     #  - y position (precise positioning in front of port)
#     #
#     # All quantities but x position is known fully, but the sign for x-position is ambiguous.
#     # Therefore, we need to implement a strategy in which two data-points are collected in order
#     # to assertion whether we need to move left or right in order to get in front of the port.
#
#     def on_event(self, event):
#
#         if not seer.port_present():
#             print("Cannot find port.")
#             return Detecting()
#
#         x, y, z, phi = seer.pos_from_image(seer.image_name)
#
#         if abs(phi) > self.phiErrorLimit:
#             execute(teensy.spin(phi))
#
#         elif abs(z) > self.zError:
#             execute(teensy.height(-z))
#
#         elif abs(y-self.yDistance) > self.roughYError:
#             execute(teensy.move_forward(y - self.yDistance))
#
#         elif abs(x) > self.xError:
#             execute(teensy.spin_base(-90))
#             time.sleep(1)
#             execute(teensy.move_forward(x))
#
#             # TODO: better motion, ascertain sign of x error
#
#         elif abs(y - self.yDistance) > self.yError:
#             execute(teensy.move_forward(y - self.yDistance))
#
#
# class Approaching(AEVCState):
#     def on_event(self, event):
#         pass
#
#
# class Connecting(AEVCState):
#     def on_event(self, event):
#         pass
#
#
# class Connected(AEVCState):
#     def on_event(self, event):
#         pass
#
#
# class Disconnecting(AEVCState):
#     def on_event(self, event):
#         pass
#
#
# class Returning(AEVCState):
#     def on_event(self, event):
#         pass
