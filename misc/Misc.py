import time
from random import randrange
import math

from core.Client import *


def get_local_coords(x, y):
    w = Client()
    return w.bounds[0] + x, w.bounds[1] + y


def random_range(low, high):
    return randrange(low, high)


def sleep(ms_low, ms_high):
    time.sleep(random_range(ms_low, ms_high) / 1000)


def center_of_contour(contour):
    m = cv2.moments(contour)
    return int(m["m10"] / m["m00"]), int(m["m01"] / m["m00"])


def contour_box(contour):
    return cv2.boundingRect(contour)


def count_color(color_low, color_high, bounds=None):
    t = time.time()
    bgr = Client().get_canvas(bounds)
    print(time.time() - t)
    hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, color_low, color_high)
    return cv2.countNonZero(mask)


def rand_box(box, offset=0):
    return random_range(box[0] + offset, box[2] - offset), random_range(box[1] + offset, box[3] - offset)


def distance(pt1, pt2):
    return math.hypot(pt2[0] - pt1[0], pt2[1] - pt1[1])


def distance_to_contour(contour, point):
    return distance(center_of_contour(contour), point)


def filter_contour_area(contours, min_contour):
    temp = contours
    i = 0
    for c in contours:
        if cv2.contourArea(c) > min_contour:
            temp[i] = c
            i += 1

    return temp[0:i]


