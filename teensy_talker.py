import serial
import time

port = serial.Serial("/dev/ttyACM0", baudrate=115200, timeout=3.0)

currentTheta = 0.0      # deg
maxTheta     = 180      # deg

currentHeight = 0.05    # m
maxHeight = 0.2         # m


def read_line():
    if port.inWaiting():
        return port.readline()
    return False


def send_command(command):
    port.write(command + ',')


def enable():
    port.write('EN' + ',')
    time.sleep(1)


def disable():
    print('disabeling command sent')
    port.write("DI" + ',')


def move_forward(dist):
    port.write("MF " + str("%.4f" % dist) + ',')
    return "dd"


def spin(angle):
    port.write("S " + str("%.4f" % angle) + ',')
    return "dd"


def height(dist):
    global currentHeight, maxHeight

    new_height = currentHeight + dist
    if 0 < new_height < maxHeight:
        currentHeight = new_height
        port.write("A " + str("%.4f" % dist) + ',')
        return "d"
    print("Invalid height.")


def spin_body(angle):
    global currentTheta, maxTheta

    new_theta = currentTheta + angle
    if abs(new_theta) < maxTheta:
        currentTheta = new_theta
        port.write("ST " + str("%.4f" % angle) + ',')
        return "d"
    print("Invalid angle.")


def spin_base(angle):
    global currentTheta, maxTheta

    new_theta = currentTheta - angle
    if abs(new_theta) < maxTheta:
        currentTheta = new_theta
        port.write("SB " + str("%.4f" % angle) + ',')
        return "ddd"
    print("Invalid angle.")


def home_arm():
    port.write("HA" + ',')
    return "hdd"


def home_base():
    port.write("HT" + ',')
    return "hdddd"


def home():
    port.write("H" + ',')
    return "hhdddd"


def set_velocity(left, right, theta, h):
    port.write("V " + str("%.4f" % left) + ' ' + str("%.4f" % right) + ' ' + str("%.4f" % theta) + ' ' + str("%.4f" % h) + ',')


def home_to_home_position():
    spin_base(-currentTheta)