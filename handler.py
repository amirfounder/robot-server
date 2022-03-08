import shlex
import keyboard
import pyautogui
import mouse


def handle_message(message: str):
    args = shlex.split(message)
    
    if args[0] == 'mouse-click':
        try:
            coordinates = args[1].split(',')
            coordinates = [int(float(x)) for x in coordinates]
            x, y = coordinates
        except:
            return 'mouse-click ERROR: Second args must a valid coordinate format (i.e. : #,#) but got {}'.format(args[1])
        
        pyautogui.moveTo(x, y, 1)
        mouse.click()
        return 'mouse-click SUCCESS'

    if args[0] == 'keyboard-write':
        keyboard.write(args[1])
        return 'keyboard-write SUCCESS'
    
    if args[0] == 'keyboard-backspace':
        try:
            backspace_count = int(args[1])
        except:
            return 'keyboard-backspace ERROR: Second args must be a number'

        for _ in range(backspace_count):
            keyboard.press_and_release('backspace')
        return 'keyboard-backspace SUCCESS'
