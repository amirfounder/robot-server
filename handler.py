import shlex
import keyboard
import pyautogui
import mouse
import mss
import numpy
from skimage.metrics import structural_similarity as compare_ssm
import cv2
import imutils
from PIL import Image

screenshots = []


def handle_message_data(message_data: str | dict):
    args = shlex.split(message_data)

    if args[0] == 'save-data':
        pass

    if args[0] == 'mouse-click':
        try:
            coordinates = args[1].split(',')
            coordinates = [int(float(x)) for x in coordinates]
            x, y = coordinates
        except:
            return 'mouse-click ERROR: Second args must a valid coordinate format (i.e. : #,#) but got {}'.format(args[1])

        pyautogui.moveTo(x, y, .2)
        mouse.click()
        return 'mouse-click SUCCESS'

    if args[0] == 'keyboard-write':
        keyboard.write(args[1], 0.1)
        return 'keyboard-write SUCCESS'

    if args[0] == 'keyboard-backspace':
        try:
            backspace_count = int(args[1])
        except:
            return 'keyboard-backspace ERROR: Second args must be a number'

        for _ in range(backspace_count):
            keyboard.press_and_release('backspace')
        return 'keyboard-backspace SUCCESS'

    if args[0] == 'screen-capture':
        with mss.mss() as sct:
            try:
                image = numpy.array(sct.grab(sct.monitors[1]))
                if len(args) == 2:
                    Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB)).save(
                        f'{args[1]}.png')
                screenshots.append(image)
                return 'SUCCESS'
            except Exception as e:
                print(e)
                return 'ERROR'

    if args[0] == 'compute-difference-between-last-two-images':
        last_two = screenshots[-2:]
        before, after = last_two
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
            after_hsv = cv2.cvtColor(after, cv2.COLOR_BGR2HSV)
            cropped_hsv = after_hsv[y:y+h, x:x+w]
            percent_red = find_red_percent_in_image(cropped_hsv)

            if percent_red > 70:
                boxes.append((x, y, w, h))

        x, y, w, h = boxes[0]

        return [(w/2) + x, (h/2) + y]

    return 'no valid functions for your input'


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

