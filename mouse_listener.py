from pynput.mouse import Listener, Button
import copy

class MouseListener:

    def __init__(self):
        self._status = {
            'position': (0,0),
            'click': dict(),
            'scroll': 0
        }

        self._listener = Listener(
            on_move=self._on_move,
            on_click=self._on_click,
            on_scroll=self._on_scroll)

    def _on_move(self, x, y):
        self._status['position'] = (x,y)

    def _on_click(self, x, y, button, pressed):
        if pressed:
            self._status['click'][button] = None
        elif button in self._status['click']:
            self._status['click'].pop(button, None)

    def _on_scroll(self, x, y, dx, dy):
        self._status['scroll'] = dy

    def get_status(self):
        status = copy.deepcopy(self._status)
        status['click'] = list(self._status['click'].keys())
        return status

    def start_listening(self):
        self._listener.start()
