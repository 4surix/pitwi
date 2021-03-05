# ---------------------------------------------------------------------------
# Source :
# - https://gist.github.com/jtriley/1108174
# - http://stackoverflow.com/questions/566746/how-to-get-console-window-width-in-python


import os
import sys
import shlex
import struct
import colorama
import platform
import subprocess

from threading import Thread
from time import sleep


from . import colors


current_os = platform.system()

if current_os == 'Windows':

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
        while datas:
            sys.stdout.write(
                datas.pop(0)
                .encode(sys_stdout.encoding, 'replace')
                .decode(sys_stdout.encoding, 'replace')
            )

p = Thread(target=run)
p.daemon = True
p.start()

def format_and_write(value, x, y, width, height, COLOR):

    i = h = 0

    data = ''
    surplus = 0

    RESET = colors.FG.get('reset') + colors.BG.get('reset')

    while i < len(value) and h < height:

        part = part__ = value[i : i + width - surplus]

        nl = 0
        index = 0

        while '\n' in part:
            nl += 1
            index = part__.index('\n')
            part__ = part__.replace('\n', ' ', 1)
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
            surplus = len(part__) - index - 1 # \n

    datas.append(data)