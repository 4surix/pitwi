# encode: utf-8
# Python 3.6.2
# ----------------------------------------------------------------------------


class IDS:

    def __init__(self):
        self.ids = {}

    def get(self, ID):
        return self.__dict__.get(ID)

    def set(self, ID, widget):

        if ID in self.__dict__:
            return False

        self.__dict__[ID] = widget
        return True

IDS = IDS()

get = IDS.get
set = IDS.set