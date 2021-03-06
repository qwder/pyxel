import os

import numpy as np

import pyxel

from .editor_constants import SCREEN_HEIGHT, SCREEN_WIDTH
from .widget import Widget


class Screen(Widget):
    def __init__(self, parent, image_file):
        super().__init__(
            parent, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, is_visible=False)

        dirname = os.path.join(os.path.dirname(__file__), 'assets')
        pyxel.image(3, system=True).load(0, 16, image_file, dirname=dirname)

        data = pyxel.image(3, system=True).data
        self._image_data = np.copy(data[16:SCREEN_HEIGHT + 16, 0:SCREEN_WIDTH])

        self._edit_history_list = []
        self._edit_history_index = 0

        self.add_event_handler('show', self.on_show)
        self.add_event_handler('draw', self.on_draw)

    @property
    def can_undo(self):
        return self._edit_history_index > 0

    @property
    def can_redo(self):
        return self._edit_history_index < len(self._edit_history_list)

    def undo(self):
        if not self.can_undo:
            return

        self._edit_history_index -= 1
        self.call_event_handler(
            'undo', self._edit_history_list[self._edit_history_index])

    def redo(self):
        if not self.can_redo:
            return

        self.call_event_handler(
            'redo', self._edit_history_list[self._edit_history_index])
        self._edit_history_index += 1

    def add_edit_history(self, data):
        self._edit_history_list = self._edit_history_list[:self.
                                                          _edit_history_index]
        self._edit_history_list.append(data)
        self._edit_history_index += 1

    def on_show(self):
        data = pyxel.image(3, system=True).data
        data[16:16 + SCREEN_HEIGHT, 0:SCREEN_WIDTH] = self._image_data

    def on_draw(self):
        pyxel.blt(0, 0, 3, 0, 16, SCREEN_WIDTH, SCREEN_HEIGHT, 6)

    def draw_not_implemented_message(self):
        pyxel.rect(78, 83, 163, 97, 11)
        pyxel.rectb(78, 83, 163, 97, 1)
        pyxel.text(84, 88, 'NOT IMPLEMENTED YET', 1)

    def on_undo(self, data):
        pass

    def on_redo(self, data):
        pass
