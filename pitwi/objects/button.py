# coding: utf-8
# Python 3.6.2
# ----------------------------------------------------------------------------

from typing import Callable


from .. import ids
from .. import terminal
from .. import colors as COLORS
from .. import binding
from .. import navigation
from ..objects import Border


class Button:

    def __init__(
            self,
            value:str = '',
            *,
            bg:str = None,
            fg:str = None,
            border:Border = None,

            active_bg:str = None,
            active_fg:str = None,
            active_border:str = None,

            key:str = 'Return',
            function:Callable[[str], None] = lambda value: None,
            id:str = None,

            row:int = 0,
            column:int = 0,
            spanrow:int = 0,
            spancolumn:int = 0,

            **kwargs
        ):

        self.value = value

        self._bg = self.bg = bg
        self._fg = self.fg = fg
        self._border = self.border = border

        self.active_bg = active_bg or bg
        self.active_fg = active_fg or fg
        self.active_border = active_border or border

        self.key = key
        self.function = function

        self.row = row
        self.column = column
        self.spanrow = spanrow
        self.spancolumn = spancolumn

        if id:
            ids.set(id, self)

    def copy(self, **kwargs):
        attrs = {**self.__dict__}
        attrs.update(kwargs)
        return Button(**attrs)

    def active(self):
        binding.entry_active = self

        self._bg = self.active_bg
        self._fg = self.active_fg
        self._border = self.active_border

        self.run(*self._info)

    def inactive(self):
        binding.entry_active = None

        self._bg = self.bg
        self._fg = self.fg
        self._border = self.border

        self.run(*self._info)

    def set(self, value):
        self.value = str(value)
        self.run(*self._info)

    def run(
            self,
            x:int, y:int, width:int, height:int
        ) -> None:

        navigation.add(self)

        self._info = (x, y, width, height)

        if self._border:
            x, y, width, height = self._border.run(x, y, width, height)

        i = 0
        h = 0

        COLOR = COLORS.FG.get(self._fg, '') + COLORS.BG.get(self._bg, '')
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

    def add(self, key:str):
        if key == self.key:
            self.function()