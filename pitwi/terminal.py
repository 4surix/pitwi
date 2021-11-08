# ---------------------------------------------------------------------------
# Source :
# - https://gist.github.com/jtriley/1108174
# - http://stackoverflow.com/questions/566746/how-to-get-console-window-width-in-python


import re
import os
import sys
import struct
import colorama
import platform

from threading import Thread
from time import sleep


from . import colors
from . import keypress


DEBUG = True

def DEBUG_write(data):
    if DEBUG:
        with open('DEBUG_PITWI.txt', 'a', encoding='utf-8') as f:
            f.write(str(data)  + '\n\n\n@@@\n\n\n')


current_os = platform.system()

if current_os == 'Windows':

    import shlex
    import subprocess

    from ctypes import windll, create_string_buffer

    def get_size():

        h = windll.kernel32.GetStdHandle(-12)
        csbi = create_string_buffer(22)
        res = windll.kernel32.GetConsoleScreenBufferInfo(h, csbi)

        if res:
            (
                bufx, bufy, curx, cury, wattr,
                left, top, right, bottom,
                maxx, maxy
            ) = struct.unpack(
                "hhhhHhhhhhh", csbi.raw
            )
            sizex = right - left + 1
            sizey = bottom - top + 1
            return sizex, sizey

        else:
            cols = int(subprocess.check_call(shlex.split('tput cols')))
            rows = int(subprocess.check_call(shlex.split('tput lines')))
            return cols, rows

elif current_os in ['Linux', 'Darwin'] or current_os.startswith('CYGWIN'):

    import fcntl
    import termios

    def get_size():

        ioctl_GWINSZ = lambda fd: struct.unpack(
            'hh',
            fcntl.ioctl(fd, termios.TIOCGWINSZ, '1234')
        )

        cr = ioctl_GWINSZ(0) or ioctl_GWINSZ(1) or ioctl_GWINSZ(2)

        if not cr:
            fd = os.open(os.ctermid(), os.O_RDONLY)
            cr = ioctl_GWINSZ(fd)
            os.close(fd)

        if not cr:
            cr = (os.environ['LINES'], os.environ['COLUMNS'])

        return int(cr[1]), int(cr[0])


sys_stdout = sys.stdout

colorama.init()

datas = []

def write(data):
    datas.append(data)


def run():

    while True:

        if datas:

            keypress.getKey.unlisten()

            while datas:
                data = (
                    datas.pop(0)
                    .encode(sys_stdout.encoding, 'replace')
                    .decode(sys_stdout.encoding, 'replace')
                )
                DEBUG_write(data)
                sys.stdout.write(data)

            sys.stdout.flush()

            keypress.getKey.listen()

p = Thread(target=run)
p.daemon = True
p.start()


def format_and_write(value, x, y, width, height, COLOR):

    i = 0
    h = 0

    data = ''
    surplus = 0

    RESET = colors.FG.get('reset') + colors.BG.get('reset')

    has_escape_chars = '\033' in value

    if has_escape_chars:
        value_split = [
            value
            for i, value in enumerate(
                re.split('((\033\\[[0-9]+;[0-9]+H|\033\\[[0-9]{2}m)+)', value)
                ,
                1
            )
            if i % 3 != 0
        ]

    len_value = len(value.replace('\n', ''))

    while i < len_value and h < height:

        len_carac_ANSI = 0

        if has_escape_chars:

            v = 0
            part__ = ''

            for index, part in enumerate([*value_split]):

                # ANSII carac
                if index % 2 != 0:
                    value_split.pop(0)
                    part__ += part
                    len_carac_ANSI += len(part)
                    continue

                # Text carac
                for char in part:
                    v += 1
                    part__ += char
                    value_split[0] = value_split[0][1:]
                    if v >= width - surplus:
                        break
                else:
                    value_split.pop(0)
                    continue

                break

            part = part__

        else:
            part = part__ = value[i : i + width - surplus]

        nl = 0
        index = 0

        while '\n' in part:
            nl += 1
            index = part__.index('\n')
            part__ = part__.replace('\n', '', 1)
            part = part.replace('\n', f"\033[{y + h + nl};{x}H", 1)

        data += (
            f"\033[{y + h};{surplus + x}H"
            + COLOR
            + part
            + RESET
        )

        i += width - surplus
        h += 1 + nl

        surplus = 0

        if index:
            h -= 1
            surplus = len(part__) - index - len_carac_ANSI

    datas.append(data)


def clear(x, y, width, height):

    value = ''

    for h in range(height):
        value += f"\033[{y + h};{x}H" + ' ' * width

    datas.append(value)


def clearall():
    if platform.system() == 'Windows':
        os.system(f'cls')
    else:
        os.system(f"clear")


def resize(width, height):
    if platform.system() == 'Windows':
        os.system(f'mode {width}, {height}')
    else:
        os.system(f"printf '\033[8;{height};{width}t'")