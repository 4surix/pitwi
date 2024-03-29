# coding: utf-8
# Python 3.6.2
# ----------------------------------------------------------------------------

import os

from time import sleep


from .. import ids
from .. import binding
from .. import terminal
from .. import keypress
from .. import navigation
from .zone import Zone


class Root(Zone):

    def __init__(self, width:int = None, height:int = None, debug:bool = False):
        super().__init__()

        terminal.debug = debug

        terminal.clearall()
        
        if width and height:
            terminal.resize(width, height)

        self.width, self.height = terminal.get_size()
        self.width -= 1
        self.height -= 1

        terminal.DEBUG_write(f"NEW ROOT\nWIDTH={self.width} | HEIGHT={self.height}")

    def active(self):
        pass

    def inactive(self):
        pass

    def run(self, *, block=True):

        keypress.getKey.unlisten()

        navigation.add(self)

        Zone.run(self, 1, 1, self.width, self.height)

        if block:
            while binding.running:
                sleep(1)

        keypress.getKey.unlisten()
        terminal.clearall()
        exit()

    def bind(self, carac, function):
        binding.add(carac, function)
        return self

    def setid(self, **kwargs):
        for id, element in kwargs.items():
            ids.set(id, element)
        return self