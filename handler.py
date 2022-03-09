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
                    Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB)).save(f'{args[1]}.png')
                screenshots.append(image)
                return 'SUCCESS'
            except Exception as e:
                print(e)
                return 'ERROR'

    if args[0] == 'compute-difference-between-last-two-images':
        last_two = screenshots[-2:]
        last_two = [cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) for img in last_two]

        before, after = last_two
        score, diff = compare_ssm(before, after, full=True)
        diff = (diff * 255).astype('uint8')
        print('SSIM: {}'.format(score))

        thresh = cv2.threshold(diff, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
        cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)

        boxes = []

        for c in cnts:
            (x, y, w, h) = cv2.boundingRect(c)
            boxes.append((x, y, w, h))
            cv2.rectangle(before, (x, y), (x + w, y + h), (0, 0, 255), 2)
            cv2.rectangle(after, (x, y), (x + w, y + h), (0, 0, 255), 2)
        
        x, y, w, h = boxes[0]
        return [(w/2) + x, (h/2) + y]



    return 'no valid functions for your input'
        