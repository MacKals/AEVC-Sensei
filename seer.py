## AEVC ##
# Determine device type
import cv2
import numpy as np

import picamera
picamera.PiCamera().vflip = True


imageNameIncrement = 0


def image_name():
    return "temp/image" + str(imageNameIncrement) + ".jpg"


def take_picture():
    picamera.PiCamera().capture(image_name())

    global imageNameIncrement
    imageNameIncrement += 1


# Circle properties
diameter = 0.1  # m

# Camera properties
xPixels = 3280
yPixels = 2464

xAngleOfView = 62.2/2 * np.pi/180  # rad
yAngleOfView = 48.8/2 * np.pi/180  # rad

# Helper constants
widthAt1m = 2 * np.tan(xAngleOfView) # total width of cameras field of view 1m in front
expectedWidthFraction = diameter / widthAt1m


# Takes picture and returns true if there is a port detected
def port_present():
    take_picture()
    return True


def x_angle_from_offset(x):
    pixel_offset = x - xPixels/2
    return pixel_offset/xPixels * xAngleOfView


def y_angle_from_offset(y):
    pixel_offset = y - yPixels/2
    return pixel_offset/yPixels * yAngleOfView


# Distance from camera to object
# Assuming: port is located in centre of image to avoid underestimate
def x_from(width):
    return xPixels/width * expectedWidthFraction


# Angle circle must be turned to face camera
# Assuming: port is located in centre of image to minimize error
def theta_from(width, height):
    return np.arccos(width/height)


# Angle camera must be turned to centre circle in image
def phi_from(x):
    return x_angle_from_offset(x)


def h_from(y, height):
    return x_from(height) * np.tan(y_angle_from_offset(y))


def convert_to_binary(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    ret, binary = cv2.threshold(gray, 80, 255, cv2.THRESH_BINARY_INV)
    return binary


def relative_position_from_binary(binary):

    returned_image, contours, hierarchy = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if not contours:
        return

    # pick largest contour
    index = 0
    max_area = 0

    for i in range(len(contours)):
        if cv2.contourArea(contours[i]) > max_area:
            index = i
            max_area = cv2.contourArea(contours[i])

    (x, y), (width, height), _ = cv2.fitEllipse(contours[index])

    # computing parameters

    r_computed = x_from(width)
    theta_computed = theta_from(width, height)
    phi_computed = phi_from(x)
    h_computed = h_from(y, height)

    x_relative = r_computed * np.sin(theta_computed)
    y_relative = r_computed * np.cos(theta_computed)
    z_relative = h_computed
    phi_relative = phi_computed

    return x_relative*1000, y_relative*1000, z_relative*1000, phi_relative


def pos_from_image(image):
    binary = convert_to_binary(image)
    return relative_position_from_binary(binary)
