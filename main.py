from mouse_listener import MouseListener
from keyboard_listener import KeyboardListener
from screen_recorder import ScreenRecorder
from data_handler import DataHandler
import keyboard
import time

mouse_listener = MouseListener()
keyboard_listener = KeyboardListener()
screen_recorder = ScreenRecorder()
data_handler = DataHandler()

keyboard.wait('f12')

screen_recorder.start_recording()
keyboard_listener.start_listening()
mouse_listener.start_listening()

while True:
    time.sleep(1)
    screenshot = screen_recorder.get_screenshot()
    keyboard_status = keyboard_listener.get_status()
    mouse_status = mouse_listener.get_status()
    data_handler.submit(screenshot, keyboard_status, mouse_status)
    if keyboard.is_pressed('f12'):
        break

print(len(keyboard_listener.get_status()))
