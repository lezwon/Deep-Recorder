import h5py
import threading
import numpy as np
from threading import Thread
from pynput.keyboard import Key, KeyCode
from pynput.mouse import Button
from concurrent.futures import ThreadPoolExecutor

class DataHandler:

    def __init__(self):
        self.batch_size = 10
        self.batch = []
        self._cs_keys = ['w', 'a', 's', 'd', 'g', '1', '2', '3', '4', Key.space, Key.shift, Key.ctrl_l]
        self._cs_mouse_keys = [ Button.left, Button.middle, Button.right ]
        self.h5file = h5py.File("./dataset.hdf5", "w")
        
        keys_length = len(self._cs_keys) + len(self._cs_mouse_keys)
        position_length = 2
        scroll_length = 1

        self._cs_keys = [KeyCode.from_char(key) if type(key) is str else key for key in self._cs_keys]

        self.DS_img = self.h5file.create_dataset("img", (0, 256, 256, 3), maxshape=( None,  256, 256, 3), compression="gzip", compression_opts=9, chunks=(self.batch_size, 256, 256, 3))

        self.DS_keys = self.h5file.create_dataset(
            "keys", (0, keys_length), maxshape=(None, keys_length), chunks=True)

        self.DS_position = self.h5file.create_dataset(
            "position", (0, position_length), maxshape=(None, position_length), chunks=True)

        self.DS_scroll = self.h5file.create_dataset(
            "scroll", (0, ), maxshape=(None, ), chunks=True)

    def submit(self, image, keyboard, mouse):
        keyboard_array = self._process_keyboard(keyboard)
        mouse_postion, mouse_keys, mouse_scroll = self._process_mouse(mouse)
        print(keyboard_array)
        print(mouse_keys)
        keys_array = np.concatenate([keyboard_array, mouse_keys])
        self.batch.append(np.array([image, keys_array, mouse_postion, mouse_scroll]))
        if len(self.batch) == self.batch_size:
            with ThreadPoolExecutor(max_workers=5) as executor:
                future = executor.submit(self._save, self.batch)
                print(future.result())
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
        return np.array(mouse['position']), np_keys, np.array(mouse['scroll'])

    def _save(self, batch):

        batch_imgs = np.array([datapoint[0] for datapoint in batch])
        batch_keys = np.array([datapoint[1] for datapoint in batch])
        batch_position = np.array([datapoint[2] for datapoint in batch])
        batch_scroll = np.array([datapoint[3] for datapoint in batch])
        
        self.DS_img.resize(self.DS_img.shape[0] + self.batch_size, axis = 0)
        self.DS_keys.resize(self.DS_keys.shape[0] + self.batch_size, axis=0)
        self.DS_position.resize(self.DS_position.shape[0] + self.batch_size, axis = 0)
        self.DS_scroll.resize(self.DS_scroll.shape[0] + self.batch_size, axis = 0)

        self.DS_img[-self.batch_size:] = batch_imgs
        self.DS_keys[-self.batch_size:] = batch_keys
        self.DS_position[-self.batch_size:] = batch_position
        self.DS_scroll[-self.batch_size:] = batch_scroll

        self.DS_img.flush()
        self.DS_keys.flush()
        self.DS_position.flush()
        self.DS_scroll.flush()

        return "Saved to H5 {}".format(threading.current_thread())
