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

    navigation = navigation

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

        self._info = None

        self.parent = None

        if id:
            ids.set(id, self)

    def copy(self, value=None, **kwargs):
        attrs = {**self.__dict__}
        attrs['value'] = value or self.value
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

    def set(
            self, 
            value = None, 
            *,
            bg = None, fg = None, 
            active_bg = None, active_fg = None, 
            border = None,
            active_border = None
        ):
        if value: self.value = str(value)
        if bg: self.bg = bg
        if fg: self.fg = fg
        if border: self.border = border
        if active_bg: self.active_bg = active_bg
        if active_fg: self.active_fg = active_fg
        if active_border: self.active_border = active_border

        if self._info:
            terminal.clear(*self._info)
            self.run(*self._info)

    def run(
            self,
            x:int, y:int, width:int, height:int
        ) -> None:

        navigation.add(self)

        self._info = (x, y, width, height)

        if self._border:
            x, y, width, height = self._border.run(x, y, width, height)

        COLOR = COLORS.FG.get(self._fg, '') + COLORS.BG.get(self._bg, '')

        terminal.format_and_write(self.value, x, y, width, height, COLOR)

    def add(self, key:str):
        if key == self.key:
            self.function(self.value)

    def delete(self):

        if self.parent:
            self.parent.rem(self)

        navigation.rem(self)