import numpy
import cv2


def find_red_percent_in_image(image_hsv):
    # create mask of all red
    RED_MIN = numpy.array([0, 10, 10], numpy.uint8)
    RED_MAX = numpy.array([2, 255, 255], numpy.uint8)

    mask = cv2.inRange(image_hsv, RED_MIN, RED_MAX)

    # calc percent of mask
    height, width = mask.shape[:2]
    num_pixels = height * width
    count_white = cv2.countNonZero(mask)
    percent_white = (count_white/num_pixels) * 100
    percent_white = round(percent_white, 2)
    print(percent_white)
    return percent_white