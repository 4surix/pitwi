# ---------------------------------------------------------------------------
# Source :
# - https://gist.github.com/jtriley/1108174
# - http://stackoverflow.com/questions/566746/how-to-get-console-window-width-in-python


import os
import sys
import struct
import platform

from threading import Thread
from time import sleep


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


datas = []

def write(data):
    datas.append(data)


def run():
    while True:
        while datas:
            sys.stdout.write(datas.pop(0))
        sleep(1)

p = Thread(target=run)
p.daemon = True
p.start()