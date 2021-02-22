# coding: utf-8
# Python 3.6.2
# ----------------------------------------------------------------------------

import os

from time import sleep


from .. import binding
from .. import terminal
from .zone import Zone


class Root(Zone):

    def __init__(self, width:int = None, height:int = None):
        super().__init__()

        if width and height:
            os.system(f'mode {width}, {height}')

        self.width, self.height = terminal.get_size()
        self.width -= 1
        self.height -= 1

    def run(self, *, block=True):
        Zone.run(self, 1, 1, self.width, self.height)
        if block:
            while True: sleep(60)

    def bind(self, carac, function):
        binding.add(carac, function)
        return self