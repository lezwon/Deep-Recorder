from pynput.keyboard import Key, Listener
from time import sleep

class KeyboardListener:

    def __init__(self):
        self._status = {}
        self._listener = Listener(
            on_press=self._on_press,
            on_release=self._on_release)

    def _on_press(self, key):
        self._status[key] = None

    def _on_release(self, key):
        self._status.pop(key, None)

    def get_state(self):
        return self._status.keys()

    def start_listening(self):
        self._listener.start()
