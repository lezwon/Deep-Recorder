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
    time.sleep(0.3)
    screenshot = screen_recorder.get_screenshot()
    keyboard_state = keyboard_listener.get_state()
    mouse_state = mouse_listener.get_state()
    data_handler.submit(screenshot, keyboard_state, mouse_state)
    if keyboard.is_pressed('f12'):
        break

print(len(keyboard_listener.get_state()))
