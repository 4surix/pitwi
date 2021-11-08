# coding: utf-8
# Python 3.6.2
# ----------------------------------------------------------------------------

from threading import Thread
from . import navigation
from . import keypress


binds = {}


def add(carac, function):
    binds[carac] = function


running = True

entry_active = None

def run():

    global running

    while True:
        key = keypress.getName()
        binds.get(key, lambda : None)()

        if key == 'Ctrl+C':
            keypress.getKey.unlisten()
            running = False
            exit()

        if key == 'Tab':
            navigation.next()
            continue

        if key == 'Ctrl+Tab':
            navigation.previous()
            continue

        if entry_active:
            entry_active.add(key)


p = Thread(target=run)
p.daemon = True
p.start()