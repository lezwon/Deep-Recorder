from threading import Thread
import time

from pynput.keyboard import Key, Listener


class KeyboardListener:

    def __init__(self):
        self.listener = Listener(
            on_press=self._on_press,
            on_release=self._on_release)
        self._status = set()

    def _on_press(self, key):
        self._status.add(key)

    def _on_release(self, key):
        self._status.remove(key)

    def get_status(self):
        return self._status

    def start_listening(self):
        self.listener.start()


check = KeyboardListener()
check.start_listening()
for i in range(10):
    time.sleep(1)
    print(check.get_status())
# check.stop()
