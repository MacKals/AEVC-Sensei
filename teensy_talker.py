import serial
import time

port = serial.Serial("/dev/ttyACM0", baudrate=115200, timeout=3.0)


def read_line():
    if port.inWaiting():
        return port.readline()
    return False


def enable():
    port.write('EN')
    time.sleep(1)


def disable():
    port.write("DI")


def move_forward(dist):
    port.write("MF " + str("%.4f" % dist))
    return "dd"


def spin(angle):
    port.write("S " + str("%.4f" % angle))
    return "dd"


def height(dist):
    port.write("A " + str("%.4f" % dist))
    return "d"


def spin_body(angle):
    port.write("ST " + str("%.4f" % angle))
    return "d"


def spin_base(angle):
    port.write("SB " + str("%.4f" % angle))
    return "ddd"


def home_arm():
    port.write("HA")
    return "hdd"


def home_base():
    port.write("HT")
    return "hdddd"


def home():
    port.write("H")
    return "hhdddd"


def set_velocity(left, right):
    port.write("V " + str("%.4f" % left) + ' ' + str("%.4f" % right))

