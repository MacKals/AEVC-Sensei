from states import AEVCState
import time
from enum import Enum, auto

import teensy_talker as teensy
import positionFromImage as vision


returnMessages = {}

def execute(rm):
    returnMessages.extend(rm)

class Initialize(AEVCState):

    def on_event(self, event):
        execute(teensy.enable())
        time.sleep(0.5)
        execute(teensy.home())
        return UnlockedState()


class Idle(AEVCState):
    def on_event(self, event):
        if event is "a":
            return Detecting

class Sleep(AEVCState):
    def on_entry(self, event):
        event(teensy.disable())

    def on_event(self, event):
        if event is "a":
            return Initialize


### Manual Control

class RC(Enum):
    forward = auto()
    turn = auto()
    turnBody = auto()
    turnBase = auto()
    height = auto()

class Manual(AEVCState):

    # In this state we are not requiring one command to be completed before
    # the next is initialized, but we still want to keep track

    def on_event(self, event):

        command, value = event

        if command is RC.forward:
            execute(teensy.moveForward(value))

        elif command is RC.turn:
            execute(teensy.turn(value))

        elif command is RC.turnBody:
            execute(teensy.turnBody(value))

        elif command is RC.turnBase:
            execute(teensy.turnBase(value))

        elif command is RC.height:
            execute(teensy.height(value))



### Automated workflow states:

class Detecting(AEVCState):
    def on_event(self, event):
        ## Take picture, see if port there,
        ##  - return centering if detected
        ##  - loop otherwise

        if vision.portPresent():
            return Centering
        else:
            return self


class Centering(AEVCState):

    lastControlVariable = None

    phiErrorLimit = 1 // degree
    xError = 0.005 // m
    yError = 0.005 // m
    zError = 0.005 // m
    yDistance = 2          // m
    roughYError = 0.5   // m

    # Mapping relative position from camera and lidar distance information to robot motion.
    #
    # Order of presidence for motion:
    #  - rotation (phi) (AEVC facing vehicle straight)
    #  - height (camera on level with port)
    #  - y position (approximatley far enough away so as not to collide)
    #  - x position (centerd in front of vehicle port)
    #  - y positoin (presice positioning in fornt of port)
    #
    # All quantaties but x position is known fully, but the sign for x-position is ambigous. Therefore, we need to implement a strategy in which two data-points are collected in order to assertain whether we need to move left or right in order to get in front of the port.
    #
    def on_event(self, event):
        if not vision.portPresent():
            print "Cannot find port."
            return Detecting

        x, y, z, phi = pos.posFromImage(imageName)

        if (abs(phi) > phiErrorLimit):
            execute(teensy.turn(phi))

        elif (abs(z) > zError):
            execute(teensy.height(-z))

        elif (abs(y-yDistance) > roughYError):
            execute(teensy.moveForward(y-yDistance))

        elif (abs(x) > xError):
            execute(teensy.turnBase(-90))
            time.sleep(1)
            execute(teensy.moveForward(x))

            #TODO: better motion, ascertain sign of x error

        elif (abs(y-yDistance) > yError):
            execute(teensy.moveForward(y-yDistance))


class Approaching(AEVCState):
    def on_event(self, event):

class Connecting(AEVCState):
    def on_event(self, event):

class Connected(AEVCState):
    def on_event(self, event):

class Disconnecting(AEVCState):
    def on_event(self, event):

class Returning(AEVCState):
    def on_event(self, event):
