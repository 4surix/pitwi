# coding: utf-8
# Python 3.6.2
# ----------------------------------------------------------------------------

from threading import Thread
from . import keypress


binds = {}


def add(carac, function):
    binds[carac] = function


def run():
    while True:
        key = keypress.getName()
        binds.get(key, lambda : None)()


p = Thread(target=run)
p.daemon = True
p.start()