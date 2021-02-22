# coding: utf-8
# Python 3.6.2
# ----------------------------------------------------------------------------

from typing import Callable
from threading import Thread
from time import sleep


from .. import ids
from .. import terminal
from ..objects import Border
from .. import keypress
from .. import colors as COLORS


class Entry:

    def __init__(
            self, 
            *, 
            textleft:str = '', 
            bg:str = None, 
            fg:str = None, 
            border:Border = None, 
            key:str = 'Return', 
            function:Callable[[str], None] = lambda value: None,
            id:str = None,

            **kwargs
        ):

        self.value = ''
        self.textleft = textleft

        self.bg = bg
        self.fg = fg

        self.border = border

        self.key = key
        self.function = function

        if id:
            ids.set(id, self)

    def copy(self, **kwargs):
        attrs = {**self.__dict__}
        attrs.update(kwargs)
        return Entry(**attrs)

    def run(
            self,
            x:int, y:int, width:int, height:int
        ) -> None:

        if self.border:
            x, y, width, height = self.border.run(x, y, width, height)

        terminal.write(f"\033[{y};{x}H" + self.textleft)

        def start():

            while True:

                end = ''

                key = keypress.getName()

                if key == 'BackSpace':
                    self.value = self.value[:-1]
                    end = " "

                elif key == self.key:
                    self.function(self.value)
                    end = ' ' * len(self.value)
                    self.value = ''

                else:
                    self.value += key

                i = 0
                h = 0

                COLOR = COLORS.FG.get(self.fg, '') + COLORS.BG.get(self.bg, '')
                RESET = COLORS.FG.get('reset') + COLORS.BG.get('reset')

                value = self.textleft + self.value + end
         
                while i <= len(value) and h < height:

                    terminal.write(
                        f"\033[{y + h};{x}H"
                        + COLOR
                        + value[i : i + width]
                        + RESET
                    )

                    i += width
                    h += 1

        p = Thread(target=start)
        p.daemon = True
        p.start()