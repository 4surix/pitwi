# coding: utf-8
# Python 3.6.2
# ----------------------------------------------------------------------------


from .button import Button


class CheckButton(Button):

    def __init__(self, *values, **kwargs):

        kwargs['function'] = self.change_value

        super().__init__(**kwargs)

        self.values = values
        self.index = 0

        self.value = values[0]

    def copy(self, *values, **kwargs):
        attrs = {**self.__dict__}
        attrs.update(kwargs)
        return CheckButton(*(values or self.values), **attrs)

    def change_value(self):

        self.index += 1

        if self.index >= len(self.values):
            self.index = 0

        self.set(self.values[self.index])