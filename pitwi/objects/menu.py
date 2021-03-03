# coding: utf-8
# Python 3.6.2
# ----------------------------------------------------------------------------

import os

from time import sleep


from .. import ids
from .zone import Zone
from .button import Button
from .carousel import Carousel


class Menu(Carousel):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def copy(self, **kwargs):
        attrs = {**self.__dict__}
        attrs.update(kwargs)
        return Menu(**attrs)

    def config_buttons(self, zone:Zone, *, style:dict = {}):
        self.info_config_buttons = (zone, style)
        return self

    def add(self, value_button, widget):

        zone, style = self.info_config_buttons

        zone.add(
            Button(
                value_button, 
                **style, 
                function = self.__function(len(self.childs))
            )
        )

        return Carousel.add(self, widget)

    def __function(self, index:int):
        """
        L'orsque la création de lambda se fait directement,
          index changais de valeur.
        Donc on fais une fonction intermediaire, 
          pour que index devienne une closure
          et ne change pas de valeur.
        """
        return lambda: self.change(index)