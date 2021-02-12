# encode: utf-8
# Python 3.6.2
# ----------------------------------------------------------------------------

import typing

from typing import Tuple


from .. import terminal
from .. import colors as COLORS


class Border:
    
    def __init__(
            self, 
            NO : str, N : str, NE : str, 
            O  : str,          E  : str,
            SO : str, S : str, SE : str, 
            *, 
            color:str = None
        ):

        self.color = color

        (
            self.NO, self.N, self.NE,
            self.O ,         self.E ,
            self.SO, self.S, self.SE
        ) = (
            NO, N, NE,
            O ,     E,
            SO, S, SE
        )

    def copy(
            self, 
            NO:str = None, N:str = None, NE:str = None, 
            O:str = None,                E:str = None,
            SO:str = None, S:str = None, SE:str = None, 
            *, 
            color:str = None
        ):
        return Border(
            NO or self.NO, N or self.N, NE or self.NE,
            O  or self.O ,              E  or self.E ,
            SO or self.SO, S or self.S, SE or self.SE,
            color = color or self.color
        )

    def run(
            self, 
            x:int, y:int, width:int, height:int
        ) -> Tuple[int]:

        terminal.write(
            COLORS.FG.get(self.color, '')

            + (
                '' if not (self.NO or self.N or self.NE)
                else
                    f"\033[{y};{x}H" 
                    + self.NO + self.N * (width - 2) + self.NE
            )

            + (
                '' if not(self.O or self.E)
                else
                    ''.join(
                        f"\033[{y + i};{x}H" + self.O 
                        + f"\033[{y + i};{width}H" + self.E
                        for i in range(1, height - 1)
                    )
            )

            + (
                '' if not (self.SO or self.S or self.SE)
                else
                    f"\033[{y + height - 1};{x}H"
                    + self.SO + self.S * (width - 2) + self.SE
            )

            + COLORS.FG.get('reset')
        )

        if self.NO or self.O or self.SO:
            x += 1
            width -= 1
        
        if self.NE or self.E or self.SE:
            width -= 1
        
        if self.N:
            y += 1
            height -= 1
        
        if self.S:
            height -= 1

        return x, y, width, height


class Empty:

    def __len__(self):
        return 0

    def __bool__(self):
        return False

    def __str__(self):
        return ' '

    def __radd__(self, obj:str):
        return obj + ' '

    def __add__(self, obj:str):
        return ' ' + obj

    def __rmul__(self, obj:int):
        return ' ' * obj

    def __mul__(self, obj:int):
        return ' ' * obj

EMPTY = Empty()


class Borders:
    Tranparent = Border(
        ' ', ' ', ' ',
        ' ',      ' ',
        ' ', ' ', ' '
    )
    Simple = Border(
        '┌', '─', '┐',
        '│',      '│',
        '└', '─', '┘'
    )
    Corner = Border(
        '┌', ' ', '┐',
        ' ',      ' ',
        '└', ' ', '┘'
    )