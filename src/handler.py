from math import sqrt
from time import sleep
from turtle import back
import keyboard
import pyautogui
import mouse
import mss
import numpy
import cv2
import imutils
from skimage.metrics import structural_similarity as compare_ssm
from src.handler_service import *
from PIL import Image

screenshots = []
items = []

def handle_message_data(data: dict):
    method = data.get('method')

    if method == 'save-data':
        data_to_save = data.get('data', [])
        items.extend(data_to_save)
        print(len(items))

    if method == 'mouse-click':
        coordinates = data.get('coordinates')
        x, y = [int(x) for x in coordinates]
        pyautogui.moveTo(x, y, .05)
        mouse.click()
        return 'SUCCESS'

    if method == 'keyboard-write':
        content = data.get('content')
        keyboard.write(content, 0.1)
        return 'SUCCESS'

    if method == 'keyboard-backspace':
        backspace_count = data.get('count', 0)
        for _ in range(backspace_count):
            keyboard.press_and_release('backspace')
            sleep(.05)
        return 'SUCCESS'

    if method == 'screen-capture':
        filename = data.get('filename')
        sct = mss.mss()
        monitor = sct.monitors[1]
        image = numpy.array(sct.grab(monitor))

        if filename:
            save_nparray_to_file(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

        screenshots.append(image)
        return 'SUCCESS'

    if method == 'compute-difference-between-last-two-images':
        last_two = screenshots[-2:]
        _, after = last_two
        last_two_gray = [cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                         for img in last_two]

        before_gray, after_gray = last_two_gray
        score, diff = compare_ssm(before_gray, after_gray, full=True)
        diff = (diff * 255).astype('uint8')
        print('SSIM: {}'.format(score))

        thresh = cv2.threshold(
            diff, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
        cnts = cv2.findContours(
            thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)

        boxes = []

        for c in cnts:
            (x, y, w, h) = cv2.boundingRect(c)
            x, y, w, h = int(x), int(y), int(w), int(h)
            area = w * h

            after_hsv = cv2.cvtColor(after, cv2.COLOR_BGR2HSV)
            cropped_hsv = after_hsv[y:y+h, x:x+w]
            percent_red = find_red_percent_in_image(cropped_hsv)

            box = dict(
                rect=[x, y, w, h],
                area=area,
                percent_red=percent_red,
                score=int(.5 * sqrt(area) + .5 * percent_red)
            )
            boxes.append(box)
            print(box)

        boxes = [box for box in boxes if box['percent_red'] > 80]
        x, y, w, h = sorted(boxes, key=lambda box: box['score'], reverse=True)[0]['rect']


        return [(w/2) + x, (h/2) + y]
