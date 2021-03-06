# coding: utf-8
# Python 3.6.2
# ----------------------------------------------------------------------------

from threading import Thread
from time import sleep


from .. import ids
from .. import colors as COLORS
from .. import terminal


class Scrolling:

    def __init__(
            self,
            value,
            *,
            bg:str = None,
            fg:str = None,
            border = None,

            row:int = 0,
            column:int = 0,
            spanrow:int = 0,
            spancolumn:int = 0,

            **kwargs
        ):

        self.value = str(value)

        self.bg = bg
        self.fg = fg

        self.border = border

        self.row = row
        self.column = column
        self.spanrow = spanrow
        self.spancolumn = spancolumn

        self._info = None

        self.parent = None
       
        if id:
            ids.set(id, self)

    def copy(self, **kwargs):
        attrs = {**self.__dict__}
        attrs.update(kwargs)
        return Scrolling(**attrs)

    def set(self, value):
        self.value = str(value)
        
        if self._info:
            terminal.clear(*self._info)
            self.run(*self._info)

    def run(self, x, y, width, height):

        self._info = (x, y, width, height)

        if self.border:
            x, y, width, height = self.border.run(x, y, width, height)

        def start():

            i = 0
            h = 0

            value = self.value.replace('\n', ' ')

            if len(value) < width:
                value += ' ' * (width - len(value))


            i = width
            text = value[:width]

            while True:

                i += 1
                if i >= width:
                    i = 0

                text = text[-len(text)+1:] + value[i]

                terminal.write(
                    # Reset
                    f"\033[{y};{x}H"
                    + ' ' * width
                    # New
                    + f"\033[{y};{x}H"
                    + COLORS.FG.get(self.fg, '')
                    + COLORS.BG.get(self.bg, '')
                    + text
                    + COLORS.FG.get('reset')
                    + COLORS.BG.get('reset')
                )

                sleep(1)

        p = Thread(target=start)
        p.daemon = True
        p.start()

    def delete(self):

        if self.parent:
            self.parent.rem(self)