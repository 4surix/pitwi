# coding: utf-8
# Python 3.6.2
# ----------------------------------------------------------------------------

from typing import Union


from .. import ids
from .. import terminal
from .. import colors as COLORS


class Zone:

    def __init__(
            self,
            *,
            color:str = None,
            border:str = None,
            id:str = None,

            rows:int = 0,
            columns:int = 0,
            childs:list = [],

            **kwargs
        ):

        self.color = color
        self.border = border

        self.rows = rows
        self.columns = columns

        self.childs = childs if childs else []

        self._info = None

        self.parent = None

        if id:
            ids.set(id, self)

    def copy(self, **kwargs):
        attrs = {**self.__dict__}
        attrs.update(kwargs)
        return Zone(childs = [c.copy() for c in attrs.pop('childs')], **attrs)

    def add(
            self, 
            child, 
            *, 
            row:int = None, column:int = None,
            spanrow:int = 1, spancolumn:int = 1
        ):

        child.row = row if row else self.rows + 1
        child.column = column if column else 1
        child.spanrow = spanrow
        child.spancolumn = spancolumn

        child.parent = self

        self.rows = max(self.rows, child.row + child.spanrow - 1)
        self.columns = max(self.columns, child.column + child.spancolumn - 1)

        self.childs.append(child)

        if self._info:
            terminal.clear(*self._info)
            self.run(*self._info)

        return self

    def rem(
            self, 
            child
        ):

        child.parent = None

        child.delete()
        self.childs.remove(child)

        if child.row <= self.rows:
            self.rows -= child.spanrow

            for child__ in self.childs:
                if child__.row > child.row:
                    child__.row -= child.spanrow

        if child.column <= self.columns:
            self.columns -= child.spancolumn

            for child__ in self.childs:
                if child__.column > child.column:
                    child__.column -= child.spancolumn

        if self._info:
            terminal.clear(*self._info)
            self.run(*self._info)

        return self

    def run(self, x:int, y:int, width:int, height:int) -> None:

        self._info = (x, y, width, height)

        if self.border:
            x, y, width, height = self.border.run(x, y, width, height)

        color = COLORS.BG.get(self.color)
        reset = f'\033[49m'

        if color:
            for h in range(height):
                terminal.write(
                    f"\033[{y + h};{x}H"
                    + color
                    + ' ' * width
                    + reset
                )

        if not self.columns or not self.rows:
            return

        wzone = width // self.columns
        hzone = height // self.rows

        for child in self.childs:

            x__ = x + (wzone * (child.column - 1))
            y__ = y + (hzone * (child.row - 1))

            width = wzone * child.spancolumn
            height = hzone * child.spanrow

            child.run(x__, y__, width, height)

    def delete(self):

        if self.parent:
            self.parent.rem(self)