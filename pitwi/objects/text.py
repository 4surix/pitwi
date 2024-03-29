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
            id:str = None,

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

    def copy(self, value=None, **kwargs):
        attrs = {**self.__dict__}
        attrs['value'] = value or self.value
        attrs.update(kwargs)
        return Text(**attrs)

    def set(self, value = None, *, bg = None, fg = None, border = None):
        if value: self.value = str(value)
        if bg: self.bg = bg
        if fg: self.fg = fg
        if border: self.border = border

        if self._info:
            terminal.clear(*self._info)
            self.run(*self._info)

    def run(
            self, 
            x:int, y:int, width:int, height:int
        ) -> None:

        self._info = (x, y, width, height)

        if self.border:
            x, y, width, height = self.border.run(x, y, width, height)

        COLOR = COLORS.FG.get(self.fg, '') + COLORS.BG.get(self.bg, '')

        terminal.format_and_write(self.value, x, y, width, height, COLOR)

    def delete(self):

        if self.parent:
            self.parent.rem(self)


    Fish = lambda value = None, *args, **kwargs: Text(value or "  _\n><_>", *args, **kwargs)