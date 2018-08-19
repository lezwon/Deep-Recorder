import cv2
import numpy as np
from mss import mss
from time import sleep
from threading import Thread

class ScreenRecorder:
    def __init__(self):
        self.screen = mss()
        self._shot = None
        self._listener = Thread(target=self._take_screenshot)

    def _take_screenshot(self):
        while True:
            screenshot = self.screen.grab(self.screen.monitors[0])
            screenshot = np.array(screenshot)
            self._shot = cv2.resize(screenshot[:,:,:-1], dsize=(256, 256),
                               interpolation = cv2.INTER_CUBIC)

    def get_screenshot(self):
        return self._shot

    def start_recording(self):
        self._listener.start()
