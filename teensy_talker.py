import serial

port = serial.Serial("/dev/ttyACM0", baudrate=115200, timeout=3.0)

def read_line():
    if port.inWaiting:
        return port.readline
    return False

def enable():
    port.write("EN")
    return "ok"

def disable():
    port.write("DI")
    return "ok"

def moveForward(dist):
    port.write("MF " + str("%.4f" % dist))

def spin(angle):
    port.write("S " + str("%.4f" % angle))

def height(dist):
    port.write("A " + str("%.4f" % dist))

def spinBody(angle):
    port.write("ST " + str("%.4f" % angle))

def spinBase(angle):
    port.write("SB " + str("%.4f" % angle))

def homeArm():
    port.write("HA")

def homeBase():
    port.write("HT")

def home():
    port.write("H")
