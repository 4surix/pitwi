# coding: utf-8
# Python 3.6.2
# ----------------------------------------------------------------------------

from .. import colors as COLORS
from .. import ids
from .. import terminal
from .. import binding
from .. import navigation


class Map:

    def __init__(
            self, 
            value, 
            *,
            bg:str = None, 
            fg:str = None, 
            border = None,

            active_bg:str = None,
            active_fg:str = None,
            active_border = None,

            pos_fg:str = None,
            pos_bg:str = None,

            id:str = None,

            row:int = 0,
            column:int = 0,
            spanrow:int = 0,
            spancolumn:int = 0,

            **kwargs
        ):

        self._bg = self.bg = bg
        self._fg = self.fg = fg
        self._border = self.border = border

        self.active_bg = active_bg
        self.active_fg = active_fg
        self.active_border = active_border

        self.pos_bg = pos_bg
        self.pos_fg = pos_fg

        self.map = value


        # Check lenght lines y, for IndexError.
        if self.map:
            max_len_y = max(len(y) for y in self.map)

            for y in self.map:
                while len(y) < max_len_y:
                    y.append(None)


        self.tiles = {
            None: "  "
        }

        self.collisions = []

        self.pos = {
            'x': round(len(self.map) / 2), 
            'y': round(len(self.map[0]) / 2) if self.map else 0
        }

        self.row = row
        self.column = column
        self.spanrow = spanrow
        self.spancolumn = spancolumn

        self._info = None

        self.parent = None

        if id:
            ids.set(id, self)

    def active(self):
        binding.entry_active = self

        self._bg = self.active_bg or self.bg
        self._fg = self.active_fg or self.fg
        self._border = self.active_border or self.border

        self.run(*self._info)

    def inactive(self):
        binding.entry_active = None

        self._bg = self.bg
        self._fg = self.fg
        self._border = self.border

        self.run(*self._info)

    def add(self, key:str):

        if key == 'Left':
            self.moveLeft()
        elif key == 'Right':
            self.moveRight()
        elif key == 'Up':
            self.moveUp()
        elif key == 'Down':
            self.moveDown()

    def get_case(self, x, y):

        try: case = self.map[x][y]
        except:
            return
        else:
            return case

    def add_case(
            self,
            x = None, y = None, value = None,
        ):
        if x != None and y != None:
            if len(self.map) <= x:
                self.map.extend([] for _ in range(x - len(self.map) + 1))
            if len(self.map[x]) <= y:
                self.map[x].extend([None] * (y - len(self.map[x]) + 1))

            self.map[x][y] = value

        return self

    def set(
            self,
            x = None, y = None, value = None,
            *,
            bg = None, fg = None,
            border = None
        ):
        if x != None and y != None:
            if len(self.map) <= x:
                self.map.extend([] for _ in range(x - len(self.map) + 1))
            if len(self.map[x]) <= y:
                self.map[x].extend([None] * (y - len(self.map[x]) + 1))

            self.map[x][y] = value

        if bg: self.bg = bg
        if fg: self.fg = fg
        if border: self.border = border

        self.move(0, 0)

        return self

    def copy(self, value=None, **kwargs):
        attrs = {**self.__dict__}
        attrs['map'] = value or self.map
        attrs.update(kwargs)
        return Map(**attrs)

    def tile(self, name, value:str, collision=False):
        if len(value) != 2:
            return self
        self.tiles[name] = value
        if collision:
            self.collisions.append(name)
        return self

    def gen(self):

        text = ''

        COLOR_POS = (
            COLORS.FG.get(self.pos_fg or self.fg, '') 
            + COLORS.BG.get(self.pos_bg or self.bg, '')
        )
        RESET_COLOR = (
            '' if not COLOR_POS
            else
                COLORS.FG.get('reset') + COLORS.BG.get('reset') 
        )

        min_x = 0
        max_x = len(self.map)
        min_y = 0
        max_y = len(self.map[0])

        # Sub 1 because case pos not count
        cote_w = int(
            (int(self.width / 2) - 1) / 2
        )
        cote_h = int(
            (self.height - 1 if self.height % 2 == 0 else self.height) / 2
        )

        min_range_x = max(self.pos['x'] - cote_w, 0)
        max_range_x = min(self.pos['x'] + cote_w + 1, max_x)

        min_range_y = max(self.pos['y'] - cote_h, 0)
        max_range_y = min(self.pos['y'] + cote_h + 1, max_y)

        spacesL = (
            '' if min_range_x != min_x
            else
                ' ' * int(
                    (self.width - (max_range_x - min_range_x) * 2) 
                    / 
                    (1 + (max_range_x == max_x))
                )
        )

        spacesR = (
            '' if max_range_x != max_x
            else
                ' ' * int(
                    (self.width - (max_range_x - min_range_x) * 2) 
                    /
                    (1 + (min_range_x == min_x))
                    # If width is not even add one longueur
                    +
                    (0 if self.width % 2 == 0 else 1)
                )
        )

        if min_range_y == min_y:
            for _ in range(round(
                (self.height - (max_range_y - min_range_y) + 1) 
                /
                (1 + (max_range_y == max_y)))
            ):
                text += ' ' * self.width

        for y in range(min_range_y, max_range_y):

            text += spacesL

            for x in range(min_range_x, max_range_x):

                if self.pos['x'] == x and self.pos['y'] == y:
                    text += (
                        COLOR_POS 
                        + self.tiles.get(self.get_case(x, y), '??')
                        + RESET_COLOR
                    )
                else:
                    text += self.tiles.get(self.get_case(x, y), '??')

            text += spacesR

        if max_range_y == max_y:
            for _ in range(int(
                (self.height - (max_range_y - min_range_y) + 1)
                / (1 + (min_range_y == min_y)))
            ):
                text += ' ' * self.width

        return text

    def move(self, x, y):

        try: case = self.map[self.pos['x'] + x][self.pos['y'] + y]
        except:
            return
        else:
            if case in self.collisions:
                return

        self.pos['x'] += x
        self.pos['y'] += y

        if self.pos['x'] < 0:
            self.pos['x'] = 0
            return

        if self.pos['x'] >= len(self.map):
            self.pos['x'] = len(self.map) - 1
            return

        if self.pos['y'] < 0:
            self.pos['y'] = 0
            return

        if self.pos['y'] >= len(self.map[0]):
            self.pos['y'] = len(self.map[0]) - 1
            return

        COLOR = COLORS.FG.get(self._fg, '') + COLORS.BG.get(self._bg, '')

        terminal.format_and_write(
            self.gen(), self.x, self.y, self.width, self.height, COLOR
        )

    def moveLeft(self):
        self.move(-1, 0)

    def moveRight(self):
        self.move(+1, 0)

    def moveUp(self):
        self.move(0, -1)

    def moveDown(self):
        self.move(0, +1)

    def run(
            self, 
            x:int, y:int, width:int, height:int
        ) -> None:

        navigation.add(self)

        self._info = (x, y, width, height)

        input(width)

        if self._border:
            x, y, width, height = self._border.run(x, y, width, height)

        self.x = x
        self.y = y
        self.width = width
        self.height = height

        input(width)

        self.move(0, 0)

    def delete(self):

        if self.parent:
            self.parent.rem(self)

        navigation.rem(self)