#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Python 3.6.2
# ----------------------------------------------------------------------------

"""Capture de touche clavier pressée.

Utilisation:
```
import keypress

if keypress.getName() == 'Tab':
    print('Tab !')

if keypress.getKey() == '\t':
    print('Tab !')
```
"""

__title__ = "keypress"
__author__ = "Asurix"
__license__ = "MIT"
__version__ = "1.0.0"
__github__ = "https://github.com/4surix/keypress"


import string
import platform


name_system = platform.system()

if name_system == 'Linux':

    import sys, tty, termios

    class GetKey:

        listened = False

        def __call__(self) -> str:

            key = ''
            
            self.listen()

            # Lis le prochain caractère.
            try: key = sys.stdin.read(1)
            finally:
                key = key if self.listened else ''
                # Remet les valeurs du descripteur de fichier comme avant
                #   après la transmission de toute sortie en file d’attente.
                self.unlisten()

            return key

        def listen(self):
            self.descripteur_fichier:int = sys.stdin.fileno()
            self.anciens_parametres = termios.tcgetattr(self.descripteur_fichier)
            tty.setraw(self.descripteur_fichier)
            self.listened = True

        def unlisten(self):
            if self.listened:
                termios.tcsetattr(
                    self.descripteur_fichier, termios.TCSADRAIN, self.anciens_parametres
                )
                self.listened = False

    getKey = GetKey()

elif name_system == 'Windows':

    import time
    from msvcrt import getch, kbhit

    def getKey() -> str:

        while not kbhit():
            time.sleep(0.1)

        return chr(getch()[0])

    getKey.listen = lambda: None
    getKey.unlisten = lambda: None

elif name_system == 'Darwin':

    import Carbon

    EventAvail = Carbon.Evt.EventAvail
    GetNextEvent = Carbon.Evt.GetNextEvent

    def getKey() -> str:

        if EventAvail(0x0008)[0] == 0:
            return ''

        else:
            return chr(GetNextEvent(0x0008)[1][1] & 0x000000FF)

    getKey.listen = lambda: None
    getKey.unlisten = lambda: None


COMBI_CTRL = {
    chr(i): 'Ctrl+' + carac
    for i, carac in enumerate(string.ascii_uppercase, start=1)
}

COMBI_ALTGR = {
    chr(i): 'AltGr+' + carac
    for i, carac in enumerate(
        'AZERTYUIOP????QSDFGHJKLM????WXCVBN', 
        start=16
    )
}

def getName() -> str:

    key = getKey()

    if key == '\x08':
        key = 'BackSpace'

    elif key == '\x1b':
        key = 'Escape'

    elif key == '\r':
        key = 'Return'

    elif key == '\t':
        key = 'Tab'

    elif key == '\xe0':

        key = getKey()

        if key == 'H':
            key = 'Up'

        elif key == 'P':
            key = 'Down'

        elif key == 'K':
            key = 'Left'

        elif key == 'M':
            key = 'Right'

        elif key == 'S':
            key = 'Delete'

        elif key == 'R':
            key = 'Insert'

        elif key == 'Q':
            key = 'PageUp'

        elif key == 'I':
            key = 'PageDown'

        elif key == 'G':
            key = 'Begin'

        elif key == 'O':
            key = 'End'

        elif key == '\x85':
            key = 'F11'

        elif key == '\x86':
            key = 'F12'

    elif key == '\x00':

        key = getKey()

        if key == ';':
            key = 'F1'

        elif key == '<':
            key = 'F2'

        elif key == '=':
            key = 'F3'

        elif key == '>':
            key = 'F4'

        elif key == '?':
            key = 'F5'

        elif key == '@':
            key = 'F6'

        elif key == 'A':
            key = 'F7'

        elif key == 'B':
            key = 'F8'

        elif key == 'C':
            key = 'F9'

        elif key == 'D':
            key = 'F10'

        elif key == '£':
            key = 'AltGr+Delete'

        elif key == '\x94':
            key = 'Ctrl+Tab'

        else:
            key = COMBI_ALTGR.get(key, key)

    else:
        key = COMBI_CTRL.get(key, key)

    return key