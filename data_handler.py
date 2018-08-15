import h5py
import numpy as np
from pynput.keyboard import Key
from pynput.mouse import Button
from threading import Thread

class DataHandler:

    def __init__(self):
        self.batch_size = 5
        self.batch = []
        self._cs_keys = ['w', 'a', 'd', 's', 'g', '1', '2', '3', '4', Key.space, Key.shift, Key.ctrl_l]
        self._cs_mouse_keys = [ Button.left, Button.middle, Button.right ]
        self.h5file = h5py.File("dataset.hdf5", "w")
        # self.dataset = self.h5file.create_dataset("cs_awp", chunks = (self.batch_size, ), maxshape=(None, ), compression="gzip", compression_opts=9, dtype="uint8")

        self.dataset = self.h5file.create_dataset(
            "cs_awp", (0, ), maxshape=(None, ), compression="gzip", compression_opts=9, chunks = True)

    def submit(self, image, keyboard, mouse):
        keyboard_array = self._process_keyboard(keyboard)
        mouse_postion, mouse_keys, mouse_scroll = self._process_mouse(mouse)
        print(keyboard_array)
        print(mouse_keys)
        keys_array = np.concatenate([keyboard_array, mouse_keys])
        self.batch.append([image, keys_array, mouse_postion, mouse_scroll])
        if len(self.batch) == self.batch_size:
            Thread(target=self._save, args=[self.batch]).start()
            self.batch = []


    def _process_keyboard(self, keyboard):
        np_keys = np.zeros(12)
        for idx, key in enumerate(self._cs_keys):
            if key in keyboard:
                np_keys[idx] = 1
        return np_keys

    def _process_mouse(self, mouse):
        np_keys = np.zeros(3)
        for idx, key in enumerate(self._cs_mouse_keys):
            if key in mouse['click']:
                np_keys[idx] = 1
        return mouse['position'], np_keys, mouse['scroll']

    def _save(self, batch):
        self.dataset.resize((self.dataset.size + self.batch_size, ))
        self.dataset[-self.batch_size] = np.array(batch)
        self.dataset.flush()
