# coding: utf-8
# Python 3.6.2
# ----------------------------------------------------------------------------

from .. import colors as COLORS
from .. import ids
from .. import terminal


class Text:

    def __init__(
            self, 
            value, 
            *, 
            bg:str = None, 
            fg:str = None, 
            border = None,
            id:str = None
        ):

        self.value = str(value)

        self.bg = bg
        self.fg = fg

        self.border = border

        if id:
            ids.set(id, self)

    def set(self, value):
        self.value = str(value)
        self.run(*self._info)

    def run(
            self, 
            x:int, y:int, width:int, height:int
        ) -> None:

        self._info = (x, y, width, height)

        if self.border:
            x, y, width, height = self.border.run(x, y, width, height)

        i = 0
        h = 0

        COLOR = COLORS.FG.get(self.fg, '') + COLORS.BG.get(self.bg, '')
        RESET = COLORS.FG.get('reset') + COLORS.BG.get('reset')

        value = self.value

        if x - 1:
            value = value.replace('\n', '\n' + f"\033[{x - 1}C")

        while i < len(value) and h < height:

            terminal.write(
                f"\033[{y + h};{x}H"
                + COLOR
                + value[i : i + width]
                + RESET
            )

            i += width
            h += 1