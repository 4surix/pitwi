# coding: utf-8
# Python 3.6.2
# ----------------------------------------------------------------------------

from typing import Union


from .. import ids
from .. import terminal
from .. import colors as COLORS


class Carousel:

    def __init__(self, *,
            border:str = None,
            id:str = None,

            row:int = 0,
            column:int = 0,
            spanrow:int = 0,
            spancolumn:int = 0,

            childs:list = None,

            **kwargs
        ):

        self.border = border

        self.index = 0

        self.childs = childs or []

        self.row = row
        self.column = column
        self.spanrow = spanrow
        self.spancolumn = spancolumn

        if id:
            ids.set(id, self)

    def copy(self, **kwargs):
        attrs = {**self.__dict__}
        attrs.update(kwargs)
        return Carousel(childs = [c.copy() for c in attrs.pop('childs')], **attrs)

    def add(self, child):
        self.childs.append(child)
        return self

    def run(self, x:int, y:int, width:int, height:int) -> None:

        if self.border:
            x, y, width, height = self.border.run(x, y, width, height)

        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def change(self, index:int):

        if index < 0 or index >= len(self.childs):
            return

        self.index = index
        terminal.clear(self.x, self.y, self.width, self.height)
        self.childs[index].run(self.x, self.y, self.width, self.height)

    def next(self):

        child = self.childs[self.index]

        self.index += 1

        if self.index >= len(self.childs):
            self.index = 0

        terminal.clear(self.x, self.y, self.width, self.height)
        child.run(self.x, self.y, self.width, self.height)